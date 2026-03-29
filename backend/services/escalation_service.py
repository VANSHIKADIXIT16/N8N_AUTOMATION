from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.models import Ticket, User
from backend.services.notification_service import create_notification


def check_ticket_escalations(db: Session):

    tickets = db.query(Ticket).filter(Ticket.status != "RESOLVED").all()

    for ticket in tickets:

        time_passed = datetime.utcnow() - ticket.created_at

        if time_passed > timedelta(hours=24):

            old_agent = ticket.assigned_to

            # ✅ FIX: Get valid user from DB
            new_user = db.query(User).first()

            if not new_user:
                print("⚠ No agent available for escalation")
                continue

            new_agent = new_user.id

            if old_agent != new_agent:

                ticket.assigned_to = new_agent
                db.commit()
                db.refresh(ticket)

                create_notification(
                    db=db,
                    user_id=new_agent,
                    message=f"Ticket #{ticket.id} reassigned after delay.",
                    type="escalation"
                )