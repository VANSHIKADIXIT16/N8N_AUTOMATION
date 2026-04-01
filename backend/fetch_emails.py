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
# ✅ MAIN FUNCTION
# =========================
def fetch_and_process_emails():
    print("🚀 fetch_and_process_emails started")

    try:
        service = get_gmail_service()

        results = service.users().messages().list(
            userId='me',
            q='is:unread newer_than:1d'
        ).execute()

        messages = results.get('messages', [])

        print(f"📬 Emails fetched: {len(messages)}")

        if not messages:
            return

        db = SessionLocal()

        # 🔁 Recursive parts extractor
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
            print("❌ No role found")
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
                        print("📄 Processing:", filename)

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

                        score = calculate_score(
                            info["skills"], info["experience"]
                        )

                        status = determine_status(
                            score, info["experience"]
                        )

                        candidate_email = (
                            info["email"] if info["email"] != "N/A" else sender
                        )

                        existing = db.query(Candidate).filter(
                            Candidate.email == candidate_email
                        ).first()

                        if existing:
                            print("⚠️ Duplicate, skipping")
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

                        print("✅ Saved")

                        send_email_gmail(
                            sender,
                            "Application Update",
                            f"Status: {status}"
                        )

                if not found_pdf:
                    print("⚠️ No PDF found")

                # mark as read
                service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()

            except Exception as e:
                print("❌ Error processing email:", e)

        db.close()

    except Exception as e:
        print("❌ Email fetch error:", e)