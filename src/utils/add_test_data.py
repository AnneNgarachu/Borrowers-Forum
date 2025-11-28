"""
Add Test Data to Database
=========================

Quick script to add sample countries for testing.
Run once to populate database with initial data.
"""

from src.services.database import get_db_context
from src.models.debt_data import Country

def add_test_countries():
    """Add sample countries to database."""
    
    test_countries = [
        {
            "name": "Ghana",
            "code": "GHA",
            "region": "Sub-Saharan Africa",
            "income_level": "LMIC",
            "population": 31072940,
            "gdp_usd_billions": 72.8,
            "climate_vulnerability_score": 45.2
        },
        {
            "name": "Kenya",
            "code": "KEN",
            "region": "Sub-Saharan Africa",
            "income_level": "LMIC",
            "population": 53771296,
            "gdp_usd_billions": 110.3,
            "climate_vulnerability_score": 52.1
        },
        {
            "name": "Zambia",
            "code": "ZMB",
            "region": "Sub-Saharan Africa",
            "income_level": "LMIC",
            "population": 18383955,
            "gdp_usd_billions": 23.1,
            "climate_vulnerability_score": 48.7
        },
        {
            "name": "Pakistan",
            "code": "PAK",
            "region": "South Asia",
            "income_level": "LMIC",
            "population": 220892340,
            "gdp_usd_billions": 347.3,
            "climate_vulnerability_score": 64.3
        },
        {
            "name": "Bangladesh",
            "code": "BGD",
            "region": "South Asia",
            "income_level": "LMIC",
            "population": 164689383,
            "gdp_usd_billions": 416.3,
            "climate_vulnerability_score": 71.2
        }
    ]
    
    with get_db_context() as db:
        added_count = 0
        
        for country_data in test_countries:
            # Check if already exists
            existing = db.query(Country).filter(
                Country.code == country_data["code"]
            ).first()
            
            if not existing:
                country = Country(**country_data)
                db.add(country)
                added_count += 1
                print(f"✓ Added: {country_data['name']} ({country_data['code']})")
            else:
                print(f"⊗ Skipped: {country_data['name']} (already exists)")
        
        db.commit()
        print(f"\n✅ Added {added_count} countries to database!")

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Test Countries to Database")
    print("=" * 60)
    add_test_countries()
    print("=" * 60)