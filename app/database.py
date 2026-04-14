from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ======================
# DATABASE URL
# ======================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")


# ======================
# Engine
# ======================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}   # เพิ่มอันนี้สำหรับ Supabase
)


# ======================
# Session
# ======================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ======================
# Base Model
# ======================

Base = declarative_base()


# ======================
# Dependency
# ======================

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()