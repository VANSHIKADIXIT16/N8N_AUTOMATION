from database import SessionLocal
from models import Ticket

db = SessionLocal()

tickets = db.query(Ticket).all()

for t in tickets:
    print(f"ID: {t.id}, Title: {t.title}, Status: {t.status}, Priority: {t.priority}")

db.close()