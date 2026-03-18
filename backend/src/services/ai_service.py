"""
Borrower's Forum Platform - AI Strategy Brief Service
======================================================

Generates negotiation strategy briefs using Claude API,
informed by similar precedents and country economic data.
"""

import logging
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.debt_data import Country, Precedent, DebtData
from src.services.precedent_search import PrecedentSearchService

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Custom exception for AI service errors."""
    pass


class AIService:
    """
    Service for generating AI-powered negotiation strategy briefs.

    Flow:
    1. Look up country data from database
    2. Find similar precedents via PrecedentSearchService
    3. Build context prompt with real data
    4. Call Claude API to generate strategy brief
    5. Return structured brief
    """

    def __init__(self, db: Session, anthropic_api_key: str):
        self.db = db
        self.api_key = anthropic_api_key

    def generate_strategy_brief(
        self,
        country_code: str,
        debt_amount_usd: float,
        relief_percent: float = 30.0,
    ) -> Dict:
        """
        Generate a negotiation strategy brief for a country.

        Args:
            country_code: ISO 3-letter country code
            debt_amount_usd: Total debt amount in USD
            relief_percent: Target debt relief percentage

        Returns:
            Dict with structured brief sections
        """
        # 1. Get country data
        country = self.db.execute(
            select(Country).where(Country.code == country_code.upper())
        ).scalar_one_or_none()

        if not country:
            raise AIServiceError(f"Country '{country_code}' not found in database")

        # 2. Get debt data if available
        debt_data = self.db.execute(
            select(DebtData)
            .where(DebtData.country_id == country.id)
            .order_by(DebtData.year.desc())
        ).scalar_one_or_none()

        # 3. Find similar precedents
        try:
            precedent_service = PrecedentSearchService(self.db)
            similar_result = precedent_service.find_similar_precedents(
                country_code=country_code.upper(),
                debt_amount_millions=debt_amount_usd / 1_000_000,
                limit=5,
            )
            similar_precedents = similar_result.get("similar_precedents", [])
        except Exception as e:
            logger.warning(f"Could not fetch similar precedents: {e}")
            similar_precedents = []

        # 4. Also get all precedents with climate clauses for reference
        climate_precedents = self.db.execute(
            select(Precedent)
            .where(Precedent.includes_climate_clause.in_(["Yes", "Partial"]))
            .order_by(Precedent.year.desc())
            .limit(5)
        ).scalars().all()

        # 5. Build the prompt
        prompt = self._build_prompt(
            country=country,
            debt_data=debt_data,
            debt_amount_usd=debt_amount_usd,
            relief_percent=relief_percent,
            similar_precedents=similar_precedents,
            climate_precedents=climate_precedents,
        )

        # 6. Call Claude API
        brief_text = self._call_claude(prompt)

        # 7. Parse and return structured response
        savings_usd = debt_amount_usd * (relief_percent / 100)

        return {
            "country": {
                "code": country.code,
                "name": country.name,
                "region": country.region,
                "income_level": country.income_level,
                "climate_vulnerability_score": country.climate_vulnerability_score,
            },
            "parameters": {
                "debt_amount_usd": debt_amount_usd,
                "relief_percent": relief_percent,
                "potential_savings_usd": savings_usd,
            },
            "brief": brief_text,
            "precedents_used": len(similar_precedents),
            "climate_precedents_used": len(climate_precedents),
        }

    def _build_prompt(
        self,
        country: Country,
        debt_data: Optional[DebtData],
        debt_amount_usd: float,
        relief_percent: float,
        similar_precedents: List[Dict],
        climate_precedents: List[Precedent],
    ) -> str:
        """Build the prompt for Claude with all available context."""

        savings = debt_amount_usd * (relief_percent / 100)
        debt_millions = debt_amount_usd / 1_000_000

        # Format country context
        country_context = f"""
COUNTRY: {country.name} ({country.code})
Region: {country.region}
Income Level: {country.income_level or 'N/A'}
Climate Vulnerability Score: {country.climate_vulnerability_score or 'N/A'}/100 (higher = more vulnerable)
Population: {country.population:,} people
GDP: ${country.gdp_usd_billions or 'N/A'}B USD
"""

        # Format debt context
        debt_context = ""
        if debt_data:
            debt_context = f"""
CURRENT DEBT DATA ({debt_data.year}):
Annual Debt Service: ${debt_data.debt_service_usd_millions:,.0f}M USD
GDP: ${debt_data.gdp_usd_millions:,.0f}M USD
Government Revenue: ${debt_data.government_revenue_usd_millions:,.0f}M USD
Debt Service to Revenue Ratio: {(debt_data.debt_service_usd_millions / debt_data.government_revenue_usd_millions * 100):.1f}%
Healthcare Worker Salary: ${debt_data.healthcare_salary_usd_thousands:,.0f}K/year
School Construction Cost: ${debt_data.school_cost_usd_thousands:,.0f}K
Climate Adaptation Budget: ${debt_data.climate_budget_usd_millions:,.0f}M/year
"""

        # Format similar precedents
        precedent_text = ""
        if similar_precedents:
            precedent_text = "\nCOMPARABLE PRECEDENTS:\n"
            for i, p in enumerate(similar_precedents, 1):
                country_info = p.get("country", {})
                precedent_text += f"""
{i}. {country_info.get('name', 'Unknown')} ({p.get('year', 'N/A')})
   Similarity Score: {p.get('similarity_score', 0):.0f}/100
   Debt Amount: ${p.get('debt_amount_millions', 0):,.0f}M
   Creditor Type: {p.get('creditor_type', 'N/A')}
   Treatment Type: {p.get('treatment_type', 'N/A')}
   NPV Reduction: {p.get('npv_reduction_percent', 0):.0f}%
   Climate Clause: {p.get('includes_climate_clause', 'N/A')}
"""

        # Format climate precedents
        climate_text = ""
        if climate_precedents:
            climate_text = "\nCLIMATE-LINKED RESTRUCTURING PRECEDENTS:\n"
            for cp in climate_precedents:
                cp_country = self.db.execute(
                    select(Country).where(Country.id == cp.country_id)
                ).scalar_one_or_none()
                cp_name = cp_country.name if cp_country else "Unknown"
                climate_text += f"- {cp_name} ({cp.year}): {cp.treatment_type}, "
                climate_text += f"Climate clause: {cp.includes_climate_clause}"
                if cp.climate_notes:
                    climate_text += f" — {cp.climate_notes}"
                climate_text += "\n"

        prompt = f"""You are a senior debt restructuring advisor preparing a confidential strategy brief for {country.name}'s finance ministry. Write a concise, actionable 1-page negotiation strategy brief.

SCENARIO:
{country.name} is seeking restructuring of ${debt_millions:,.0f}M in debt, targeting {relief_percent:.0f}% relief (${savings / 1_000_000:,.0f}M in savings).

{country_context}
{debt_context}
{precedent_text}
{climate_text}

Write the brief with these exact section headers using markdown (##):

## Executive Summary
2-3 sentences on the overall strategy and what is achievable based on comparable cases.

## Comparable Precedents
Reference the most relevant 2-3 precedents from the data above. What did they achieve? What makes them comparable? Include specific numbers (NPV reduction %, debt amounts, treatment types).

## Recommended Negotiating Position
3-4 specific, numbered recommendations on what terms to push for, backed by precedent data. Include target NPV reduction range, grace period, and interest rate benchmarks.

## Climate Clauses to Request
Based on the climate-linked precedents above, recommend 3-4 specific climate provisions to include in any restructuring agreement. Reference actual precedents that achieved these.

## Key Talking Points
5-6 bullet points that negotiators can use in discussions. These should be evidence-based and reference specific data points.

IMPORTANT GUIDELINES:
- Be specific with numbers — reference actual precedent data, not generalities
- Frame everything as what comparable countries achieved, not what "should" happen
- Keep the tone professional and diplomatic — this is for a finance ministry
- Total length should be roughly 1 page (500-700 words)
- Do not add disclaimers or caveats about being an AI — write as an advisor would"""

        return prompt

    def _call_claude(self, prompt: str) -> str:
        """Call the Claude API to generate the brief."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1200,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            return message.content[0].text

        except ImportError:
            raise AIServiceError(
                "anthropic package not installed. Run: pip install anthropic"
            )
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise AIServiceError(f"Failed to generate strategy brief: {str(e)}")
