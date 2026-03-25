from sqlalchemy import Column, Integer, String, Float, DateTime,ForeignKey
from sqlalchemy.orm import relationship
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

# ✅ NEW MODELS

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    skills = relationship("Skill", back_populates="role")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="skills")