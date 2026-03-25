from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 🔹 1. Database URL
DATABASE_URL = "postgresql://postgres:rootadmin123@localhost:5432/workflow_db"

# 🔹 2. Create Engine
engine = create_engine(DATABASE_URL)

# 🔹 3. Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 4. Base class for models
Base = declarative_base()

# 🔹 5. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()