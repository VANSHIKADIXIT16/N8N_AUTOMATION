from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Shared Properties
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str


# For Creating User
class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# For Returning User (Response)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2