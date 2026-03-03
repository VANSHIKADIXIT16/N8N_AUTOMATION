from pydantic import BaseModel, EmailStr
from datetime import datetime


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True