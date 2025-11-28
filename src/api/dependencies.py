"""
API Dependencies

Shared dependencies for FastAPI routers.
Provides database session management and other common dependencies.
"""

from typing import Generator
from sqlalchemy.orm import Session

from ..services.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI endpoints.
    
    Yields a database session and ensures it's properly closed after use.
    This is the standard pattern for database session management in FastAPI.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        ```python
        @router.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()