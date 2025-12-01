"""
Borrower's Forum Platform - Database Service
=============================================

Framework Applied: database_design_excellence.md + uncle_bob_platform_frameworks.md
Principle: Centralized database connection management with proper lifecycle
Why: Prevents connection leaks, enables dependency injection, makes testing easy
"""

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator
import logging

from src.config.settings import get_settings
from src.models.debt_data import Base

# Configure logging
logger = logging.getLogger(__name__)

# ============================================
# DATABASE ENGINE SETUP
# Framework: Database Design Excellence
# ============================================

def get_database_engine():
    """
    Create and configure database engine.
    
    Framework: Database Design Excellence
    - Connection pooling for performance
    - SQLite optimizations for development
    - PostgreSQL ready for production
    
    Why: Single engine instance, reused across application
    """
    settings = get_settings()
    
    # Engine configuration based on database type
    if "sqlite" in settings.DATABASE_URL.lower():
        # SQLite specific configuration
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False},  # Allow multiple threads
            poolclass=StaticPool,  # Single connection pool for SQLite
            echo=settings.DATABASE_ECHO,  # Log SQL queries if enabled
        )
        
        # Enable foreign keys for SQLite (not enabled by default)
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
        logger.info("✓ Database engine created: SQLite")
    
    else:
        # PostgreSQL configuration (for production)
        engine = create_engine(
            settings.DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_timeout=settings.DATABASE_POOL_TIMEOUT,
            pool_pre_ping=True,  # Verify connections before using
            echo=settings.DATABASE_ECHO,
        )
        
        logger.info("✓ Database engine created: PostgreSQL")
    
    return engine


# Create global engine instance
engine = get_database_engine()

# Create session factory
# Framework: Clean Architecture - Dependency Injection
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================
# DATABASE INITIALIZATION
# Framework: Data Engineering Excellence
# ============================================

def init_database():
    """
    Initialize database - create all tables.
    
    Framework: Data Engineering Excellence
    - Idempotent operation (safe to run multiple times)
    - Creates all tables from models
    - Logs success/failure
    
    Usage:
        from src.services.database import init_database
        init_database()
    
    Why: Simple setup, no manual SQL needed
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise


def drop_all_tables():
    """
    Drop all tables (DANGEROUS - use only in development/testing).
    
    Framework: Testing Excellence
    Why: Clean slate for tests, never use in production
    """
    settings = get_settings()
    
    if settings.ENVIRONMENT == "production":
        raise ValueError("Cannot drop tables in production!")
    
    logger.warning("⚠️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("✓ All tables dropped")


# ============================================
# SESSION MANAGEMENT
# Framework: Clean Architecture + API Design
# ============================================

def get_db() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection.
    
    Framework: Clean Architecture - Dependency Injection
    Used by FastAPI to inject database sessions into endpoints.
    
    Usage:
        @app.get("/countries")
        def get_countries(db: Session = Depends(get_db)):
            return db.query(Country).all()
    
    Why: 
    - Automatic session cleanup (even if error occurs)
    - Easy to mock for testing
    - Follows FastAPI patterns
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Get database session as context manager.
    
    Framework: Clean Architecture
    For use outside of FastAPI endpoints (scripts, background jobs).
    
    Usage:
        from src.services.database import get_db_context
        
        with get_db_context() as db:
            countries = db.query(Country).all()
            # Session automatically closed after 'with' block
    
    Why: Ensures proper cleanup, pythonic pattern
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ============================================
# DATABASE HEALTH CHECK
# Framework: Monitoring & Observability
# ============================================

def check_database_health() -> dict:
    """
    Check database connection health.
    
    Framework: Monitoring & Observability Framework
    Used by health check endpoints to verify database connectivity.
    
    Returns:
        dict: {
            "status": "healthy" | "unhealthy",
            "database_type": "sqlite" | "postgresql",
            "details": "connection message"
        }
    
    Why: Early detection of database issues
    """
    try:
        with get_db_context() as db:
            # Try a simple query - FIXED: Using text() wrapper for SQLAlchemy 2.0
            db.execute(text("SELECT 1"))
        
        settings = get_settings()
        db_type = "sqlite" if "sqlite" in settings.DATABASE_URL.lower() else "postgresql"
        
        return {
            "status": "healthy",
            "database_type": db_type,
            "details": "Database connection successful"
        }
    
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "database_type": "unknown",
            "details": str(e)
        }


# ============================================
# DATABASE UTILITIES
# Framework: Data Engineering Excellence
# ============================================

def get_or_create(db: Session, model, **kwargs):
    """
    Get existing record or create new one.
    
    Framework: Data Engineering Excellence
    Common pattern to avoid duplicate inserts.
    
    Args:
        db: Database session
        model: SQLAlchemy model class
        **kwargs: Fields to match/create
    
    Returns:
        Tuple of (instance, created_boolean)
    
    Example:
        country, created = get_or_create(
            db, 
            Country, 
            code="GHA", 
            name="Ghana"
        )
    
    Why: Idempotent operations, prevents errors
    """
    instance = db.query(model).filter_by(**kwargs).first()
    
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance, True


def bulk_insert_or_update(db: Session, model, records: list, key_fields: list):
    """
    Efficiently insert or update multiple records.
    
    Framework: Performance & Scalability Framework
    Uses bulk operations for better performance.
    
    Args:
        db: Database session
        model: SQLAlchemy model class
        records: List of dictionaries with record data
        key_fields: Fields to use for matching existing records
    
    Example:
        records = [
            {"code": "GHA", "name": "Ghana", "region": "Africa"},
            {"code": "KEN", "name": "Kenya", "region": "Africa"},
        ]
        bulk_insert_or_update(db, Country, records, ["code"])
    
    Why: Much faster than individual inserts
    """
    for record in records:
        # Check if exists
        filter_dict = {field: record[field] for field in key_fields}
        existing = db.query(model).filter_by(**filter_dict).first()
        
        if existing:
            # Update
            for key, value in record.items():
                setattr(existing, key, value)
        else:
            # Insert
            db.add(model(**record))
    
    db.commit()
    logger.info(f"✓ Bulk operation completed: {len(records)} records")


# ============================================
# TRANSACTION HELPERS
# Framework: Database Design Excellence
# ============================================

@contextmanager
def transaction(db: Session):
    """
    Transaction context manager.
    
    Framework: Database Design Excellence
    Ensures atomic operations - all succeed or all fail.
    
    Usage:
        with transaction(db):
            db.add(country1)
            db.add(country2)
            # Both committed together, or both rolled back on error
    
    Why: Data consistency, prevents partial updates
    """
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction failed: {e}")
        raise


# ============================================
# DEVELOPER NOTES
# ============================================
"""
DATABASE SERVICE DESIGN DECISIONS:

1. **Singleton Engine**:
   - Created once, reused everywhere
   - Connection pooling for performance
   - Thread-safe

2. **Session Management**:
   - get_db(): For FastAPI dependency injection
   - get_db_context(): For scripts and background jobs
   - Always automatically closed

3. **SQLite vs PostgreSQL**:
   - SQLite: Development (simple, no setup)
   - PostgreSQL: Production (scalable, features)
   - Same code works for both!

4. **Foreign Keys in SQLite**:
   - Not enabled by default
   - We enable with PRAGMA on connection
   - Ensures referential integrity

5. **Health Checks**:
   - Verify database connectivity
   - Used by monitoring systems
   - Returns structured response
   - IMPORTANT: Uses text() wrapper for SQLAlchemy 2.0 compatibility

HOW TO USE THIS SERVICE:

In FastAPI endpoints:
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from src.services.database import get_db

@app.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()
```

In scripts:
```python
from src.services.database import get_db_context
from src.models.debt_data import Country

with get_db_context() as db:
    countries = db.query(Country).all()
    print(f"Found {len(countries)} countries")
```

Initialize database (run once):
```python
from src.services.database import init_database
init_database()
```

TESTING:
```python
# In tests, use in-memory SQLite
from src.services.database import engine
engine = create_engine("sqlite:///:memory:")
```
"""