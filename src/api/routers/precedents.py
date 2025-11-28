"""
Precedents Search API Router

RESTful endpoints for searching historical debt restructuring precedents.
Helps countries find comparable cases for negotiation reference.

Endpoints:
- GET /api/v1/precedents - Search with filters
- GET /api/v1/precedents/similar - Find similar cases
- GET /api/v1/precedents/stats - Get statistics
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.services.precedent_search import PrecedentSearchService, PrecedentSearchError


# Router instance
router = APIRouter(
    prefix="/precedents",
    tags=["Precedents Search"],
    responses={
        404: {"description": "Precedent or country not found"},
        400: {"description": "Invalid request parameters"}
    }
)


# Response Models
class CountryInfo(BaseModel):
    """Country information in precedent"""
    code: str
    name: str
    region: Optional[str]
    income_level: Optional[str]


class PrecedentResponse(BaseModel):
    """Individual precedent details"""
    id: str
    country: CountryInfo
    year: int
    debt_amount_millions: float
    creditor_type: Optional[str]
    treatment_type: Optional[str]
    duration_months: Optional[int]
    npv_reduction_percent: Optional[float]
    grace_period_months: Optional[int]
    interest_rate_percent: Optional[float]
    terms_summary: Optional[str]
    conditions: Optional[str]
    outcomes: Optional[str]
    includes_climate_clause: Optional[str]
    climate_notes: Optional[str]
    source_url: Optional[str]
    source_document: Optional[str]


class ScoreBreakdown(BaseModel):
    """Similarity score breakdown"""
    regional_match: bool
    income_level_match: bool
    climate_vulnerability_similarity: Optional[float]
    debt_amount_ratio: float
    years_ago: int


class SimilarPrecedent(BaseModel):
    """Precedent with similarity score"""
    id: str
    similarity_score: float
    score_breakdown: ScoreBreakdown
    country: CountryInfo
    year: int
    debt_amount_millions: float
    creditor_type: Optional[str]
    treatment_type: Optional[str]
    npv_reduction_percent: Optional[float]
    grace_period_months: Optional[int]
    terms_summary: Optional[str]
    outcomes: Optional[str]
    includes_climate_clause: Optional[str]


# API Endpoints
@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Search precedents",
    description="""
    Search historical debt restructuring precedents with multiple filters.
    
    Filters available:
    - **country_code**: Filter by specific country (ISO 3-letter code)
    - **year_start** / **year_end**: Filter by year range
    - **creditor_type**: Official, Private, Mixed, Paris Club
    - **treatment_type**: Flow, Stock, HIPC, Common Framework
    - **includes_climate**: Filter by climate clause presence
    - **min_debt_amount** / **max_debt_amount**: Filter by debt amount range
    
    Results are paginated and ordered by most recent first.
    """,
    response_description="List of precedents matching filters"
)
async def search_precedents(
    country_code: Optional[str] = Query(
        None,
        description="ISO 3-letter country code (e.g., GHA, KEN)",
        min_length=3,
        max_length=3
    ),
    year_start: Optional[int] = Query(
        None,
        description="Start of year range (inclusive)",
        ge=1980,
        le=2030
    ),
    year_end: Optional[int] = Query(
        None,
        description="End of year range (inclusive)",
        ge=1980,
        le=2030
    ),
    creditor_type: Optional[str] = Query(
        None,
        description="Type of creditor"
    ),
    treatment_type: Optional[str] = Query(
        None,
        description="Type of debt treatment"
    ),
    includes_climate: Optional[bool] = Query(
        None,
        description="Filter by climate clause presence"
    ),
    min_debt_amount: Optional[float] = Query(
        None,
        description="Minimum debt amount in millions USD",
        ge=0
    ),
    max_debt_amount: Optional[float] = Query(
        None,
        description="Maximum debt amount in millions USD",
        ge=0
    ),
    limit: int = Query(
        20,
        description="Maximum number of results",
        ge=1,
        le=100
    ),
    offset: int = Query(
        0,
        description="Number of results to skip (for pagination)",
        ge=0
    ),
    db: Session = Depends(get_db)
):
    """
    Search precedents with filters.
    
    Args:
        country_code: Filter by country
        year_start: Start of year range
        year_end: End of year range
        creditor_type: Type of creditor
        treatment_type: Type of treatment
        includes_climate: Filter by climate clause
        min_debt_amount: Minimum debt amount
        max_debt_amount: Maximum debt amount
        limit: Results per page
        offset: Pagination offset
        db: Database session (injected)
    
    Returns:
        Paginated list of precedents with filters applied
    """
    try:
        service = PrecedentSearchService(db)
        
        # Validate year range
        if year_start and year_end and year_start > year_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="year_start must be less than or equal to year_end"
            )
        
        # Validate debt amount range
        if min_debt_amount and max_debt_amount and min_debt_amount > max_debt_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_debt_amount must be less than or equal to max_debt_amount"
            )
        
        result = service.search_precedents(
            country_code=country_code,
            year_start=year_start,
            year_end=year_end,
            creditor_type=creditor_type,
            treatment_type=treatment_type,
            includes_climate=includes_climate,
            min_debt_amount=min_debt_amount,
            max_debt_amount=max_debt_amount,
            limit=limit,
            offset=offset
        )
        
        return result
    
    except PrecedentSearchError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        print(f"Unexpected error in precedent search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during search"
        )


@router.get(
    "/similar",
    status_code=status.HTTP_200_OK,
    summary="Find similar precedents",
    description="""
    Find precedents similar to a given country and debt situation.
    
    Uses intelligent similarity scoring based on:
    - **Regional similarity**: Same region = +30 points
    - **Income level**: Same income level = +25 points
    - **Climate vulnerability**: Similar scores = up to +15 points
    - **Debt amount**: Similar debt size = up to +20 points
    - **Recency**: More recent cases = up to +10 points
    
    Results are ranked by similarity score (0-100).
    """,
    response_description="Ranked list of similar precedents"
)
async def find_similar_precedents(
    country_code: str = Query(
        ...,
        description="ISO 3-letter country code",
        min_length=3,
        max_length=3
    ),
    debt_amount_millions: float = Query(
        ...,
        description="Debt amount in millions USD",
        gt=0
    ),
    limit: int = Query(
        10,
        description="Maximum number of results",
        ge=1,
        le=50
    ),
    db: Session = Depends(get_db)
):
    """
    Find similar precedents using AI-powered similarity matching.
    
    Args:
        country_code: Reference country code
        debt_amount_millions: Reference debt amount
        limit: Maximum results
        db: Database session (injected)
    
    Returns:
        Ranked list of similar precedents with similarity scores
    """
    try:
        service = PrecedentSearchService(db)
        result = service.find_similar_precedents(
            country_code=country_code.upper(),
            debt_amount_millions=debt_amount_millions,
            limit=limit
        )
        return result
    
    except PrecedentSearchError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        print(f"Unexpected error in similarity search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during similarity search"
        )


@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    summary="Get precedent statistics",
    description="Get statistics about available precedents in the database",
    response_description="Precedent statistics by category"
)
async def get_precedent_statistics(
    db: Session = Depends(get_db)
):
    """
    Get statistics about available precedents.
    
    Returns counts by:
    - Total precedents
    - Creditor type
    - Treatment type
    - Climate clause presence
    - Year range
    
    Args:
        db: Database session (injected)
    
    Returns:
        Statistics dictionary
    """
    try:
        service = PrecedentSearchService(db)
        stats = service.get_precedent_statistics()
        return stats
    
    except Exception as e:
        print(f"Unexpected error getting statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving statistics"
        )