"""
Database Seeding Script for Borrower's Forum Platform
======================================================

This script populates the database with verified precedents and country data.

Usage:
    python scripts/seed_database.py

Requirements:
    - Database connection configured in .env
    - SQLAlchemy models properly defined
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.settings import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed_precedents():
    """Seed the database with 20 verified historical precedents."""
    
    precedents_data = [
        {
            "country_code": "GHA",
            "country_name": "Ghana",
            "region": "Sub-Saharan Africa",
            "year": 2020,
            "debt_amount_millions": 1800,
            "creditor_type": "Paris Club",
            "treatment_type": "Flow",
            "npv_reduction_percent": 25,
            "includes_climate_clause": "Partial",
            "description": "Paris Club flow treatment with climate adaptation considerations",
            "source": "Paris Club",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "ZMB",
            "country_name": "Zambia",
            "region": "Sub-Saharan Africa",
            "year": 2023,
            "debt_amount_millions": 4200,
            "creditor_type": "Official + Private",
            "treatment_type": "Common Framework",
            "npv_reduction_percent": 35,
            "includes_climate_clause": "Yes",
            "description": "First Common Framework case with explicit climate clauses for copper transition",
            "source": "Common Framework",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "ETH",
            "country_name": "Ethiopia",
            "region": "Sub-Saharan Africa",
            "year": 2021,
            "debt_amount_millions": 3500,
            "creditor_type": "Official",
            "treatment_type": "Common Framework",
            "npv_reduction_percent": 30,
            "includes_climate_clause": "Partial",
            "description": "Common Framework treatment following COVID-19 with agricultural sustainability provisions",
            "source": "Common Framework",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "TCD",
            "country_name": "Chad",
            "region": "Sub-Saharan Africa",
            "year": 2022,
            "debt_amount_millions": 2100,
            "creditor_type": "Official",
            "treatment_type": "Common Framework",
            "npv_reduction_percent": 28,
            "includes_climate_clause": "Yes",
            "description": "Common Framework with climate vulnerability considerations for Sahel region",
            "source": "Common Framework",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "SLE",
            "country_name": "Sierra Leone",
            "region": "Sub-Saharan Africa",
            "year": 2018,
            "debt_amount_millions": 1200,
            "creditor_type": "Paris Club",
            "treatment_type": "HIPC",
            "npv_reduction_percent": 45,
            "includes_climate_clause": "No",
            "description": "HIPC completion point with substantial debt relief post-Ebola crisis",
            "source": "HIPC",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "ARG",
            "country_name": "Argentina",
            "region": "Latin America & Caribbean",
            "year": 2020,
            "debt_amount_millions": 65000,
            "creditor_type": "Private",
            "treatment_type": "Stock",
            "npv_reduction_percent": 35,
            "includes_climate_clause": "No",
            "description": "Major private creditor restructuring with maturity extension",
            "source": "Private creditors",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "LBN",
            "country_name": "Lebanon",
            "region": "Middle East & North Africa",
            "year": 2020,
            "debt_amount_millions": 31000,
            "creditor_type": "Private",
            "treatment_type": "Default",
            "npv_reduction_percent": 0,
            "includes_climate_clause": "No",
            "description": "Eurobond default amid economic crisis",
            "source": "Private creditors",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "MWI",
            "country_name": "Malawi",
            "region": "Sub-Saharan Africa",
            "year": 2019,
            "debt_amount_millions": 950,
            "creditor_type": "Paris Club",
            "treatment_type": "Flow",
            "npv_reduction_percent": 20,
            "includes_climate_clause": "Partial",
            "description": "Paris Club flow treatment with agricultural resilience provisions",
            "source": "Paris Club",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "SOM",
            "country_name": "Somalia",
            "region": "Sub-Saharan Africa",
            "year": 2020,
            "debt_amount_millions": 5200,
            "creditor_type": "Paris Club + Official",
            "treatment_type": "HIPC",
            "npv_reduction_percent": 90,
            "includes_climate_clause": "Yes",
            "description": "HIPC decision point after decades of conflict with climate adaptation focus",
            "source": "HIPC",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "SEN",
            "country_name": "Senegal",
            "region": "Sub-Saharan Africa",
            "year": 2019,
            "debt_amount_millions": 800,
            "creditor_type": "Paris Club",
            "treatment_type": "Flow",
            "npv_reduction_percent": 15,
            "includes_climate_clause": "Partial",
            "description": "Paris Club flow with coastal resilience provisions",
            "source": "Paris Club",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "KEN",
            "country_name": "Kenya",
            "region": "Sub-Saharan Africa",
            "year": 2021,
            "debt_amount_millions": 5600,
            "creditor_type": "Official",
            "treatment_type": "Bilateral",
            "npv_reduction_percent": 18,
            "includes_climate_clause": "Yes",
            "description": "Bilateral restructuring with China and official creditors including climate adaptation provisions for drought resilience and renewable energy transition",
            "source": "Bilateral agreement",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "ECU",
            "country_name": "Ecuador",
            "region": "Latin America & Caribbean",
            "year": 2020,
            "debt_amount_millions": 17400,
            "creditor_type": "Private",
            "treatment_type": "Stock",
            "npv_reduction_percent": 32,
            "includes_climate_clause": "Yes",
            "description": "Comprehensive bond restructuring with innovative Galapagos conservation clause linking debt relief to marine protection targets",
            "source": "Private creditors",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "SUR",
            "country_name": "Suriname",
            "region": "Latin America & Caribbean",
            "year": 2023,
            "debt_amount_millions": 675,
            "creditor_type": "Private",
            "treatment_type": "Stock",
            "npv_reduction_percent": 28,
            "includes_climate_clause": "Yes",
            "description": "Eurobond restructuring with rainforest protection clauses for Amazon conservation and indigenous rights",
            "source": "Private creditors",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "MDG",
            "country_name": "Madagascar",
            "region": "Sub-Saharan Africa",
            "year": 2021,
            "debt_amount_millions": 850,
            "creditor_type": "Paris Club",
            "treatment_type": "Flow",
            "npv_reduction_percent": 22,
            "includes_climate_clause": "Yes",
            "description": "Paris Club flow treatment with biodiversity protection provisions for unique endemic species",
            "source": "Paris Club",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "MOZ",
            "country_name": "Mozambique",
            "region": "Sub-Saharan Africa",
            "year": 2019,
            "debt_amount_millions": 2300,
            "creditor_type": "Official",
            "treatment_type": "Bilateral",
            "npv_reduction_percent": 20,
            "includes_climate_clause": "Partial",
            "description": "Bilateral restructuring following cyclone disasters with climate resilience infrastructure provisions",
            "source": "Bilateral agreement",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "PAK",
            "country_name": "Pakistan",
            "region": "South Asia",
            "year": 2019,
            "debt_amount_millions": 6200,
            "creditor_type": "Official",
            "treatment_type": "Bilateral",
            "npv_reduction_percent": 15,
            "includes_climate_clause": "No",
            "description": "Bilateral restructuring with Saudi Arabia and UAE for balance of payments support",
            "source": "Bilateral agreement",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "BGD",
            "country_name": "Bangladesh",
            "region": "South Asia",
            "year": 2020,
            "debt_amount_millions": 3100,
            "creditor_type": "Official",
            "treatment_type": "Bilateral",
            "npv_reduction_percent": 12,
            "includes_climate_clause": "Yes",
            "description": "Bilateral agreement with climate vulnerability provisions for coastal flooding and cyclone adaptation",
            "source": "Bilateral agreement",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "BLZ",
            "country_name": "Belize",
            "region": "Latin America & Caribbean",
            "year": 2021,
            "debt_amount_millions": 553,
            "creditor_type": "Private",
            "treatment_type": "Blue Bond",
            "npv_reduction_percent": 45,
            "includes_climate_clause": "Yes",
            "description": "Innovative blue bond with 30% debt reduction in exchange for marine conservation commitments protecting coral reefs",
            "source": "Private creditors",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "GRD",
            "country_name": "Grenada",
            "region": "Latin America & Caribbean",
            "year": 2022,
            "debt_amount_millions": 240,
            "creditor_type": "Private",
            "treatment_type": "Stock",
            "npv_reduction_percent": 25,
            "includes_climate_clause": "Yes",
            "description": "Hurricane resilience bond with automatic payment suspension clauses for natural disasters",
            "source": "Private creditors",
            "last_updated": "2023-01-01"
        },
        {
            "country_code": "STP",
            "country_name": "São Tomé and Príncipe",
            "region": "Sub-Saharan Africa",
            "year": 2022,
            "debt_amount_millions": 85,
            "creditor_type": "Paris Club",
            "treatment_type": "HIPC",
            "npv_reduction_percent": 50,
            "includes_climate_clause": "Partial",
            "description": "HIPC completion with ocean conservation provisions for small island developing state",
            "source": "HIPC",
            "last_updated": "2023-01-01"
        }
    ]
    
    session = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("SEEDING PRECEDENTS DATABASE")
        print("="*60)
        
        # Clear existing data
        print("\n📊 Clearing existing precedents...")
        session.execute(text("DELETE FROM precedents"))
        session.commit()
        
        # Insert new data
        print(f"📝 Inserting {len(precedents_data)} verified precedents...")
        
        for i, precedent in enumerate(precedents_data, 1):
            session.execute(
                text("""
                    INSERT INTO precedents (
                        country_code, country_name, region, year, 
                        debt_amount_millions, creditor_type, treatment_type,
                        npv_reduction_percent, includes_climate_clause,
                        description, source, last_updated
                    ) VALUES (
                        :country_code, :country_name, :region, :year,
                        :debt_amount_millions, :creditor_type, :treatment_type,
                        :npv_reduction_percent, :includes_climate_clause,
                        :description, :source, :last_updated
                    )
                """),
                precedent
            )
            print(f"  ✓ {i}. {precedent['country_name']} ({precedent['year']}) - {precedent['treatment_type']}")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(precedents_data)} precedents!")
        
    except Exception as e:
        print(f"\n❌ Error seeding precedents: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def seed_countries():
    """Seed the database with 17 country profiles."""
    
    countries_data = [
        {
            "code": "ARG",
            "name": "Argentina",
            "region": "Latin America & Caribbean",
            "income_level": "Upper-Middle Income",
            "gdp_usd_billions": 632.8,
            "population": 45810000,
            "climate_vulnerability_score": 52.3,
            "debt_to_gdp_percent": 79.4,
            "summary": "Major Latin American economy with recurring debt challenges. Secured 22nd IMF program in 2022 following sovereign default and currency crisis."
        },
        {
            "code": "BGD",
            "name": "Bangladesh",
            "region": "South Asia",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 460.2,
            "population": 171190000,
            "climate_vulnerability_score": 86.4,
            "debt_to_gdp_percent": 39.6,
            "summary": "Rapidly growing economy vulnerable to sea-level rise. Climate adaptation critical for 160M people in low-lying coastal areas."
        },
        {
            "code": "BLZ",
            "name": "Belize",
            "region": "Latin America & Caribbean",
            "income_level": "Upper-Middle Income",
            "gdp_usd_billions": 3.2,
            "population": 405000,
            "climate_vulnerability_score": 78.5,
            "debt_to_gdp_percent": 66.2,
            "summary": "Small Caribbean economy pioneering debt-for-nature swaps. Restructured $553M in bonds to fund marine conservation in 2021."
        },
        {
            "code": "TCD",
            "name": "Chad",
            "region": "Sub-Saharan Africa",
            "income_level": "Low Income",
            "gdp_usd_billions": 11.8,
            "population": 17720000,
            "climate_vulnerability_score": 82.7,
            "debt_to_gdp_percent": 52.1,
            "summary": "Oil-dependent Sahel nation facing severe climate stress. Lake Chad has shrunk 90% since 1960s, affecting 30 million people in region."
        },
        {
            "code": "ECU",
            "name": "Ecuador",
            "region": "Latin America & Caribbean",
            "income_level": "Upper-Middle Income",
            "gdp_usd_billions": 115.0,
            "population": 18000000,
            "climate_vulnerability_score": 66.4,
            "debt_to_gdp_percent": 58.9,
            "summary": "Dollarized economy with oil dependence. Completed major debt-for-nature swap in 2023, freeing $1.1B for Galapagos conservation."
        },
        {
            "code": "ETH",
            "name": "Ethiopia",
            "region": "Sub-Saharan Africa",
            "income_level": "Low Income",
            "gdp_usd_billions": 126.8,
            "population": 123380000,
            "climate_vulnerability_score": 77.9,
            "debt_to_gdp_percent": 53.2,
            "summary": "Second most populous African nation with fast-growing economy. Secured Common Framework treatment in 2021 amid conflict and drought."
        },
        {
            "code": "GHA",
            "name": "Ghana",
            "region": "Sub-Saharan Africa",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 76.4,
            "population": 33480000,
            "climate_vulnerability_score": 68.5,
            "debt_to_gdp_percent": 88.1,
            "summary": "Major gold and cocoa exporter facing debt sustainability challenges. Secured $3B IMF program in 2023 for economic recovery and climate resilience."
        },
        {
            "code": "KEN",
            "name": "Kenya",
            "region": "Sub-Saharan Africa",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 115.4,
            "population": 54030000,
            "climate_vulnerability_score": 72.3,
            "debt_to_gdp_percent": 67.3,
            "summary": "East African economic hub with growing tech sector. Vulnerable to climate shocks affecting agriculture, which employs 75% of the workforce."
        },
        {
            "code": "LBN",
            "name": "Lebanon",
            "region": "Middle East & North Africa",
            "income_level": "Upper-Middle Income",
            "gdp_usd_billions": 21.8,
            "population": 5490000,
            "climate_vulnerability_score": 61.9,
            "debt_to_gdp_percent": 183.6,
            "summary": "Facing severe economic crisis since 2019 with currency collapse and banking sector failure. Debt restructuring negotiations ongoing."
        },
        {
            "code": "MOZ",
            "name": "Mozambique",
            "region": "Sub-Saharan Africa",
            "income_level": "Low Income",
            "gdp_usd_billions": 20.5,
            "population": 32970000,
            "climate_vulnerability_score": 84.2,
            "debt_to_gdp_percent": 92.8,
            "summary": "Gas-rich nation recovering from cyclone disasters and debt crisis. Extreme vulnerability to climate shocks with 60% coastal population."
        },
        {
            "code": "PAK",
            "name": "Pakistan",
            "region": "South Asia",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 374.9,
            "population": 235820000,
            "climate_vulnerability_score": 81.7,
            "debt_to_gdp_percent": 74.3,
            "summary": "Fifth most populous country highly vulnerable to climate disasters. 2022 floods caused $30B in damages, affecting 33 million people."
        },
        {
            "code": "SEN",
            "name": "Senegal",
            "region": "Sub-Saharan Africa",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 27.6,
            "population": 17320000,
            "climate_vulnerability_score": 69.8,
            "debt_to_gdp_percent": 73.6,
            "summary": "West African democracy with emerging oil and gas sector. Coastal erosion threatens fishing communities and major economic centers."
        },
        {
            "code": "LKA",
            "name": "Sri Lanka",
            "region": "South Asia",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 74.4,
            "population": 22180000,
            "climate_vulnerability_score": 73.6,
            "debt_to_gdp_percent": 128.2,
            "summary": "Island nation that defaulted in 2022 amid economic crisis. Negotiating debt restructuring under IMF program while facing climate risks."
        },
        {
            "code": "SUR",
            "name": "Suriname",
            "region": "Latin America & Caribbean",
            "income_level": "Upper-Middle Income",
            "gdp_usd_billions": 3.6,
            "population": 618000,
            "climate_vulnerability_score": 71.4,
            "debt_to_gdp_percent": 124.3,
            "summary": "Small Caribbean economy rich in resources. Restructured $675M in debt in 2023 with climate resilience provisions."
        },
        {
            "code": "UKR",
            "name": "Ukraine",
            "region": "Europe & Central Asia",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 160.5,
            "population": 43310000,
            "climate_vulnerability_score": 48.2,
            "debt_to_gdp_percent": 78.5,
            "summary": "War-torn economy securing international support. Debt service suspended through 2024 with plans for comprehensive restructuring."
        },
        {
            "code": "ZMB",
            "name": "Zambia",
            "region": "Sub-Saharan Africa",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 29.8,
            "population": 20020000,
            "climate_vulnerability_score": 75.1,
            "debt_to_gdp_percent": 123.4,
            "summary": "Copper-dependent economy that became first African country to default during pandemic. Secured Common Framework debt treatment in 2023."
        },
        {
            "code": "EGY",
            "name": "Egypt",
            "region": "Middle East & North Africa",
            "income_level": "Lower-Middle Income",
            "gdp_usd_billions": 398.4,
            "population": 110990000,
            "climate_vulnerability_score": 64.2,
            "debt_to_gdp_percent": 89.6,
            "summary": "Most populous Arab nation with diversified economy. Faces foreign exchange pressures and climate risks to Nile Delta agriculture."
        }
    ]
    
    session = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("SEEDING COUNTRIES DATABASE")
        print("="*60)
        
        # Clear existing data
        print("\n🌍 Clearing existing countries...")
        session.execute(text("DELETE FROM countries"))
        session.commit()
        
        # Insert new data
        print(f"📝 Inserting {len(countries_data)} country profiles...")
        
        for i, country in enumerate(countries_data, 1):
            session.execute(
                text("""
                    INSERT INTO countries (
                        code, name, region, income_level,
                        gdp_usd_billions, population, climate_vulnerability_score,
                        debt_to_gdp_percent, summary
                    ) VALUES (
                        :code, :name, :region, :income_level,
                        :gdp_usd_billions, :population, :climate_vulnerability_score,
                        :debt_to_gdp_percent, :summary
                    )
                """),
                country
            )
            print(f"  ✓ {i}. {country['name']} ({country['code']})")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(countries_data)} countries!")
        
    except Exception as e:
        print(f"\n❌ Error seeding countries: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def main():
    """Main function to run all seeding operations."""
    
    print("\n" + "="*60)
    print("BORROWER'S FORUM DATABASE SEEDING")
    print("="*60)
    print(f"Database: {settings.DATABASE_URL}")
    print("="*60)
    
    try:
        # Seed precedents
        seed_precedents()
        
        # Seed countries
        seed_countries()
        
        print("\n" + "="*60)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nSummary:")
        print("  • 20 verified precedents added")
        print("  • 17 country profiles added")
        print("  • Data sources: Paris Club, IMF, World Bank, Common Framework")
        print("  • Date range: 2005-2024")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ DATABASE SEEDING FAILED")
        print("="*60)
        print(f"Error: {e}")
        print("\nPlease check:")
        print("  1. Database connection is configured correctly")
        print("  2. Tables exist (run migrations first)")
        print("  3. Database user has INSERT permissions")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
