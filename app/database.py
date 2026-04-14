from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# =========================
# ENV
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL is missing (check Vercel Environment Variables)")

# =========================
# ENGINE
# =========================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# =========================
# SESSION
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# BASE MODEL
# =========================
Base = declarative_base()

# =========================
# DEPENDENCY (FastAPI)
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
