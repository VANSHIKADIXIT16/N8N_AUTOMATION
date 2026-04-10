from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base
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
    role_id = Column(Integer, ForeignKey("roles.id"))
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
    type = Column(String, default="optional")  # ✅ ADD THIS LINE

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="skills")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin / hr / support / employee
    department = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    customers = relationship("Customer")
    employee = relationship("Employee", back_populates="user")
    tickets = relationship("Ticket", back_populates="assigned_user")
    notifications = relationship("Notification", back_populates="user")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    department = Column(String)
    job_title = Column(String)
    joining_date = Column(DateTime)
    employment_type = Column(String)
    status = Column(String)  # active / probation / terminated
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="employee")
    documents = relationship("EmployeeDocument", back_populates="employee")

class EmployeeDocument(Base):
    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    document_type = Column(String)
    file_url = Column(String)
    verification_status = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    employee = relationship("Employee", back_populates="documents")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tickets = relationship("Ticket", back_populates="customer")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    priority = Column(String)
    status = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    department = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="tickets")
    assigned_user = relationship("User", back_populates="tickets")
    messages = relationship("TicketMessage", back_populates="ticket")

class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    ticket = relationship("Ticket", back_populates="messages")

class AIEvaluation(Base):
    __tablename__ = "ai_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    related_type = Column(String)  # employee / ticket
    related_id = Column(Integer)
    ai_score = Column(String)
    classification = Column(String)
    sentiment = Column(String)
    confidence = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String)  # employee / ticket
    entity_id = Column(Integer)
    workflow_name = Column(String)
    status = Column(String)  # running / success / failed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    type = Column(String)  # email / slack / system
    status = Column(String)  # sent / failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="notifications")
