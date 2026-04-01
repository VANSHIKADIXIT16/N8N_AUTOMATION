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
from backend.routes import ticket_routes, escalation_routes
from backend.routes import dashboard_routes 
from backend.routes import customer_routes
from backend.schemas.customer_schema import CustomerCreate, CustomerResponse

# ✅ AUTH IMPORT
from backend.auth import auth_routes


app = FastAPI()

# ✅ EXISTING ROUTES (UNCHANGED)
app.include_router(notification_routes.router)
app.include_router(ticket_routes.router)
app.include_router(escalation_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(customer_routes.router)

# ✅ AUTH ROUTES ADDED
app.include_router(auth_routes.router)


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