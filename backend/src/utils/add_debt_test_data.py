"""
Add Sample DebtData to Database

This script adds realistic debt and development cost data for the 5 countries
already in the database (Ghana, Kenya, Zambia, Pakistan, Bangladesh).

Data includes:
- Debt service amounts (IMF-style estimates)
- Healthcare worker salaries
- School construction costs
- Climate adaptation budgets
- GDP and government revenue

Run this script to populate the database with test data for the debt calculator.

Usage:
    python -m src.utils.add_debt_test_data
"""

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.services.database import SessionLocal, engine
from src.models.debt_data import Country, DebtData, Base


def add_debt_test_data():
    """Add sample DebtData records for testing the debt calculator"""
    
    # Create database session
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("📊 ADDING SAMPLE DEBT DATA")
        print("=" * 60)
        
        # Get all countries
        countries = db.execute(select(Country)).scalars().all()
        
        if not countries:
            print("❌ No countries found in database!")
            print("   Please run add_test_data.py first to add countries.")
            return
        
        print(f"\n✓ Found {len(countries)} countries in database")
        
        # Sample data for each country (2023 data)
        # Source: Estimated based on IMF, World Bank, WHO data
        debt_data_samples = {
            "GHA": {  # Ghana
                "year": 2023,
                "debt_service_usd_millions": 2500.0,  # $2.5 billion
                "gdp_usd_millions": 77000.0,  # $77 billion
                "government_revenue_usd_millions": 15000.0,  # $15 billion
                "healthcare_salary_usd_thousands": 20.0,  # $20k annual salary
                "school_cost_usd_thousands": 400.0,  # $400k per school
                "climate_budget_usd_millions": 200.0,  # $200 million
                "source_debt": "IMF World Economic Outlook 2023",
                "source_healthcare": "WHO Global Health Expenditure Database 2023",
                "source_climate": "UNFCCC National Communications Ghana 2023",
                "data_quality_score": 85.0
            },
            "KEN": {  # Kenya
                "year": 2023,
                "debt_service_usd_millions": 3200.0,  # $3.2 billion
                "gdp_usd_millions": 118000.0,  # $118 billion
                "government_revenue_usd_millions": 20000.0,  # $20 billion
                "healthcare_salary_usd_thousands": 18.0,  # $18k annual salary
                "school_cost_usd_thousands": 350.0,  # $350k per school
                "climate_budget_usd_millions": 250.0,  # $250 million
                "source_debt": "IMF World Economic Outlook 2023",
                "source_healthcare": "WHO Global Health Expenditure Database 2023",
                "source_climate": "UNFCCC National Communications Kenya 2023",
                "data_quality_score": 88.0
            },
            "ZMB": {  # Zambia
                "year": 2023,
                "debt_service_usd_millions": 1800.0,  # $1.8 billion
                "gdp_usd_millions": 29000.0,  # $29 billion
                "government_revenue_usd_millions": 6500.0,  # $6.5 billion
                "healthcare_salary_usd_thousands": 15.0,  # $15k annual salary
                "school_cost_usd_thousands": 300.0,  # $300k per school
                "climate_budget_usd_millions": 150.0,  # $150 million
                "source_debt": "IMF World Economic Outlook 2023",
                "source_healthcare": "WHO Global Health Expenditure Database 2023",
                "source_climate": "UNFCCC National Communications Zambia 2023",
                "data_quality_score": 82.0
            },
            "PAK": {  # Pakistan
                "year": 2023,
                "debt_service_usd_millions": 8500.0,  # $8.5 billion
                "gdp_usd_millions": 375000.0,  # $375 billion
                "government_revenue_usd_millions": 50000.0,  # $50 billion
                "healthcare_salary_usd_thousands": 12.0,  # $12k annual salary
                "school_cost_usd_thousands": 250.0,  # $250k per school
                "climate_budget_usd_millions": 400.0,  # $400 million
                "source_debt": "IMF World Economic Outlook 2023",
                "source_healthcare": "WHO Global Health Expenditure Database 2023",
                "source_climate": "UNFCCC National Communications Pakistan 2023",
                "data_quality_score": 80.0
            },
            "BGD": {  # Bangladesh
                "year": 2023,
                "debt_service_usd_millions": 3800.0,  # $3.8 billion
                "gdp_usd_millions": 460000.0,  # $460 billion
                "government_revenue_usd_millions": 55000.0,  # $55 billion
                "healthcare_salary_usd_thousands": 10.0,  # $10k annual salary
                "school_cost_usd_thousands": 200.0,  # $200k per school
                "climate_budget_usd_millions": 500.0,  # $500 million
                "source_debt": "IMF World Economic Outlook 2023",
                "source_healthcare": "WHO Global Health Expenditure Database 2023",
                "source_climate": "UNFCCC National Communications Bangladesh 2023",
                "data_quality_score": 83.0
            }
        }
        
        print("\n" + "=" * 60)
        print("Adding debt data for each country...")
        print("=" * 60 + "\n")
        
        added_count = 0
        skipped_count = 0
        
        for country in countries:
            if country.code not in debt_data_samples:
                print(f"⚠️  {country.name} ({country.code}): No sample data available - skipping")
                skipped_count += 1
                continue
            
            # Check if data already exists
            existing = db.execute(
                select(DebtData).where(
                    DebtData.country_id == country.id,
                    DebtData.year == 2023
                )
            ).scalar_one_or_none()
            
            if existing:
                print(f"ℹ️  {country.name} ({country.code}): Data for 2023 already exists - skipping")
                skipped_count += 1
                continue
            
            # Get sample data for this country
            data = debt_data_samples[country.code]
            
            # Create DebtData record
            debt_data = DebtData(
                country_id=country.id,
                year=data["year"],
                debt_service_usd_millions=data["debt_service_usd_millions"],
                gdp_usd_millions=data["gdp_usd_millions"],
                government_revenue_usd_millions=data["government_revenue_usd_millions"],
                healthcare_salary_usd_thousands=data["healthcare_salary_usd_thousands"],
                school_cost_usd_thousands=data["school_cost_usd_thousands"],
                climate_budget_usd_millions=data["climate_budget_usd_millions"],
                source_debt=data["source_debt"],
                source_healthcare=data["source_healthcare"],
                source_climate=data["source_climate"],
                data_quality_score=data["data_quality_score"],
                collected_date=datetime.utcnow()
            )
            
            db.add(debt_data)
            
            print(f"✓ {country.name} ({country.code}):")
            print(f"  - Debt Service: ${data['debt_service_usd_millions']:,.0f}M")
            print(f"  - Doctor Salary: ${data['healthcare_salary_usd_thousands']:,.0f}K/year")
            print(f"  - School Cost: ${data['school_cost_usd_thousands']:,.0f}K")
            print(f"  - Climate Budget: ${data['climate_budget_usd_millions']:,.0f}M")
            print(f"  - Data Quality: {data['data_quality_score']}%\n")
            
            added_count += 1
        
        # Commit all changes
        db.commit()
        
        print("=" * 60)
        print(f"✅ Successfully added {added_count} debt data records")
        if skipped_count > 0:
            print(f"ℹ️  Skipped {skipped_count} records (already exist or no sample data)")
        print("=" * 60)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DATABASE SUMMARY")
        print("=" * 60)
        
        total_countries = db.execute(select(Country)).scalars().all()
        total_debt_data = db.execute(select(DebtData)).scalars().all()
        
        print(f"Total Countries: {len(total_countries)}")
        print(f"Total DebtData Records: {len(total_debt_data)}")
        
        print("\n🎉 Debt calculator is now ready to test!")
        print("   Try calculating with: country_code='GHA', year=2023, debt_amount_usd=50000000")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error adding debt data: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    add_debt_test_data()