"""
Borrower's Forum Platform - AI Strategy Brief Router
=====================================================

POST /api/v1/ai/strategy-brief
Generates AI-powered negotiation strategy briefs using Claude.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.api.auth import require_api_key
from src.models.debt_data import APIKey
from src.services.ai_service import AIService, AIServiceError
from src.config.settings import get_settings

router = APIRouter(prefix="/ai", tags=["AI Strategy"])

settings = get_settings()


class StrategyBriefRequest(BaseModel):
    """Request body for generating a strategy brief."""
    country_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 3-letter country code",
        example="GHA",
    )
    debt_amount_usd: float = Field(
        ...,
        gt=0,
        description="Total debt amount in USD",
        example=50000000,
    )
    relief_percent: float = Field(
        default=30.0,
        ge=1,
        le=100,
        description="Target debt relief percentage",
        example=30.0,
    )


class StrategyBriefResponse(BaseModel):
    """Response containing the generated strategy brief."""
    country: dict
    parameters: dict
    brief: str
    precedents_used: int
    climate_precedents_used: int


@router.post(
    "/strategy-brief",
    response_model=StrategyBriefResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI negotiation strategy brief",
    description="""
    Generate a 1-page negotiation strategy brief using AI analysis.

    The brief includes:
    - Executive summary based on comparable cases
    - Relevant precedent analysis with specific terms achieved
    - Recommended negotiating positions backed by data
    - Climate clause recommendations from real precedents
    - Key talking points for negotiators

    **Requires API key.**
    """,
)
async def generate_strategy_brief(
    request: StrategyBriefRequest,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key),
):
    """Generate an AI-powered negotiation strategy brief."""

    # Check for Anthropic API key
    anthropic_key = getattr(settings, "ANTHROPIC_API_KEY", None) or __import__("os").environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. ANTHROPIC_API_KEY environment variable is required.",
        )

    try:
        service = AIService(db=db, anthropic_api_key=anthropic_key)
        result = service.generate_strategy_brief(
            country_code=request.country_code.upper(),
            debt_amount_usd=request.debt_amount_usd,
            relief_percent=request.relief_percent,
        )
        return result

    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    except Exception as e:
        print(f"Unexpected error generating strategy brief: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the strategy brief",
        )
