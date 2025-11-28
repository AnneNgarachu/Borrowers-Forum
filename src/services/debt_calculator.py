"""
Debt Calculator Service

This module provides business logic for calculating debt service trade-offs
against development spending (doctors, schools, climate projects).

Business Rules:
- Converts debt service amounts to equivalent development resources
- Uses country-specific salary and cost data from DebtData table
- Provides year-over-year comparisons
- Highlights opportunity costs of debt payments
"""

from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from decimal import Decimal, ROUND_HALF_UP

from ..models.debt_data import Country, DebtData


class DebtCalculationError(Exception):
    """Custom exception for debt calculation errors"""
    pass


class DebtCalculatorService:
    """
    Service for calculating debt service vs development trade-offs.
    
    This service converts debt service payments into equivalent numbers of:
    - Doctors that could be employed
    - Schools that could be built
    - Climate adaptation projects that could be funded
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize the debt calculator service.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def calculate_opportunity_cost(
        self,
        country_code: str,
        year: int,
        debt_amount_usd: float
    ) -> Dict:
        """
        Calculate the opportunity cost of debt service in development terms.
        
        Args:
            country_code: ISO 3-letter country code (e.g., 'GHA', 'KEN')
            year: Year for the calculation (2015-2030)
            debt_amount_usd: Debt service amount in USD
        
        Returns:
            Dictionary containing:
                - country_info: Basic country details
                - debt_amount: Input debt amount
                - equivalents: Calculated equivalents (doctors, schools, etc.)
                - year: Year of calculation
                - data_quality: Data quality score (0-100)
        
        Raises:
            DebtCalculationError: If country not found, data missing, or invalid input
        """
        # Validate inputs
        if debt_amount_usd <= 0:
            raise DebtCalculationError("Debt amount must be greater than 0")
        
        if year < 2015 or year > 2030:
            raise DebtCalculationError("Year must be between 2015 and 2030")
        
        # Get country
        country = self.db.execute(
            select(Country).where(Country.code == country_code.upper())
        ).scalar_one_or_none()
        
        if not country:
            raise DebtCalculationError(f"Country with code '{country_code}' not found")
        
        # Get debt data for the specified year
        debt_data = self.db.execute(
            select(DebtData).where(
                DebtData.country_id == country.id,
                DebtData.year == year
            )
        ).scalar_one_or_none()
        
        if not debt_data:
            raise DebtCalculationError(
                f"No debt data available for {country.name} in {year}"
            )
        
        # Check if we have the necessary data
        missing_data = []
        if not debt_data.healthcare_salary_usd_thousands:
            missing_data.append("healthcare salary")
        if not debt_data.school_cost_usd_thousands:
            missing_data.append("school cost")
        if not debt_data.climate_budget_usd_millions:
            missing_data.append("climate budget")
        
        if missing_data:
            raise DebtCalculationError(
                f"Missing required data for {country.name} ({year}): {', '.join(missing_data)}"
            )
        
        # Calculate equivalents
        equivalents = self._calculate_equivalents(debt_amount_usd, debt_data)
        
        # Build response
        result = {
            "country_info": {
                "code": country.code,
                "name": country.name,
                "region": country.region,
                "income_level": country.income_level,
                "population": country.population,
                "gdp_usd_billions": float(country.gdp_usd_billions) if country.gdp_usd_billions else None,
                "climate_vulnerability_score": float(country.climate_vulnerability_score) if country.climate_vulnerability_score else None
            },
            "calculation": {
                "debt_amount_usd": float(debt_amount_usd),
                "year": year,
                "data_quality_score": float(debt_data.data_quality_score) if debt_data.data_quality_score else None
            },
            "equivalents": equivalents,
            "context": {
                "annual_debt_service_usd": float(debt_data.debt_service_usd_millions * 1_000_000) if debt_data.debt_service_usd_millions else None,
                "gdp_usd": float(debt_data.gdp_usd_millions * 1_000_000) if debt_data.gdp_usd_millions else None,
                "government_revenue_usd": float(debt_data.government_revenue_usd_millions * 1_000_000) if debt_data.government_revenue_usd_millions else None,
                "debt_to_gdp_ratio": self._calculate_ratio(
                    debt_amount_usd, 
                    debt_data.gdp_usd_millions * 1_000_000 if debt_data.gdp_usd_millions else None
                ),
                "debt_to_revenue_ratio": self._calculate_ratio(
                    debt_amount_usd,
                    debt_data.government_revenue_usd_millions * 1_000_000 if debt_data.government_revenue_usd_millions else None
                )
            },
            "sources": {
                "debt_data": debt_data.source_debt,
                "healthcare_data": debt_data.source_healthcare,
                "education_data": debt_data.source_school,  # ← CORRECT FIELD NAME
                "climate_data": debt_data.source_climate
            }
        }
        
        return result
    
    def _calculate_equivalents(
        self,
        debt_amount_usd: float,
        debt_data: DebtData
    ) -> Dict:
        """
        Calculate equivalent resources (doctors, schools, climate projects).
        
        Args:
            debt_amount_usd: Debt amount in USD
            debt_data: DebtData record with cost information
        
        Returns:
            Dictionary with calculated equivalents
        """
        # Convert to Decimal for precise calculations
        debt_decimal = Decimal(str(debt_amount_usd))
        
        # Convert salary/costs from thousands/millions to actual amounts
        doctor_annual_salary = Decimal(str(debt_data.healthcare_salary_usd_thousands)) * 1000
        school_cost = Decimal(str(debt_data.school_cost_usd_thousands)) * 1000
        climate_budget_total = Decimal(str(debt_data.climate_budget_usd_millions)) * 1_000_000
        
        # Calculate equivalents
        # Doctors: Assuming 5-year employment contracts
        doctors_5_years = (debt_decimal / (doctor_annual_salary * 5)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        # Doctors: Annual employment
        doctors_1_year = (debt_decimal / doctor_annual_salary).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        # Schools: One-time construction cost
        schools = (debt_decimal / school_cost).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        # Climate projects: Percentage of annual climate budget
        climate_percentage = (
            (debt_decimal / climate_budget_total) * 100
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if climate_budget_total > 0 else Decimal('0')
        
        return {
            "doctors": {
                "annual_employment": float(doctors_1_year),
                "five_year_employment": float(doctors_5_years),
                "annual_salary_usd": float(doctor_annual_salary),
                "description": f"Could employ {int(doctors_1_year)} doctors for 1 year or {int(doctors_5_years)} doctors for 5 years"
            },
            "schools": {
                "number_of_schools": float(schools),
                "cost_per_school_usd": float(school_cost),
                "description": f"Could build {int(schools)} schools"
            },
            "climate_adaptation": {
                "percentage_of_annual_budget": float(climate_percentage),
                "annual_climate_budget_usd": float(climate_budget_total),
                "description": f"Represents {float(climate_percentage):.1f}% of annual climate adaptation budget"
            }
        }
    
    def _calculate_ratio(
        self,
        numerator: Optional[float],
        denominator: Optional[float]
    ) -> Optional[float]:
        """
        Calculate percentage ratio with null handling.
        
        Args:
            numerator: Top value
            denominator: Bottom value
        
        Returns:
            Percentage ratio or None if either value is missing
        """
        if numerator is None or denominator is None or denominator == 0:
            return None
        
        return round((numerator / denominator) * 100, 2)
    
    def compare_scenarios(
        self,
        country_code: str,
        year: int,
        scenarios: list[float]
    ) -> Dict:
        """
        Compare multiple debt amount scenarios.
        
        Args:
            country_code: ISO 3-letter country code
            year: Year for calculations
            scenarios: List of debt amounts to compare
        
        Returns:
            Dictionary with comparative analysis
        """
        if len(scenarios) < 2:
            raise DebtCalculationError("At least 2 scenarios required for comparison")
        
        results = []
        for debt_amount in scenarios:
            try:
                result = self.calculate_opportunity_cost(country_code, year, debt_amount)
                results.append(result)
            except DebtCalculationError as e:
                # Skip invalid scenarios
                continue
        
        if len(results) < 2:
            raise DebtCalculationError("Not enough valid scenarios to compare")
        
        return {
            "country": results[0]["country_info"]["name"],
            "year": year,
            "scenarios": results,
            "comparison": self._build_comparison(results)
        }
    
    def _build_comparison(self, results: list[Dict]) -> Dict:
        """
        Build comparison statistics across scenarios.
        
        Args:
            results: List of calculation results
        
        Returns:
            Comparison dictionary
        """
        debt_amounts = [r["calculation"]["debt_amount_usd"] for r in results]
        doctors_annual = [r["equivalents"]["doctors"]["annual_employment"] for r in results]
        schools = [r["equivalents"]["schools"]["number_of_schools"] for r in results]
        
        return {
            "debt_range": {
                "min": min(debt_amounts),
                "max": max(debt_amounts),
                "difference": max(debt_amounts) - min(debt_amounts)
            },
            "doctors_range": {
                "min": min(doctors_annual),
                "max": max(doctors_annual),
                "difference": max(doctors_annual) - min(doctors_annual)
            },
            "schools_range": {
                "min": min(schools),
                "max": max(schools),
                "difference": max(schools) - min(schools)
            }
        }