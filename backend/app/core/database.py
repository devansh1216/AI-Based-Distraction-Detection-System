"""
Database configuration for PostgreSQL using SQLAlchemy.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./distraction.db",
)

# SQLAlchemy Engine
engine_options = {
    "pool_pre_ping": True,
    "future": True,
}

if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_options)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    future = True,
)

def get_db():
    """
    Creates a new database session for each request
    and ensures it is properly closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()