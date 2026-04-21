from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os

# ======================
# Load .env
# ======================

load_dotenv()

# ======================
# DATABASE URL
# ======================

DATABASE_URL = os.getenv("DATABASE_URL")

# ======================
# Engine (SAFE INIT)
# ======================

engine = None
SessionLocal = None

if DATABASE_URL:

    # SQLite (Local Dev)
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False}
        )

    # PostgreSQL / Supabase / Vercel
    else:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"sslmode": "require"}
        )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

else:
    print("⚠️ WARNING: DATABASE_URL is missing (check .env / Vercel env)")

# ======================
# Base Model
# ======================

Base = declarative_base()

# ======================
# Dependency
# ======================

def get_db():
    if SessionLocal is None:
        raise Exception("Database not initialized: DATABASE_URL missing")

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
