from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.ticket_schema import TicketCreate, TicketResponse
from backend.schemas.ticket_message_schema import TicketMessageCreate, TicketMessageResponse
from backend.services.workflow_engine import process_ticket_workflow
from backend import crud
from backend.models import Ticket
from backend.services.notification_service import create_notification

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketResponse)
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

@router.get("/assigned/{agent_id}")
def get_assigned_tickets(agent_id: int, db: Session = Depends(get_db)):

    tickets = db.query(Ticket).filter(Ticket.assigned_to == agent_id).all()

    return tickets

@router.patch("/{ticket_id}/status")
def update_ticket_status(ticket_id: int, status: str, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    ticket.status = status
    db.commit()
    db.refresh(ticket)

    return ticket

@router.patch("/{ticket_id}/resolve")
def resolve_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    # Update ticket status
    ticket.status = "RESOLVED"
    db.commit()
    db.refresh(ticket)

    # Create notification for customer
    message = f"Your ticket #{ticket.id} has been resolved by support."

    create_notification(
        db=db,
        user_id=ticket.customer_id,
        message=message,
        type="system"
    )

    return {"message": "Ticket resolved and notification sent"}

@router.get("/customer/{customer_id}")
def get_customer_tickets(customer_id: int, db: Session = Depends(get_db)):

    tickets = db.query(Ticket).filter(Ticket.customer_id == customer_id).all()

    return tickets

@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    return ticket

@router.post("/{ticket_id}/messages" , response_model=TicketMessageResponse)
def send_message(ticket_id: int, message: TicketMessageCreate, db: Session = Depends(get_db)):

    return crud.create_ticket_message(
        db,
        ticket_id,
        message.sender_id,
        message.message
    )

@router.get("/{ticket_id}/messages", response_model=list[TicketMessageResponse])
def get_messages(ticket_id: int, db: Session = Depends(get_db)):

    return crud.get_ticket_messages(db, ticket_id)