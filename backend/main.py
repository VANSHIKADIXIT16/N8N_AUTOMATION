from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Response
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from threading import Thread
import time

from models import Candidate, Complaint, Role, Skill, User
from database import engine, get_db, Base
from utils import extract_text_from_pdf, extract_candidate_info, calculate_score, determine_status, route_complaint, send_email_gmail
from fetch_emails import fetch_and_process_emails
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Import new routes and schemas
from routes import notification_routes, ticket_routes, escalation_routes, dashboard_routes, customer_routes
from schemas.user_schema import UserCreate, UserResponse
import crud

app = FastAPI(title="Resume Parsing & Complaint Routing System")

# Include new routers
app.include_router(notification_routes.router)
app.include_router(ticket_routes.router)
app.include_router(escalation_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(customer_routes.router)
# temp add
import requests

print(requests.get("https://www.google.com").status_code)
# ✅ Background Email Worker
def email_worker():
    while True:
        try:
            print("📩 Checking for new emails...")
            fetch_and_process_emails()
        except Exception as e:
            print("❌ Email fetch error:", str(e))
        time.sleep(60)  # check every 60 seconds

# ✅ Start on backend startup
@app.on_event("startup")
def start_email_listener():
    thread = Thread(target=email_worker, daemon=True)
    thread.start()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS Fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/roles/")
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@app.post("/roles/")
def create_role(name: str, db: Session = Depends(get_db)):
    print(f"Creating role: {name}")
    existing = db.query(Role).filter(Role.name == name).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    new_role = Role(name=name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return {"id": new_role.id, "name": new_role.name}

@app.post("/roles/{role_id}/skills/")
def add_skills(role_id: int, skills: List[dict], db: Session = Depends(get_db)):
    print(f"Adding skills to role {role_id}: {skills}")
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    created_skills = []
    
    for skill_data in skills:
        skill = Skill(
            name=skill_data["name"],
            type=skill_data.get("type", "optional"),
            role_id=role_id
        )
        db.add(skill)
        created_skills.append(skill.name)
    
    db.commit()
    
    return {
        "message": "Skills added successfully",
        "skills": created_skills
    }

@app.get("/roles/{role_id}/skills/")
def get_skills(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    skills = [skill.name for skill in role.skills]
    
    return {
        "role": role.name,
        "skills": skills
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Parsing & Complaint Routing System API"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/upload_resume/")
async def upload_resume(
    file: UploadFile = File(...), 
    role_id: int = Form(...),
    parsed_data: str = Form(None),
    db: Session = Depends(get_db)
):
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    skills_from_db = [{"name": skill.name, "type": skill.type} for skill in role.skills]

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    import json
    info = None
    if parsed_data:
        try:
            info = json.loads(parsed_data)
        except:
            pass
            
    if not info:
        content = await file.read()
        text = extract_text_from_pdf(content)
        info = extract_candidate_info(text, skills_from_db)

        if "name" not in info or info["name"] == "Unknown":
            info["name"] = file.filename.split('.')[0]
    
    name = info.get("name", file.filename.split('.')[0])
    email = info.get("email", "N/A")
    skills = info.get("skills", [])
    
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
    
    experience = info.get("experience", 0)
    
    score = calculate_score(skills, experience)
    status = determine_status(score, experience)
    
    new_candidate = Candidate(
        name=name,
        email=email,
        skills=", ".join([s["name"] if isinstance(s, dict) else s for s in skills]),
        experience=experience,
        score=score,
        status=status,
        role_id=role_id
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    
    subject = f"Application Status Update - {new_candidate.name}"
    email_response = f"Hello {new_candidate.name}, your application has been processed. Status: {status}."
    
    email_sent = send_email_gmail(email, subject, email_response)
    
    return {
        "candidate_id": new_candidate.id,
        "name": name,
        "email": email,
        "skills": skills,
        "experience": experience,
        "score": score,
        "status": status,
        "email_response": email_response,
        "email_sent": email_sent
    }

@app.post("/submit_complaint/")
async def submit_complaint(user_name: str = Form(...), email: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    department = route_complaint(description)
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
