from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    customer_id: int
    title: str
    description: str
    category: str
    priority: str
    status: str
    assigned_to: int


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True