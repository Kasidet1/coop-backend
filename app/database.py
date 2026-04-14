from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

# ======================
# DATABASE URL (Vercel / Local safe)
# ======================

DATABASE_URL = os.getenv("DATABASE_URL")

# ======================
# Engine (SAFE INIT)
# ======================

engine = None
SessionLocal = None

if DATABASE_URL:
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
    print("⚠️ WARNING: DATABASE_URL is missing (check Vercel env)")

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
