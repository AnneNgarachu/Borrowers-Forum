"""
Live Data API Router

Fetches real-time economic data from World Bank and IMF APIs.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from src.api.auth import require_api_key
from src.models.debt_data import APIKey
from src.services.external_data import ExternalDataService, ExternalDataError


router = APIRouter(
    prefix="/live",
    tags=["Live Data"],
    responses={
        401: {"description": "API key required"},
        404: {"description": "Country not found"},
        500: {"description": "External API error"}
    }
)


@router.get(
    "/economic/{country_code}",
    status_code=status.HTTP_200_OK,
    summary="Get live economic data",
    description="""
    Fetch real-time economic data from World Bank API.
    
    Returns:
    - GDP (current US$)
    - Population
    - External debt
    - Debt service payments
    - Government revenue
    
    **Requires API key.**
    """,
    response_description="Live economic indicators"
)
async def get_live_economic_data(
    country_code: str,
    year: Optional[int] = Query(
        None,
        description="Year for data (default: most recent)",
        ge=2000,
        le=2024
    ),
    api_key: APIKey = Depends(require_api_key)
):
    """
    Get live economic data for a country.
    
    Requires: Valid API key with read permission.
    """
    try:
        service = ExternalDataService()
        data = service.get_country_economic_data(
            country_code=country_code.upper(),
            year=year
        )
        
        # Check if we got valid data
        if not data.get("country"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country '{country_code}' not found in World Bank database"
            )
        
        return data
        
    except ExternalDataError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching external data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/debt/{country_code}",
    status_code=status.HTTP_200_OK,
    summary="Get live debt data",
    description="""
    Fetch real-time debt data formatted for the debt calculator.
    
    Returns debt service data in millions USD, compatible with
    the debt calculator endpoints.
    
    **Requires API key.**
    """,
    response_description="Live debt data for calculator"
)
async def get_live_debt_data(
    country_code: str,
    year: int = Query(
        2022,
        description="Year for data",
        ge=2000,
        le=2024
    ),
    api_key: APIKey = Depends(require_api_key)
):
    """
    Get live debt data for debt calculator.
    
    Requires: Valid API key with read permission.
    """
    try:
        service = ExternalDataService()
        data = service.get_live_debt_data(
            country_code=country_code.upper(),
            year=year
        )
        
        return data
        
    except ExternalDataError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching external data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/countries",
    status_code=status.HTTP_200_OK,
    summary="Get supported countries",
    description="List of countries with available World Bank data. **Requires API key.**",
    response_description="List of supported country codes"
)
async def get_supported_countries(
    api_key: APIKey = Depends(require_api_key)
):
    """
    Get list of commonly used country codes.
    
    Requires: Valid API key with read permission.
    """
    return {
        "message": "World Bank API supports most ISO 3-letter country codes",
        "examples": [
            {"code": "GHA", "name": "Ghana"},
            {"code": "KEN", "name": "Kenya"},
            {"code": "ZMB", "name": "Zambia"},
            {"code": "PAK", "name": "Pakistan"},
            {"code": "BGD", "name": "Bangladesh"},
            {"code": "NGA", "name": "Nigeria"},
            {"code": "ETH", "name": "Ethiopia"},
            {"code": "TZA", "name": "Tanzania"},
            {"code": "UGA", "name": "Uganda"},
            {"code": "ZAF", "name": "South Africa"},
        ],
        "note": "Try any ISO 3-letter country code - most countries are supported"
    }