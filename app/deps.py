"""Dependency injection functions for FastAPI routes."""
from typing import Generator
from sqlalchemy.orm import Session
from app.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Create a database session for a request.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
