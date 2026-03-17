"""
Borrower's Forum Platform - Countries Router
=============================================

Framework Applied: api_design_integration_framework.md
Principle: RESTful API design with proper validation and responses
Why: Clean, predictable API that follows industry standards
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from src.services.database import get_db
from src.models.debt_data import Country, APIKey
from src.api.auth import require_api_key, require_write_permission

# ============================================
# PYDANTIC MODELS (Request/Response Schemas)
# Framework: API Design & Integration Framework
# ============================================

class CountryResponse(BaseModel):
    """
    Country response model.
    
    Framework: API Design Framework
    - Clear field types
    - Descriptive field names
    - Example values for documentation
    
    Why: Type safety, auto-generated docs, clear contracts
    """
    id: str = Field(..., description="Unique country identifier")
    name: str = Field(..., description="Country name", example="Ghana")
    code: str = Field(..., description="ISO 3-letter country code", example="GHA")
    region: Optional[str] = Field(None, description="Geographic region", example="Sub-Saharan Africa")
    income_level: Optional[str] = Field(None, description="Income classification", example="LMIC")
    population: Optional[int] = Field(None, description="Population count", example=31072940)
    gdp_usd_billions: Optional[float] = Field(None, description="GDP in billions USD", example=72.8)
    climate_vulnerability_score: Optional[float] = Field(None, description="Climate vulnerability (0-100)", example=45.2)
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True  # Allows creation from ORM models (Pydantic V1)


class CountryListResponse(BaseModel):
    """
    Country list response with metadata.
    
    Framework: API Design Framework
    Why: Consistent response format, easy pagination later
    """
    total: int = Field(..., description="Total number of countries")
    countries: List[CountryResponse] = Field(..., description="List of countries")


class CountryCreate(BaseModel):
    """
    Country creation request model.
    
    Framework: Data Engineering Excellence
    Why: Validate input before database insertion
    """
    name: str = Field(..., min_length=2, max_length=100, description="Country name")
    code: str = Field(..., min_length=3, max_length=3, description="ISO 3-letter code")
    region: Optional[str] = Field(None, max_length=50)
    income_level: Optional[str] = Field(None, max_length=10)
    population: Optional[int] = Field(None, gt=0)
    gdp_usd_billions: Optional[float] = Field(None, gt=0)
    climate_vulnerability_score: Optional[float] = Field(None, ge=0, le=100)


# ============================================
# CREATE ROUTER
# Framework: Clean Architecture
# ============================================

router = APIRouter()


# ============================================
# ENDPOINTS (Protected with API Key)
# Framework: API Design & Integration Framework
# ============================================

@router.get(
    "/countries",
    response_model=CountryListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all countries",
    description="Retrieve a list of all countries in the database with optional filtering. **Requires API key.**",
    responses={
        200: {"description": "List of countries retrieved successfully"},
        401: {"description": "API key required"},
        500: {"description": "Internal server error"}
    }
)
async def list_countries(
    region: Optional[str] = Query(None, description="Filter by region"),
    income_level: Optional[str] = Query(None, description="Filter by income level"),
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key)  # 🔒 Protected
):
    """
    List all countries.
    
    Framework: API Design Framework
    - RESTful endpoint naming
    - Query parameters for filtering
    - Proper HTTP status codes
    
    Requires: Valid API key with read permission.
    
    Args:
        region: Optional region filter
        income_level: Optional income level filter
        db: Database session (injected by FastAPI)
        api_key: Validated API key (injected by FastAPI)
    
    Returns:
        CountryListResponse: List of countries with metadata
    
    Example:
        GET /api/v1/countries
        GET /api/v1/countries?region=Sub-Saharan%20Africa
        GET /api/v1/countries?income_level=LMIC
    """
    try:
        # Build query
        query = db.query(Country)
        
        # Apply filters if provided
        if region:
            query = query.filter(Country.region == region)
        if income_level:
            query = query.filter(Country.income_level == income_level)
        
        # Execute query
        countries = query.order_by(Country.name).all()
        
        return CountryListResponse(
            total=len(countries),
            countries=countries
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving countries: {str(e)}"
        )


@router.get(
    "/countries/{country_code}",
    response_model=CountryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get country by code",
    description="Retrieve detailed information about a specific country. **Requires API key.**",
    responses={
        200: {"description": "Country found"},
        401: {"description": "API key required"},
        404: {"description": "Country not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_country(
    country_code: str,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key)  # 🔒 Protected
):
    """
    Get country by ISO code.
    
    Framework: API Design Framework
    - RESTful resource access
    - Proper 404 handling
    - Clear error messages
    
    Requires: Valid API key with read permission.
    
    Args:
        country_code: ISO 3-letter country code (e.g., "GHA")
        db: Database session (injected by FastAPI)
        api_key: Validated API key (injected by FastAPI)
    
    Returns:
        CountryResponse: Country details
    
    Raises:
        HTTPException: 404 if country not found
    
    Example:
        GET /api/v1/countries/GHA
        GET /api/v1/countries/KEN
    """
    try:
        # Query by code (case-insensitive)
        country = db.query(Country).filter(
            Country.code == country_code.upper()
        ).first()
        
        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country with code '{country_code}' not found"
            )
        
        return country
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving country: {str(e)}"
        )


@router.post(
    "/countries",
    response_model=CountryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new country",
    description="Add a new country to the database. **Requires API key with write permission.**",
    responses={
        201: {"description": "Country created successfully"},
        401: {"description": "API key required"},
        403: {"description": "Write permission required"},
        409: {"description": "Country already exists"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)
async def create_country(
    country_data: CountryCreate,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_write_permission)  # 🔒 Requires write permission
):
    """
    Create a new country.
    
    Framework: API Design Framework + Data Engineering Excellence
    - Proper POST semantics (201 Created)
    - Duplicate detection
    - Input validation via Pydantic
    
    Requires: Valid API key with write permission (read_write or admin).
    
    Args:
        country_data: Country data to create
        db: Database session (injected by FastAPI)
        api_key: Validated API key with write permission (injected by FastAPI)
    
    Returns:
        CountryResponse: Created country
    
    Raises:
        HTTPException: 409 if country already exists
    
    Example:
        POST /api/v1/countries
        {
          "name": "Ghana",
          "code": "GHA",
          "region": "Sub-Saharan Africa",
          "income_level": "LMIC"
        }
    """
    try:
        # Check if country already exists
        existing = db.query(Country).filter(
            (Country.code == country_data.code.upper()) |
            (Country.name == country_data.name)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Country with code '{country_data.code}' or name '{country_data.name}' already exists"
            )
        
        # Create new country
        new_country = Country(
            name=country_data.name,
            code=country_data.code.upper(),
            region=country_data.region,
            income_level=country_data.income_level,
            population=country_data.population,
            gdp_usd_billions=country_data.gdp_usd_billions,
            climate_vulnerability_score=country_data.climate_vulnerability_score
        )
        
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        
        return new_country
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating country: {str(e)}"
        )


# ============================================
# DEVELOPER NOTES
# ============================================
"""
COUNTRIES ROUTER DESIGN DECISIONS:

1. **RESTful Design**:
   - GET /countries → List all
   - GET /countries/{code} → Get one
   - POST /countries → Create new
   
2. **Response Models**:
   - Pydantic models ensure type safety
   - Auto-generate API documentation
   - Consistent response format

3. **Error Handling**:
   - 404: Resource not found
   - 409: Duplicate/conflict
   - 422: Validation error (automatic from Pydantic)
   - 500: Server error

4. **Filtering**:
   - Query parameters for flexible filtering
   - Easy to extend with more filters

5. **Database Session**:
   - Injected via Depends(get_db)
   - Automatically closed after request
   - Transaction management

6. **Authentication** (Phase 7):
   - All endpoints require API key
   - GET endpoints: require_api_key (read permission)
   - POST endpoint: require_write_permission (write permission)
   - Rate limiting applied automatically

HOW TO EXTEND:

Add more endpoints:
```python
@router.put("/countries/{country_code}")
async def update_country(...):
    # Update logic
    pass

@router.delete("/countries/{country_code}")
async def delete_country(...):
    # Delete logic
    pass
```

Add more filters:
```python
@router.get("/countries")
async def list_countries(
    region: Optional[str] = None,
    min_population: Optional[int] = None,  # New filter
    max_gdp: Optional[float] = None,  # New filter
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key)
):
    query = db.query(Country)
    if min_population:
        query = query.filter(Country.population >= min_population)
    # ...
```
"""