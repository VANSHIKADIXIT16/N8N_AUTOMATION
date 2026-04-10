from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# ✅ Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
print("ENV VALUE:", os.getenv("DATABASE_URL"))

# ✅ Fix for Render (in case URL starts with postgres://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ❌ Do NOT allow fallback (prevents accidental local DB usage)
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in .env file")

# 🔍 Debug (optional but helpful)
print("🚀 Connected to DB:", DATABASE_URL)

# ✅ Create SQLAlchemy engine (stable for cloud DB like Render)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # avoids stale connections
)

# ✅ Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base class for all models
Base = declarative_base()

# ✅ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()