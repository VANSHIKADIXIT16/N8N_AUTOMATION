from sqlalchemy.orm import Session
from backend.models import Ticket, WorkflowExecution, AIEvaluation
from datetime import datetime


def process_ticket_workflow(db: Session, ticket_id: int, execution_id: int):

    try:

        # Get ticket
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

        description = ticket.description.lower()

        # Simple AI logic
        if "urgent" in description:
            priority = "HIGH"
            sentiment = "negative"

        elif "refund" in description:
            priority = "MEDIUM"
            sentiment = "neutral"

        else:
            priority = "LOW"
            sentiment = "positive"

        # Save AI evaluation
        ai_eval = AIEvaluation(
            related_type="ticket",
            related_id=ticket_id,
            ai_score=priority,
            classification="support_ticket",
            sentiment=sentiment,
            confidence="0.90",
            created_at=datetime.utcnow()
        )

        db.add(ai_eval)

        # Update ticket
        ticket.priority = priority
        ticket.status = "IN_PROGRESS"
        ticket.updated_at = datetime.utcnow()

        # Update workflow execution
        execution = db.query(WorkflowExecution).filter(
            WorkflowExecution.id == execution_id
        ).first()

        execution.status = "COMPLETED"
        execution.completed_at = datetime.utcnow()

        db.commit()

    except Exception as e:

        execution = db.query(WorkflowExecution).filter(
            WorkflowExecution.id == execution_id
        ).first()

        execution.status = "FAILED"
        execution.error_message = str(e)
        execution.completed_at = datetime.utcnow()

        db.commit()