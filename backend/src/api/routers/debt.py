"""
Debt Calculator API Router

RESTful endpoints for calculating debt service vs development trade-offs.
Converts debt payments into equivalent doctors, schools, and climate projects.

Endpoints:
- POST /api/v1/debt/calculate - Calculate opportunity cost for single scenario
- POST /api/v1/debt/compare - Compare multiple debt scenarios
- POST /api/v1/debt/calculate-live - Calculate using live World Bank data
- GET /api/v1/debt/info - Get calculator methodology
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..auth import require_api_key
from ...services.debt_calculator import DebtCalculatorService, DebtCalculationError
from ...services.external_data import ExternalDataService
from ...models.debt_data import APIKey

# Router instance
router = APIRouter(
    prefix="/debt",
    tags=["Debt Calculator"],
    responses={
        401: {"description": "API key required"},
        404: {"description": "Country or data not found"},
        400: {"description": "Invalid request parameters"},
        422: {"description": "Validation error"}
    }
)


# Pydantic Models for Request/Response
class DebtCalculationRequest(BaseModel):
    """Request model for debt calculation"""
    country_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 3-letter country code (e.g., GHA, KEN, ZMB)",
        example="GHA"
    )
    year: int = Field(
        ...,
        ge=2015,
        le=2030,
        description="Year for the calculation (2015-2030)",
        example=2023
    )
    debt_amount_usd: float = Field(
        ...,
        gt=0,
        description="Debt service amount in USD",
        example=50000000  # 50 million USD
    )
    
    @validator('country_code')
    def validate_country_code(cls, v):
        """Ensure country code is uppercase"""
        return v.upper()
    
    class Config:
        schema_extra = {
            "example": {
                "country_code": "GHA",
                "year": 2023,
                "debt_amount_usd": 50000000
            }
        }


class ComparisonRequest(BaseModel):
    """Request model for comparing multiple scenarios"""
    country_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 3-letter country code",
        example="KEN"
    )
    year: int = Field(
        ...,
        ge=2015,
        le=2030,
        description="Year for calculations",
        example=2023
    )
    scenarios: List[float] = Field(
        ...,
        min_items=2,
        max_items=10,
        description="List of debt amounts to compare (2-10 scenarios)",
        example=[25000000, 50000000, 100000000]
    )
    
    @validator('country_code')
    def validate_country_code(cls, v):
        """Ensure country code is uppercase"""
        return v.upper()
    
    @validator('scenarios')
    def validate_scenarios(cls, v):
        """Ensure all scenarios are positive"""
        if any(amount <= 0 for amount in v):
            raise ValueError("All debt amounts must be greater than 0")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "country_code": "KEN",
                "year": 2023,
                "scenarios": [25000000, 50000000, 100000000]
            }
        }


class CountryInfo(BaseModel):
    """Country information in response"""
    code: str
    name: str
    region: Optional[str]
    income_level: Optional[str]
    population: Optional[int]
    gdp_usd_billions: Optional[float]
    climate_vulnerability_score: Optional[float]


class CalculationInfo(BaseModel):
    """Calculation metadata"""
    debt_amount_usd: float
    year: int
    data_quality_score: Optional[float]


class DoctorEquivalents(BaseModel):
    """Doctor employment equivalents"""
    annual_employment: float
    five_year_employment: float
    annual_salary_usd: float
    description: str


class SchoolEquivalents(BaseModel):
    """School construction equivalents"""
    number_of_schools: float
    cost_per_school_usd: float
    description: str


class ClimateEquivalents(BaseModel):
    """Climate project equivalents"""
    percentage_of_annual_budget: float
    annual_climate_budget_usd: float
    description: str


class Equivalents(BaseModel):
    """All calculated equivalents"""
    doctors: DoctorEquivalents
    schools: SchoolEquivalents
    climate_adaptation: ClimateEquivalents


class Context(BaseModel):
    """Economic context for the calculation"""
    annual_debt_service_usd: Optional[float]
    gdp_usd: Optional[float]
    government_revenue_usd: Optional[float]
    debt_to_gdp_ratio: Optional[float]
    debt_to_revenue_ratio: Optional[float]


class Sources(BaseModel):
    """Data sources"""
    debt_data: Optional[str]
    healthcare_data: Optional[str]
    education_data: Optional[str]
    climate_data: Optional[str]


class DebtCalculationResponse(BaseModel):
    """Response model for debt calculation"""
    country_info: CountryInfo
    calculation: CalculationInfo
    equivalents: Equivalents
    context: Context
    sources: Sources
    
    class Config:
        schema_extra = {
            "example": {
                "country_info": {
                    "code": "GHA",
                    "name": "Ghana",
                    "region": "Sub-Saharan Africa",
                    "income_level": "LMIC",
                    "population": 33000000,
                    "gdp_usd_billions": 77.0,
                    "climate_vulnerability_score": 68.5
                },
                "calculation": {
                    "debt_amount_usd": 50000000.0,
                    "year": 2023,
                    "data_quality_score": 85.0
                },
                "equivalents": {
                    "doctors": {
                        "annual_employment": 2500,
                        "five_year_employment": 500,
                        "annual_salary_usd": 20000,
                        "description": "Could employ 2500 doctors for 1 year or 500 doctors for 5 years"
                    },
                    "schools": {
                        "number_of_schools": 125,
                        "cost_per_school_usd": 400000,
                        "description": "Could build 125 schools"
                    },
                    "climate_adaptation": {
                        "percentage_of_annual_budget": 25.0,
                        "annual_climate_budget_usd": 200000000,
                        "description": "Represents 25.0% of annual climate adaptation budget"
                    }
                },
                "context": {
                    "annual_debt_service_usd": 2500000000,
                    "gdp_usd": 77000000000,
                    "government_revenue_usd": 15000000000,
                    "debt_to_gdp_ratio": 0.06,
                    "debt_to_revenue_ratio": 0.33
                },
                "sources": {
                    "debt_data": "IMF World Economic Outlook 2023",
                    "healthcare_data": "WHO Global Health Expenditure Database",
                    "education_data": "UNESCO Institute for Statistics",
                    "climate_data": "UNFCCC National Communications"
                }
            }
        }


# API Endpoints (Protected with API Key)
@router.post(
    "/calculate",
    response_model=DebtCalculationResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate debt opportunity cost",
    description="""
    Calculate the opportunity cost of debt service payments in development terms.
    **Requires API key.**
    
    This endpoint converts a debt service amount into equivalent:
    - Number of doctors that could be employed (1-year and 5-year contracts)
    - Number of schools that could be built
    - Percentage of annual climate adaptation budget
    
    The calculation uses country-specific salary and cost data from the specified year.
    """,
    response_description="Calculated opportunity costs and equivalents"
)
async def calculate_debt_opportunity_cost(
    request: DebtCalculationRequest,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key)
) -> DebtCalculationResponse:
    """
    Calculate debt service opportunity cost.
    
    Requires: Valid API key with read permission.
    """
    try:
        calculator = DebtCalculatorService(db)
        result = calculator.calculate_opportunity_cost(
            country_code=request.country_code,
            year=request.year,
            debt_amount_usd=request.debt_amount_usd
        )
        return result
    
    except DebtCalculationError as e:
        error_message = str(e)
        
        if "not found" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
    
    except Exception as e:
        print(f"Unexpected error in debt calculation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during calculation"
        )


@router.post(
    "/calculate-live",
    status_code=status.HTTP_200_OK,
    summary="Calculate with live World Bank data",
    description="""
    Calculate opportunity cost using real-time World Bank data.
    **Requires API key.**
    
    Unlike /calculate which uses stored data, this endpoint fetches
    live economic indicators from the World Bank API.
    
    Supports any country with World Bank data (most countries worldwide).
    """,
    response_description="Calculated opportunity costs with live data"
)
async def calculate_with_live_data(
    country_code: str = Query(..., min_length=3, max_length=3, description="ISO 3-letter country code"),
    year: int = Query(2022, ge=2000, le=2024, description="Year for data"),
    debt_amount_usd: float = Query(..., gt=0, description="Debt amount in USD"),
    api_key: APIKey = Depends(require_api_key)
):
    """
    Calculate debt opportunity cost using live World Bank data.
    
    Requires: Valid API key with read permission.
    """
    try:
        # Fetch live data
        service = ExternalDataService()
        live_data = service.get_country_economic_data(country_code.upper(), year)
        
        if not live_data.get("country"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country '{country_code}' not found in World Bank database"
            )
        
        country = live_data["country"]
        indicators = live_data["economic_indicators"]
        
        # Get salary and cost estimates based on income level
        income_level = country.get("income_level", "LMC")
        
        # Estimated costs by income level (USD)
        cost_estimates = {
            "LIC": {"doctor_salary": 8000, "school_cost": 200000, "climate_budget_pct": 2.0},
            "LMC": {"doctor_salary": 15000, "school_cost": 350000, "climate_budget_pct": 1.5},
            "UMC": {"doctor_salary": 30000, "school_cost": 500000, "climate_budget_pct": 1.0},
            "HIC": {"doctor_salary": 80000, "school_cost": 1000000, "climate_budget_pct": 0.5},
        }
        
        estimates = cost_estimates.get(income_level, cost_estimates["LMC"])
        
        doctor_salary = estimates["doctor_salary"]
        school_cost = estimates["school_cost"]
        gdp = indicators.get("gdp_usd") or 0
        climate_budget = gdp * (estimates["climate_budget_pct"] / 100) if gdp else 0
        
        # Calculate equivalents
        doctors_1yr = debt_amount_usd / doctor_salary if doctor_salary else 0
        doctors_5yr = doctors_1yr / 5
        schools = debt_amount_usd / school_cost if school_cost else 0
        climate_pct = (debt_amount_usd / climate_budget * 100) if climate_budget else 0
        
        return {
            "data_source": "World Bank Open Data API (Live)",
            "country_info": {
                "code": country.get("code"),
                "name": country.get("name"),
                "region": country.get("region"),
                "income_level": income_level,
                "capital": country.get("capital")
            },
            "calculation": {
                "debt_amount_usd": debt_amount_usd,
                "year": year
            },
            "live_indicators": {
                "gdp_usd": indicators.get("gdp_usd"),
                "population": indicators.get("population"),
                "external_debt_usd": indicators.get("external_debt_usd"),
                "debt_service_usd": indicators.get("debt_service_usd"),
                "government_revenue_usd": indicators.get("government_revenue_usd")
            },
            "equivalents": {
                "doctors": {
                    "annual_employment": round(doctors_1yr),
                    "five_year_employment": round(doctors_5yr),
                    "estimated_salary_usd": doctor_salary,
                    "description": f"Could employ {round(doctors_1yr):,} doctors for 1 year or {round(doctors_5yr):,} doctors for 5 years"
                },
                "schools": {
                    "number_of_schools": round(schools),
                    "estimated_cost_usd": school_cost,
                    "description": f"Could build {round(schools):,} schools"
                },
                "climate_adaptation": {
                    "percentage_of_annual_budget": round(climate_pct, 1),
                    "estimated_annual_budget_usd": round(climate_budget),
                    "description": f"Represents {round(climate_pct, 1)}% of estimated annual climate adaptation budget"
                }
            },
            "methodology_notes": {
                "salary_estimates": "Based on World Bank income classification",
                "school_costs": "Regional average construction costs",
                "climate_budget": f"Estimated at {estimates['climate_budget_pct']}% of GDP for {income_level} countries"
            },
            "metadata": live_data.get("metadata")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating with live data: {str(e)}"
        )


@router.post(
    "/compare",
    status_code=status.HTTP_200_OK,
    summary="Compare multiple debt scenarios",
    description="""
    Compare the opportunity costs of multiple debt service amounts.
    **Requires API key.**
    
    This endpoint allows you to analyze different debt scenarios side-by-side,
    showing how different payment amounts translate to development resources.
    
    Useful for:
    - Analyzing negotiation options
    - Understanding the impact of debt relief
    - Comparing restructuring proposals
    """,
    response_description="Comparative analysis of scenarios"
)
async def compare_debt_scenarios(
    request: ComparisonRequest,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key)
):
    """
    Compare multiple debt scenarios.
    
    Requires: Valid API key with read permission.
    """
    try:
        calculator = DebtCalculatorService(db)
        result = calculator.compare_scenarios(
            country_code=request.country_code,
            year=request.year,
            scenarios=request.scenarios
        )
        return result
    
    except DebtCalculationError as e:
        error_message = str(e)
        
        if "not found" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
    
    except Exception as e:
        print(f"Unexpected error in scenario comparison: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during comparison"
        )


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    summary="Get calculator information",
    description="Get information about the debt calculator including methodology and data sources. **Requires API key.**",
    response_description="Calculator metadata and methodology"
)
async def get_calculator_info(
    api_key: APIKey = Depends(require_api_key)
):
    """
    Get debt calculator information and methodology.
    
    Requires: Valid API key with read permission.
    """
    return {
        "name": "Debt Opportunity Cost Calculator",
        "version": "1.0.0",
        "description": "Converts debt service payments into equivalent development resources",
        "endpoints": {
            "/calculate": "Uses stored country data (5 countries)",
            "/calculate-live": "Uses live World Bank data (190+ countries)"
        },
        "methodology": {
            "doctors": {
                "calculation": "Debt amount / (Annual doctor salary × Years)",
                "assumptions": [
                    "5-year employment contracts for long-term employment",
                    "1-year contracts for annual employment",
                    "Salaries based on country-specific healthcare worker compensation"
                ]
            },
            "schools": {
                "calculation": "Debt amount / Cost per school",
                "assumptions": [
                    "One-time construction cost",
                    "Includes basic infrastructure and equipment",
                    "Costs vary by country income level"
                ]
            },
            "climate_adaptation": {
                "calculation": "(Debt amount / Annual climate budget) × 100",
                "assumptions": [
                    "Percentage of total annual climate adaptation budget",
                    "Budget includes resilience and mitigation projects"
                ]
            }
        },
        "data_sources": {
            "stored_data": [
                "IMF World Economic Outlook",
                "World Bank Development Indicators",
                "WHO Global Health Expenditure Database",
                "UNESCO Institute for Statistics",
                "UNFCCC National Communications"
            ],
            "live_data": [
                "World Bank Open Data API (real-time)"
            ]
        },
        "supported_years": "2000-2024 (live), 2015-2030 (stored)",
        "currency": "USD"
    }