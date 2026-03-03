from fastapi import FastAPI
from backend.database import engine
from sqlalchemy import text
from backend.models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user_schema import UserCreate, UserResponse
from backend import crud

app = FastAPI()

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