import os.path
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from database import SessionLocal
from models import Candidate, Complaint
from utils import extract_text_from_pdf, extract_candidate_info, calculate_score, determine_status, route_complaint, send_email_gmail

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def process_unread_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])

    if not messages:
        print("No unread messages found.")
        return

    db = SessionLocal()
    
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        
        subject = ""
        sender = ""
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']
        
        # Check for attachments
        parts = payload.get('parts', [])
        for part in parts:
            if part.get('filename') and part.get('filename').endswith('.pdf'):
                # Process Resume
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=msg['id'], id=attachment_id).execute()
                data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                
                text = extract_text_from_pdf(data)
                info = extract_candidate_info(text)
                score = calculate_score(info["skills"], info["experience"])
                status = determine_status(score, info["experience"])
                
                new_candidate = Candidate(
                    name=part['filename'].split('.')[0],
                    email=info["email"] if info["email"] != "N/A" else sender,
                    skills=", ".join(info["skills"]),
                    experience=info["experience"],
                    score=score,
                    status=status
                )
                db.add(new_candidate)
                db.commit()
                
                # Send Reply
                reply_content = f"Hello, we have received your resume. Status: {status}."
                send_email_gmail(sender, "Application Update", reply_content)
                
            elif "complaint" in subject.lower():
                # Process Complaint
                body = ""
                if 'parts' in part:
                    for subpart in part['parts']:
                        if subpart['mimeType'] == 'text/plain':
                            body = base64.urlsafe_b64decode(subpart['body']['data']).decode()
                elif part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode()
                
                if body:
                    dept = route_complaint(body)
                    new_complaint = Complaint(
                        user_name=sender,
                        email=sender,
                        description=body,
                        department=dept
                    )
                    db.add(new_complaint)
                    db.commit()
                    
                    # Send Reply
                    reply_content = f"Hello, your complaint has been routed to the {dept} department."
                    send_email_gmail(sender, "Complaint Update", reply_content)

        # Mark as read
        service.users().messages().batchModify(
            userId='me',
            body={'ids': [msg['id']], 'removeLabelIds': ['UNREAD']}
        ).execute()

    db.close()

if __name__ == "__main__":
    process_unread_emails()
