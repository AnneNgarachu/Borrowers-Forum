"""
Borrower's Forum Platform - Database Models
============================================

Framework Applied: database_design_excellence.md
Principle: Progressive schema design with proper relationships
Why: Clean data structure makes queries easy and prevents data integrity issues
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Country(Base):
    """
    Country master data table.
    
    Framework: Database Design Excellence
    - UUID primary keys (better for distributed systems)
    - Proper constraints (unique, not null)
    - Timestamps for audit trail
    - Clear relationships
    
    Why: Single source of truth for country data, prevents duplication
    """
    __tablename__ = "countries"
    
    # Primary key - using string to store UUID
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Core fields
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True)  # ISO 3-letter code
    
    # Classification
    region = Column(String(50))  # e.g., "Sub-Saharan Africa", "South Asia"
    income_level = Column(String(10))  # LIC, LMIC, UMIC, HIC
    
    # Optional metadata
    population = Column(Integer)
    gdp_usd_billions = Column(Float)
    climate_vulnerability_score = Column(Float)  # ND-GAIN index (0-100)
    
    # Audit timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    debt_data = relationship("DebtData", back_populates="country", cascade="all, delete-orphan")
    precedents = relationship("Precedent", back_populates="country", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Country(code='{self.code}', name='{self.name}')>"


class DebtData(Base):
    """
    Annual debt service and development indicators.
    
    Framework: Database Design Excellence
    - One country, many debt records (1:many relationship)
    - Unique constraint prevents duplicate year entries
    - Check constraints ensure data quality
    - Indexed foreign keys for query performance
    
    Why: Track debt vs development trade-offs over time
    """
    __tablename__ = "debt_data"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key
    country_id = Column(String(36), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Time dimension
    year = Column(Integer, nullable=False, index=True)
    
    # Financial data (in millions USD unless specified)
    debt_service_usd_millions = Column(Float, nullable=False)
    gdp_usd_millions = Column(Float)
    government_revenue_usd_millions = Column(Float)
    
    # Development indicators
    healthcare_salary_usd_thousands = Column(Float)  # Average annual salary
    school_cost_usd_thousands = Column(Float)  # Primary school construction
    climate_budget_usd_millions = Column(Float)  # Annual climate adaptation budget
    
    # Data quality metadata
    source_debt = Column(String(500), nullable=False)
    source_healthcare = Column(String(500))
    source_school = Column(String(500))
    source_climate = Column(String(500))
    
    data_quality_score = Column(Float)  # 0-100, based on source reliability
    notes = Column(String(2000))
    
    # Audit timestamps
    collected_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    country = relationship("Country", back_populates="debt_data")
    
    # Constraints
    __table_args__ = (
        # Only one record per country per year
        UniqueConstraint('country_id', 'year', name='unique_country_year'),
        # Reasonable value ranges
        CheckConstraint('debt_service_usd_millions > 0', name='positive_debt_service'),
        CheckConstraint('year >= 2015 AND year <= 2030', name='valid_year_range'),
    )
    
    def __repr__(self):
        return f"<DebtData(country_id='{self.country_id}', year={self.year})>"


class Precedent(Base):
    """
    Debt restructuring precedents.
    
    Framework: Database Design Excellence
    - Links to country via foreign key
    - Structured fields for easy filtering
    - Comprehensive metadata for comparisons
    
    Why: Enable precedent search and similarity analysis
    """
    __tablename__ = "precedents"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key
    country_id = Column(String(36), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Basic information
    year = Column(Integer, nullable=False, index=True)
    debt_amount_millions = Column(Float, nullable=False)
    
    # Classification (for filtering and comparison)
    creditor_type = Column(String(50), index=True)  # Official, Private, Mixed, Paris Club, etc.
    treatment_type = Column(String(50), index=True)  # Flow, Stock, HIPC, Common Framework, etc.
    
    # Terms and outcomes
    duration_months = Column(Integer)
    npv_reduction_percent = Column(Float)  # Net Present Value reduction
    grace_period_months = Column(Integer)
    interest_rate_percent = Column(Float)
    
    # Free-text details
    terms_summary = Column(String(2000))
    conditions = Column(String(2000))
    outcomes = Column(String(2000))
    
    # Climate linkage (for our specific use case)
    includes_climate_clause = Column(String(10))  # Yes, No, Partial
    climate_notes = Column(String(1000))
    
    # Sources and documentation
    source_url = Column(String(500))
    source_document = Column(String(500))
    
    # Metadata
    notes = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    country = relationship("Country", back_populates="precedents")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('debt_amount_millions > 0', name='positive_debt_amount'),
        CheckConstraint('year >= 1980 AND year <= 2030', name='valid_precedent_year'),
    )
    
    def __repr__(self):
        return f"<Precedent(country_id='{self.country_id}', year={self.year}, type='{self.treatment_type}')>"


# ============================================
# DEVELOPER NOTES
# ============================================
"""
DATABASE SCHEMA DESIGN DECISIONS:

1. **UUID Primary Keys**:
   - Why: Better for distributed systems, no collisions
   - Stored as String(36) for SQLite compatibility
   - In production PostgreSQL, use UUID type

2. **Timestamps**:
   - created_at: When record was created
   - updated_at: When record was last modified
   - Auto-managed by SQLAlchemy

3. **Relationships**:
   - One country → Many debt records
   - One country → Many precedents
   - Cascade delete: If country deleted, related records also deleted

4. **Constraints**:
   - Unique: Prevents duplicate data
   - Check: Ensures data quality at database level
   - Not Null: Required fields

5. **Indexes**:
   - Foreign keys: Faster joins
   - Frequently queried fields: Faster filtering (country code, year)

6. **Data Types**:
   - String with max length: Predictable storage
   - Float: Decimal precision for financial data
   - Integer: Whole numbers (years, months)
   - DateTime: Timezone-aware timestamps

HOW TO EXTEND THIS SCHEMA:

Adding a new field to existing table:
1. Add column to model class
2. Create migration: `alembic revision --autogenerate -m "Add new_field"`
3. Apply migration: `alembic upgrade head`

Adding a new table:
1. Create new model class
2. Define relationships if needed
3. Create migration
4. Apply migration

MIGRATION EXAMPLE (for later):
```bash
# After changing models
alembic revision --autogenerate -m "Add climate vulnerability field"
alembic upgrade head
```
"""