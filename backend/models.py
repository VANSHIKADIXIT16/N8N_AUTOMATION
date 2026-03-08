from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    skills = Column(String)
    experience = Column(Integer)
    score = Column(Float)
    status = Column(String)  # Shortlisted, Rejected, Pending
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    email = Column(String)
    description = Column(String)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
