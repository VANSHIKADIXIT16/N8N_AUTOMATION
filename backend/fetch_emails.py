import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from database import SessionLocal
from models import Candidate, Role

from utils import (
    extract_text_from_pdf,
    extract_candidate_info,
    calculate_score,
    determine_status,
    send_email_gmail
)

# ✅ Scheduler
from apscheduler.schedulers.background import BackgroundScheduler

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# =========================
# ✅ GMAIL CONNECTION
# =========================
def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

# =========================
# ✅ FETCH & PROCESS EMAILS
# =========================
def fetch_and_process_emails():
    print("🚀 fetch_and_process_emails started")
    print("Connecting to mailbox...")

    try:
        service = get_gmail_service()

        # For testing, use only 'is:unread'; you can add 'newer_than:1d' later
        # results = service.users().messages().list(
        # userId='me',
        #     q='has:attachment filename:pdf'  # Fetch all emails with PDF attachments
        # ).execute()
        results = service.users().messages().list(
    userId='me',
        maxResults=10
    ).execute()

        messages = results.get('messages', [])
        print(f"📬 Emails fetched: {len(messages)}")
        print("DEBUG: Raw results from Gmail API:", results)
        if 'messages' in results:
             print("Message IDs:", [m['id'] for m in results['messages']])
        if not messages:
            print("⚠️ No new unread emails found.")
            return

        db = SessionLocal()

        # Recursive function to extract all parts (PDF attachments etc.)
        def get_parts(payload):
            parts = []
            if 'parts' in payload:
                for p in payload['parts']:
                    parts.extend(get_parts(p))
            else:
                parts.append(payload)
            return parts

        role = db.query(Role).first()
        if not role:
            print("❌ No role found in DB.")
            db.close()
            return

        skills_from_db = [{"name": s.name, "type": s.type} for s in role.skills]

        for msg in messages:
            try:
                print("\n📨 Processing email:", msg['id'])

                message = service.users().messages().get(
                    userId='me', id=msg['id']
                ).execute()

                payload = message.get('payload', {})
                headers = payload.get('headers', [])

                sender = ""
                for h in headers:
                    if h['name'] == 'From':
                        sender = h['value']

                parts = get_parts(payload)

                found_pdf = False
        
                for part in parts:
                    filename = part.get('filename')
                    if filename and filename.lower().endswith('.pdf'):
                        found_pdf = True
                        print("📄 Processing attachment:", filename)

                        attachment = service.users().messages().attachments().get(
                            userId='me',
                            messageId=msg['id'],
                            id=part['body']['attachmentId']
                        ).execute()

                        data = base64.urlsafe_b64decode(
                            attachment['data'].encode('UTF-8')
                        )

                        text = extract_text_from_pdf(data)
                        info = extract_candidate_info(text, skills_from_db)

                        score = calculate_score(info["skills"], info["experience"])
                        status = determine_status(score, info["experience"])

                        candidate_email = info["email"] if info["email"] != "N/A" else sender

                        existing = db.query(Candidate).filter(
                            Candidate.email == candidate_email
                        ).first()
                        if existing:
                            print("⚠️ Duplicate candidate, skipping")
                            continue

                        new_candidate = Candidate(
                            name=filename.split('.')[0],
                            email=candidate_email,
                            skills=", ".join([s["name"] for s in info["skills"]]),
                            experience=info["experience"],
                            score=score,
                            status=status,
                            role_id=role.id
                        )
                        db.add(new_candidate)
                        db.commit()
                        print("✅ Candidate saved:", candidate_email)

                        send_email_gmail(
                            candidate_email,
                            "Application Update",
                            f"Status: {status}"
                        )

                if not found_pdf:
                    print("⚠️ No PDF attachments found in email.")

                # Mark message as read
                service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()

            except Exception as e:
                print("❌ Error processing email:", e)

        db.close()
        print("🚀 Finished processing all emails.")

    except Exception as e:
        print("❌ Email fetch error:", e)

# =========================
# ✅ START BACKGROUND SCHEDULER (1 MINUTE INTERVAL)
# =========================
scheduler = None

def start_email_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        # Run fetch_and_process_emails every 1 minute
        scheduler.add_job(fetch_and_process_emails, 'interval', minutes=1)
        scheduler.start()
        print("⏱ Email fetch scheduler started (runs every 1 minute)")

# Only call once when server starts
start_email_scheduler()