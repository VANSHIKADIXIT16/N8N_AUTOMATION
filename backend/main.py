from fastapi import FastAPI
from backend.database import engine
from sqlalchemy import text
from backend.models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user_schema import UserCreate, UserResponse
from backend import crud
from backend.schemas.ticket_schema import TicketCreate, TicketResponse
from backend.services.workflow_engine import process_ticket_workflow
from backend.routes import notification_routes

app = FastAPI()

app.include_router(notification_routes.router)

@app.on_event("startup")
def test_db_connection():
    # ✅ Auto create tables
    Base.metadata.create_all(bind=engine)

    # ✅ Test DB connection
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Database Connected Successfully")
    except Exception as e:
        print("❌ Database Connection Failed")
        print(e)

@app.get("/")
def read_root():
    return {"message": "Workflow Backend Running 🚀"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):

    # Step 1: create ticket
    db_ticket = crud.create_ticket(db, ticket)

    # Step 2: create workflow execution
    execution = crud.create_workflow_execution(
        db,
        entity_type="ticket",
        entity_id=db_ticket.id
    )

    # Step 3: run workflow engine
    process_ticket_workflow(db, db_ticket.id, execution.id)

    return db_ticket

