from sqlalchemy.orm import Session
from backend.models.customer import Customer
from backend.schemas.customer_schema import CustomerCreate

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(
        user_id=customer.user_id,
        name=customer.name,
        email=customer.email,
        phone=customer.phone
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session):
    return db.query(Customer).all()
