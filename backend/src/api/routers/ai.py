"""
Borrower's Forum Platform - AI Router
======================================

POST /api/v1/ai/strategy-brief — Generate negotiation strategy briefs
POST /api/v1/ai/chat — Chat with the debt restructuring advisor
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.api.dependencies import get_db
from src.api.auth import require_api_key
from src.models.debt_data import APIKey, Country, Precedent, DebtData
from src.services.ai_service import AIService, AIServiceError
from src.config.settings import get_settings

logger = logging.getLogger(__name__)

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


# ==========================================
# CHAT ENDPOINT
# ==========================================

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's question")
    history: List[ChatMessage] = Field(default=[], description="Previous messages for context")

class ChatResponse(BaseModel):
    reply: str
    sources_consulted: int


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with the debt restructuring advisor",
    description="Ask questions about debt restructuring, precedents, and climate clauses. **Requires API key.**",
)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(require_api_key),
):
    """Chat with the AI debt restructuring advisor."""

    anthropic_key = getattr(settings, "ANTHROPIC_API_KEY", None) or __import__("os").environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured.",
        )

    try:
        # Build database context for the AI
        countries = db.execute(select(Country).order_by(Country.name)).scalars().all()
        precedents = db.execute(
            select(Precedent).order_by(Precedent.year.desc())
        ).scalars().all()

        country_summary = ", ".join([f"{c.name} ({c.code})" for c in countries])

        precedent_lines = []
        for p in precedents:
            c = db.execute(select(Country).where(Country.id == p.country_id)).scalar_one_or_none()
            name = c.name if c else "Unknown"
            precedent_lines.append(
                f"- {name} ({p.year}): ${p.debt_amount_millions:,.0f}M, "
                f"{p.treatment_type}, {p.creditor_type}, "
                f"NPV reduction: {p.npv_reduction_percent or 'N/A'}%, "
                f"Climate clause: {p.includes_climate_clause or 'N/A'}"
                f"{' — ' + p.climate_notes if p.climate_notes else ''}"
            )

        system_prompt = f"""You are the Borrower's Forum AI Advisor — an expert on sovereign debt restructuring for developing nations. You have access to the platform's verified database.

DATABASE CONTEXT:
Countries covered: {country_summary}
Total precedents: {len(precedents)}

PRECEDENT DATABASE:
{chr(10).join(precedent_lines)}

GUIDELINES:
- Answer questions about debt restructuring, precedents, climate clauses, and negotiation strategy
- Always reference specific data from the precedent database when relevant
- Be concise — keep responses under 300 words
- Use markdown formatting: **bold** for emphasis, bullet points for lists
- If asked about a country not in the database, say so honestly
- Frame advice as "based on comparable precedents" not as definitive recommendations
- You are an analytical tool, not a legal or financial advisor"""

        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)

        messages = []
        for msg in request.history[-10:]:  # Keep last 10 messages for context
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": request.message})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=system_prompt,
            messages=messages,
        )

        return ChatResponse(
            reply=response.content[0].text,
            sources_consulted=len(precedents),
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}",
        )
