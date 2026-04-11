from sqlalchemy.orm import Session
from backend.models import Ticket, WorkflowExecution
from datetime import datetime
from backend.services.n8n_service import trigger_n8n_workflow

def process_ticket_workflow(db: Session, ticket_id: int, execution_id: int):
    try:
        # Get ticket
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise Exception("Ticket not found")
            
        # ✅ TRIGGER N8N WORKFLOW (Replaces local automation logic)
        n8n_data = {
            "event": "ticket_created",
            "ticket_id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "category": ticket.category,
            "customer_id": ticket.customer_id
        }
        
        trigger_n8n_workflow(n8n_data)

        # Update workflow execution status
        execution = db.query(WorkflowExecution).filter(
            WorkflowExecution.id == execution_id
        ).first()

        if execution:
            execution.status = "COMPLETED"
            execution.completed_at = datetime.utcnow()

        db.commit()
        print(f"✅ Ticket {ticket_id} processed via n8n workflow")

    except Exception as e:
        print(f"❌ Workflow error: {str(e)}")
        execution = db.query(WorkflowExecution).filter(
            WorkflowExecution.id == execution_id
        ).first()

        if execution:
            execution.status = "FAILED"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()

        db.commit()

# ... (rest of the file can be cleaned up or removed if no longer used)

    text = (ticket.title + " " + ticket.description).lower()

    if "refund" in text or "payment" in text:
        return "billing"

    elif "error" in text or "bug" in text or "login" in text:
        return "engineering"

    else:
        return "support"

def assign_agent(db: Session, department: str):
    
    from models import User, Ticket

    agents = db.query(User).filter(
        User.role == "agent",
        User.department == department
    ).all()

    if not agents:
        return None

    # count tickets assigned to each agent
    agent_ticket_counts = []

    for agent in agents:
        count = db.query(Ticket).filter(
            Ticket.assigned_to == agent.id
        ).count()

        agent_ticket_counts.append((agent.id, count))

    # choose agent with minimum tickets
    selected_agent = min(agent_ticket_counts, key=lambda x: x[1])

    return selected_agent[0]
