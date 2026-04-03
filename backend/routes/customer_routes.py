from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.customer_schema import CustomerCreate

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@router.get("/")
def get_all_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)
