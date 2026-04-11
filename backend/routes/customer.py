from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services import customer_service
from backend.schemas.customer_schema import CustomerCreate

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, customer)


@router.get("/")
def get_all_customers(db: Session = Depends(get_db)):
    return customer_service.get_customers(db)
