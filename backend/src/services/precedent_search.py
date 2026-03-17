"""
Precedents Search Service

Business logic for searching and analyzing historical debt restructuring precedents.

Features:
- Filter by country, year range, creditor type, treatment type
- Similarity matching based on debt amount, country characteristics
- Ranked results by relevance
"""

from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from datetime import datetime

from ..models.debt_data import Country, Precedent


class PrecedentSearchError(Exception):
    """Custom exception for precedent search errors"""
    pass


class PrecedentSearchService:
    """
    Service for searching historical debt restructuring precedents.
    
    Provides filtering, sorting, and similarity matching to help countries
    find comparable cases for negotiation reference.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize the precedent search service.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def search_precedents(
        self,
        country_code: Optional[str] = None,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        creditor_type: Optional[str] = None,
        treatment_type: Optional[str] = None,
        includes_climate: Optional[bool] = None,
        min_debt_amount: Optional[float] = None,
        max_debt_amount: Optional[float] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict:
        """
        Search precedents with multiple filters.
        
        Args:
            country_code: Filter by country (ISO 3-letter code)
            year_start: Start of year range (inclusive)
            year_end: End of year range (inclusive)
            creditor_type: Type of creditor (Official, Private, Mixed, Paris Club)
            treatment_type: Type of treatment (Flow, Stock, HIPC, Common Framework)
            includes_climate: Filter by climate clause presence
            min_debt_amount: Minimum debt amount in millions USD
            max_debt_amount: Maximum debt amount in millions USD
            limit: Maximum number of results
            offset: Number of results to skip (for pagination)
        
        Returns:
            Dictionary with precedents list, total count, and filters applied
        """
        # Build query
        query = select(Precedent, Country).join(
            Country, Precedent.country_id == Country.id
        )
        
        # Apply filters
        filters = []
        
        if country_code:
            filters.append(Country.code == country_code.upper())
        
        if year_start:
            filters.append(Precedent.year >= year_start)
        
        if year_end:
            filters.append(Precedent.year <= year_end)
        
        if creditor_type:
            filters.append(Precedent.creditor_type == creditor_type)
        
        if treatment_type:
            filters.append(Precedent.treatment_type == treatment_type)
        
        if includes_climate is not None:
            if includes_climate:
                filters.append(Precedent.includes_climate_clause.in_(['Yes', 'Partial']))
            else:
                filters.append(Precedent.includes_climate_clause == 'No')
        
        if min_debt_amount is not None:
            filters.append(Precedent.debt_amount_millions >= min_debt_amount)
        
        if max_debt_amount is not None:
            filters.append(Precedent.debt_amount_millions <= max_debt_amount)
        
        if filters:
            query = query.where(and_(*filters))
        
        # Order by most recent first
        query = query.order_by(Precedent.year.desc())
        
        # Get total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.execute(count_query).scalar()
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        # Execute query
        results = self.db.execute(query).all()
        
        # Format results
        precedents = []
        for precedent, country in results:
            precedents.append({
                "id": precedent.id,
                "country": {
                    "code": country.code,
                    "name": country.name,
                    "region": country.region,
                    "income_level": country.income_level
                },
                "year": precedent.year,
                "debt_amount_millions": float(precedent.debt_amount_millions),
                "creditor_type": precedent.creditor_type,
                "treatment_type": precedent.treatment_type,
                "duration_months": precedent.duration_months,
                "npv_reduction_percent": float(precedent.npv_reduction_percent) if precedent.npv_reduction_percent else None,
                "grace_period_months": precedent.grace_period_months,
                "interest_rate_percent": float(precedent.interest_rate_percent) if precedent.interest_rate_percent else None,
                "terms_summary": precedent.terms_summary,
                "conditions": precedent.conditions,
                "outcomes": precedent.outcomes,
                "includes_climate_clause": precedent.includes_climate_clause,
                "climate_notes": precedent.climate_notes,
                "source_url": precedent.source_url,
                "source_document": precedent.source_document
            })
        
        return {
            "precedents": precedents,
            "total": total,
            "limit": limit,
            "offset": offset,
            "filters_applied": {
                "country_code": country_code,
                "year_range": f"{year_start or 'any'}-{year_end or 'any'}",
                "creditor_type": creditor_type,
                "treatment_type": treatment_type,
                "includes_climate": includes_climate,
                "debt_range_millions": f"{min_debt_amount or 0}-{max_debt_amount or 'unlimited'}"
            }
        }
    
    def find_similar_precedents(
        self,
        country_code: str,
        debt_amount_millions: float,
        limit: int = 10
    ) -> Dict:
        """
        Find precedents similar to a given country and debt situation.
        
        Uses similarity scoring based on:
        - Country characteristics (region, income level, climate vulnerability)
        - Debt amount (within similar range)
        - Recency (prefer more recent cases)
        
        Args:
            country_code: ISO 3-letter country code
            debt_amount_millions: Debt amount in millions USD
            limit: Maximum number of results
        
        Returns:
            Dictionary with ranked similar precedents
        
        Raises:
            PrecedentSearchError: If country not found
        """
        # Get the reference country
        country = self.db.execute(
            select(Country).where(Country.code == country_code.upper())
        ).scalar_one_or_none()
        
        if not country:
            raise PrecedentSearchError(f"Country with code '{country_code}' not found")
        
        # Get all precedents with their countries
        query = select(Precedent, Country).join(
            Country, Precedent.country_id == Country.id
        )
        
        results = self.db.execute(query).all()
        
        # Score each precedent for similarity
        scored_precedents = []
        
        for precedent, prec_country in results:
            score = self._calculate_similarity_score(
                reference_country=country,
                precedent=precedent,
                precedent_country=prec_country,
                reference_debt_amount=debt_amount_millions
            )
            
            scored_precedents.append({
                "precedent": precedent,
                "country": prec_country,
                "similarity_score": score,
                "score_breakdown": self._get_score_breakdown(
                    country, prec_country, debt_amount_millions, precedent
                )
            })
        
        # Sort by similarity score (descending)
        scored_precedents.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # Take top N
        top_precedents = scored_precedents[:limit]
        
        # Format results
        results_list = []
        for item in top_precedents:
            precedent = item["precedent"]
            prec_country = item["country"]
            
            results_list.append({
                "id": precedent.id,
                "similarity_score": round(item["similarity_score"], 2),
                "score_breakdown": item["score_breakdown"],
                "country": {
                    "code": prec_country.code,
                    "name": prec_country.name,
                    "region": prec_country.region,
                    "income_level": prec_country.income_level
                },
                "year": precedent.year,
                "debt_amount_millions": float(precedent.debt_amount_millions),
                "creditor_type": precedent.creditor_type,
                "treatment_type": precedent.treatment_type,
                "npv_reduction_percent": float(precedent.npv_reduction_percent) if precedent.npv_reduction_percent else None,
                "grace_period_months": precedent.grace_period_months,
                "terms_summary": precedent.terms_summary,
                "outcomes": precedent.outcomes,
                "includes_climate_clause": precedent.includes_climate_clause
            })
        
        return {
            "reference_country": {
                "code": country.code,
                "name": country.name,
                "region": country.region,
                "income_level": country.income_level
            },
            "reference_debt_amount_millions": debt_amount_millions,
            "similar_precedents": results_list,
            "total_found": len(results_list)
        }
    
    def _calculate_similarity_score(
        self,
        reference_country: Country,
        precedent: Precedent,
        precedent_country: Country,
        reference_debt_amount: float
    ) -> float:
        """
        Calculate similarity score between reference situation and precedent.
        
        Scoring components (0-100):
        - Same region: +30 points
        - Same income level: +25 points
        - Similar climate vulnerability: +15 points
        - Similar debt amount: +20 points
        - Recency: +10 points
        
        Args:
            reference_country: The country seeking precedents
            precedent: The historical precedent
            precedent_country: The country of the precedent
            reference_debt_amount: The debt amount to compare
        
        Returns:
            Similarity score (0-100)
        """
        score = 0.0
        
        # Regional similarity (30 points)
        if reference_country.region == precedent_country.region:
            score += 30
        
        # Income level similarity (25 points)
        if reference_country.income_level == precedent_country.income_level:
            score += 25
        
        # Climate vulnerability similarity (15 points)
        if reference_country.climate_vulnerability_score and precedent_country.climate_vulnerability_score:
            diff = abs(reference_country.climate_vulnerability_score - precedent_country.climate_vulnerability_score)
            # Full points if within 10 points, scaled down beyond that
            similarity = max(0, 15 - (diff / 10 * 15))
            score += similarity
        
        # Debt amount similarity (20 points)
        # Consider similar if within 50% of reference amount
        debt_ratio = precedent.debt_amount_millions / reference_debt_amount
        if 0.5 <= debt_ratio <= 2.0:
            # Full points at 1:1 ratio, scaled down as ratio deviates
            deviation = abs(1.0 - debt_ratio)
            similarity = max(0, 20 - (deviation * 40))
            score += similarity
        
        # Recency (10 points)
        # More recent cases are more relevant
        current_year = datetime.now().year
        years_ago = current_year - precedent.year
        # Full points if within 5 years, scaled down for older cases
        recency_score = max(0, 10 - (years_ago / 5 * 10))
        score += recency_score
        
        return min(100, score)  # Cap at 100
    
    def _get_score_breakdown(
        self,
        reference_country: Country,
        precedent_country: Country,
        reference_debt_amount: float,
        precedent: Precedent
    ) -> Dict:
        """Get detailed breakdown of similarity score components"""
        breakdown = {
            "regional_match": reference_country.region == precedent_country.region,
            "income_level_match": reference_country.income_level == precedent_country.income_level,
            "climate_vulnerability_similarity": None,
            "debt_amount_ratio": round(precedent.debt_amount_millions / reference_debt_amount, 2),
            "years_ago": datetime.now().year - precedent.year
        }
        
        if reference_country.climate_vulnerability_score and precedent_country.climate_vulnerability_score:
            breakdown["climate_vulnerability_similarity"] = round(
                abs(reference_country.climate_vulnerability_score - precedent_country.climate_vulnerability_score),
                1
            )
        
        return breakdown
    
    def get_precedent_statistics(self) -> Dict:
        """
        Get statistics about available precedents.
        
        Returns:
            Dictionary with counts by various categories
        """
        # Total count
        total = self.db.execute(select(func.count(Precedent.id))).scalar()
        
        # Count by creditor type
        creditor_counts = {}
        creditor_results = self.db.execute(
            select(Precedent.creditor_type, func.count(Precedent.id))
            .group_by(Precedent.creditor_type)
        ).all()
        for creditor_type, count in creditor_results:
            if creditor_type:
                creditor_counts[creditor_type] = count
        
        # Count by treatment type
        treatment_counts = {}
        treatment_results = self.db.execute(
            select(Precedent.treatment_type, func.count(Precedent.id))
            .group_by(Precedent.treatment_type)
        ).all()
        for treatment_type, count in treatment_results:
            if treatment_type:
                treatment_counts[treatment_type] = count
        
        # Count with climate clauses
        climate_count = self.db.execute(
            select(func.count(Precedent.id))
            .where(Precedent.includes_climate_clause.in_(['Yes', 'Partial']))
        ).scalar()
        
        # Year range
        year_stats = self.db.execute(
            select(
                func.min(Precedent.year),
                func.max(Precedent.year)
            )
        ).one()
        
        return {
            "total_precedents": total,
            "by_creditor_type": creditor_counts,
            "by_treatment_type": treatment_counts,
            "with_climate_clause": climate_count,
            "year_range": {
                "earliest": year_stats[0],
                "latest": year_stats[1]
            }
        }