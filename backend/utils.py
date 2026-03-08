import re
import PyPDF2
import io

# Regex for email extraction
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Regex for experience extraction (e.g., "5 years", "3+ years")
EXPERIENCE_REGEX = r'(\d+)\s*(?:\+)?\s*years'

# Keywords for skills
SKILLS_LIST = [
    "Python", "JavaScript", "React", "Node.js", "SQL", "Machine Learning", 
    "Data Analysis", "Project Management", "Communication", "Leadership",
    "Customer Support", "Sales", "Marketing", "Cloud Computing", "AWS", "Azure"
]

# Complaint routing keywords
DEPARTMENT_KEYWORDS = {
    "IT Support": ["computer", "software", "hardware", "internet", "password", "system", "email", "bug", "crash"],
    "HR": ["payroll", "leave", "salary", "recruitment", "benefit", "policy", "employee"],
    "Finance": ["invoice", "payment", "billing", "refund", "tax", "budget", "expense"],
    "General": []  # Default
}

def extract_text_from_pdf(pdf_content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_candidate_info(text: str):
    # Extract email
    email_match = re.search(EMAIL_REGEX, text)
    email = email_match.group(0) if email_match else "N/A"
    
    # Extract skills
    found_skills = [skill for skill in SKILLS_LIST if skill.lower() in text.lower()]
    
    # Extract experience (summing multiple mentions or taking the max)
    exp_matches = re.findall(EXPERIENCE_REGEX, text.lower())
    experience = max([int(e) for e in exp_matches]) if exp_matches else 0
    
    return {
        "email": email,
        "skills": found_skills,
        "experience": experience
    }

def calculate_score(skills: list, experience: int) -> float:
    # Example scoring: 10 points per skill (max 50) + 10 points per year of experience (max 50)
    skill_score = min(len(skills) * 10, 50)
    exp_score = min(experience * 10, 50)
    return float(skill_score + exp_score)

def determine_status(score: float, experience: int) -> str:
    # Eligibility criteria: at least 40 points and 2 years experience
    if score >= 40 and experience >= 2:
        return "Shortlisted"
    return "Rejected"

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import base64
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email_gmail(to_email: str, subject: str, content: str):
    """
    Sends an email using the Gmail API.
    Requires credentials.json and token.json.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This part requires manual setup and credentials.json file
            # For this simulation, we'll log a message instead.
            print(f"Gmail API not configured. Would have sent to {to_email}: {content}")
            return False
            
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content(content)
        message['To'] = to_email
        message['From'] = 'me'
        message['Subject'] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
        
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f'Message Id: {send_message["id"]}')
        return True
    except Exception as error:
        print(f'An error occurred: {error}')
        return False

def route_complaint(description: str) -> str:
    description_lower = description.lower()
    for dept, keywords in DEPARTMENT_KEYWORDS.items():
        if any(keyword in description_lower for keyword in keywords):
            return dept
    return "General"
