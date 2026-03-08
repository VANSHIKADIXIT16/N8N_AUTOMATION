from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Candidate, Complaint
from utils import extract_text_from_pdf, extract_candidate_info, calculate_score, determine_status, route_complaint, send_email_gmail
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Parsing & Complaint Routing System")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Parsing & Complaint Routing System API"}

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read PDF content
    content = await file.read()
    text = extract_text_from_pdf(content)
    
    # Extract information
    info = extract_candidate_info(text)
    
    # Calculate score and determine status
    score = calculate_score(info["skills"], info["experience"])
    status = determine_status(score, info["experience"])
    
    # Store in database
    new_candidate = Candidate(
        name=file.filename.split('.')[0],
        email=info["email"],
        skills=", ".join(info["skills"]),
        experience=info["experience"],
        score=score,
        status=status
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    
    # Send automated email response
    subject = f"Application Status Update - {new_candidate.name}"
    email_response = f"Hello {new_candidate.name}, your application for a position has been processed. Status: {status}."
    
    # Attempt to send via Gmail API
    email_sent = send_email_gmail(info["email"], subject, email_response)
    
    return {
        "candidate_id": new_candidate.id,
        "email": info["email"],
        "skills": info["skills"],
        "experience": info["experience"],
        "score": score,
        "status": status,
        "email_response": email_response,
        "email_sent": email_sent
    }

@app.post("/submit_complaint/")
async def submit_complaint(user_name: str = Form(...), email: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    # Route complaint
    department = route_complaint(description)
    
    # Store in database
    new_complaint = Complaint(
        user_name=user_name,
        email=email,
        description=description,
        department=department
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    
    return {
        "complaint_id": new_complaint.id,
        "department": department,
        "message": f"Your complaint has been routed to {department} department."
    }

@app.get("/candidates/")
def get_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()

@app.get("/complaints/")
def get_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).all()
