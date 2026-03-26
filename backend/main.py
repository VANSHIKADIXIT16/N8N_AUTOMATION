from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Candidate, Complaint, Role, Skill
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Candidate, Complaint
from utils import extract_text_from_pdf, extract_candidate_info, calculate_score, determine_status, route_complaint, send_email_gmail
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Parsing & Complaint Routing System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/roles/")
def create_role(name: str, db: Session = Depends(get_db)):
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
    created_skills.append(skill_name)
    
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
        # Fallback to backend parsing if frontend data is missing
        content = await file.read()
        text = extract_text_from_pdf(content)
        info = extract_candidate_info(text, skills_from_db)
        # Handle cases where name is missing
        if "name" not in info or info["name"] == "Unknown":
            info["name"] = file.filename.split('.')[0]
    
    # Ensure consistency in info structure
    name = info.get("name", file.filename.split('.')[0])
    email = info.get("email", "N/A")
    skills = info.get("skills", [])
    experience = info.get("experience", 0)
    
    # Calculate score and determine status
    score = calculate_score(skills, experience)
    status = determine_status(score, experience)
    
    # Store in database
    new_candidate = Candidate(
        name=name,
        email=email,
        skills=", ".join([s["name"] for s in info["skills"]]),
        experience=experience,
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
