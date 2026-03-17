"""
Seed precedents data into the database

Run this script to populate the precedents table with historical debt restructuring cases.

Usage:
python scripts/seed_precedents.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.database import get_db
from src.models.precedent import Precedent

PRECEDENTS_DATA = [
    {
        "country": "Ghana",
        "country_code": "GHA",
        "year": 2020,
        "agreement_type": "Paris Club",
        "creditor_type": "Official Creditor",
        "treatment_type": "Debt Service Suspension",
        "debt_amount_usd": 46000000000,
        "npv_reduction_pct": 35.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "Ghana received debt service suspension under the DSSI framework with explicit climate resilience provisions for cocoa sector transition."
    },
    {
        "country": "Kenya",
        "country_code": "KEN",
        "year": 2023,
        "agreement_type": "Bilateral",
        "creditor_type": "Official Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 8500000000,
        "npv_reduction_pct": 22.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "Kenya negotiated bilateral debt restructuring with major creditors including climate adaptation financing for drought resilience programs."
    },
    {
        "country": "Zambia",
        "country_code": "ZMB",
        "year": 2023,
        "agreement_type": "Common Framework",
        "creditor_type": "Multilateral + bilateral",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 21600000000,
        "npv_reduction_pct": 42.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "First Common Framework case with explicit climate clauses for copper sector green transition and renewable energy development."
    },
    {
        "country": "Ethiopia",
        "country_code": "ETH",
        "year": 2021,
        "agreement_type": "Common Framework",
        "creditor_type": "Multilateral + bilateral",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 16600000000,
        "npv_reduction_pct": 38.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "Common Framework agreement with climate-indexed debt provisions tied to agricultural climate adaptation and water security initiatives."
    },
    {
        "country": "Chad",
        "country_code": "TCD",
        "year": 2022,
        "agreement_type": "Common Framework",
        "creditor_type": "Official Creditor",
        "treatment_type": "Debt Service Suspension",
        "debt_amount_usd": 12000000000,
        "npv_reduction_pct": 45.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "Common Framework treatment with climate vulnerability-indexed repayment terms for Sahel region desertification response."
    },
    {
        "country": "Egypt",
        "country_code": "EGY",
        "year": 2020,
        "agreement_type": "IMF Program",
        "creditor_type": "Multilateral",
        "treatment_type": "Financing Package",
        "debt_amount_usd": 145000000000,
        "npv_reduction_pct": 15.0,
        "has_climate_clause": False,
        "region": "Middle East & North Africa",
        "description": "Extended Fund Facility with structural reforms and debt management program focused on fiscal sustainability."
    },
    {
        "country": "Pakistan",
        "country_code": "PAK",
        "year": 2019,
        "agreement_type": "Paris Club",
        "creditor_type": "Official Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 166700000000,
        "npv_reduction_pct": 28.0,
        "has_climate_clause": False,
        "region": "South Asia",
        "description": "Paris Club debt restructuring with extended maturities following IMF program engagement for economic stabilization."
    },
    {
        "country": "Bangladesh",
        "country_code": "BGD",
        "year": 2020,
        "agreement_type": "IMF Program",
        "creditor_type": "Multilateral + bilateral",
        "treatment_type": "Debt Service Suspension",
        "debt_amount_usd": 39800000000,
        "npv_reduction_pct": 18.0,
        "has_climate_clause": True,
        "region": "South Asia",
        "description": "DSSI participation with climate vulnerability provisions for coastal resilience and cyclone adaptation infrastructure."
    },
    {
        "country": "Senegal",
        "country_code": "SEN",
        "year": 2021,
        "agreement_type": "Paris Club",
        "creditor_type": "Official Creditor",
        "treatment_type": "Debt Service Suspension",
        "debt_amount_usd": 15200000000,
        "npv_reduction_pct": 25.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "DSSI treatment with climate-smart agriculture financing provisions for Sahel region food security."
    },
    {
        "country": "Argentina",
        "country_code": "ARG",
        "year": 2020,
        "agreement_type": "Sovereign Bond",
        "creditor_type": "Private Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 65000000000,
        "npv_reduction_pct": 55.0,
        "has_climate_clause": False,
        "region": "Latin America & Caribbean",
        "description": "Landmark private creditor debt restructuring with significant NPV haircut and extended maturity profile."
    },
    {
        "country": "Ecuador",
        "country_code": "ECU",
        "year": 2020,
        "agreement_type": "Sovereign Bond",
        "creditor_type": "Private Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 17500000000,
        "npv_reduction_pct": 52.0,
        "has_climate_clause": False,
        "region": "Latin America & Caribbean",
        "description": "Eurobond restructuring with substantial NPV reduction and cash flow relief during pandemic crisis."
    },
    {
        "country": "Sri Lanka",
        "country_code": "LKA",
        "year": 2023,
        "agreement_type": "IMF Program",
        "creditor_type": "Multilateral + bilateral",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 46000000000,
        "npv_reduction_pct": 32.0,
        "has_climate_clause": False,
        "region": "South Asia",
        "description": "Comprehensive debt restructuring under IMF program following economic crisis and sovereign default."
    },
    {
        "country": "Lebanon",
        "country_code": "LBN",
        "year": 2020,
        "agreement_type": "Sovereign Default",
        "creditor_type": "Private Creditor",
        "treatment_type": "Default",
        "debt_amount_usd": 31000000000,
        "npv_reduction_pct": 0.0,
        "has_climate_clause": False,
        "region": "Middle East & North Africa",
        "description": "First sovereign default in Lebanese history amid banking crisis and currency collapse."
    },
    {
        "country": "Suriname",
        "country_code": "SUR",
        "year": 2021,
        "agreement_type": "Sovereign Bond",
        "creditor_type": "Private Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 675000000,
        "npv_reduction_pct": 48.0,
        "has_climate_clause": False,
        "region": "Latin America & Caribbean",
        "description": "Eurobond restructuring following sovereign default with significant principal haircut and maturity extension."
    },
    {
        "country": "Belize",
        "country_code": "BLZ",
        "year": 2021,
        "agreement_type": "Blue Bond",
        "creditor_type": "Private Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 553000000,
        "npv_reduction_pct": 45.0,
        "has_climate_clause": True,
        "region": "Latin America & Caribbean",
        "description": "Innovative blue bond restructuring with marine conservation financing and debt-for-nature swap components."
    },
    {
        "country": "Grenada",
        "country_code": "GRD",
        "year": 2022,
        "agreement_type": "Hurricane Clause",
        "creditor_type": "Official Creditor",
        "treatment_type": "Debt Service Suspension",
        "debt_amount_usd": 428000000,
        "npv_reduction_pct": 20.0,
        "has_climate_clause": True,
        "region": "Latin America & Caribbean",
        "description": "First implementation of hurricane clause allowing automatic debt service suspension following natural disaster."
    },
    {
        "country": "Barbados",
        "country_code": "BRB",
        "year": 2018,
        "agreement_type": "Domestic Restructuring",
        "creditor_type": "Domestic Creditor",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 4100000000,
        "npv_reduction_pct": 38.0,
        "has_climate_clause": False,
        "region": "Latin America & Caribbean",
        "description": "Successful domestic debt restructuring with strong creditor participation and economic recovery program."
    },
    {
        "country": "Mozambique",
        "country_code": "MOZ",
        "year": 2019,
        "agreement_type": "Paris Club",
        "creditor_type": "Official Creditor",
        "treatment_type": "Debt Service Suspension",
        "debt_amount_usd": 14600000000,
        "npv_reduction_pct": 30.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "Paris Club treatment following cyclone disasters with climate adaptation provisions for coastal resilience."
    },
    {
        "country": "Malawi",
        "country_code": "MWI",
        "year": 2022,
        "agreement_type": "HIPC",
        "creditor_type": "Multilateral",
        "treatment_type": "Debt Relief",
        "debt_amount_usd": 2800000000,
        "npv_reduction_pct": 85.0,
        "has_climate_clause": True,
        "region": "Sub-Saharan Africa",
        "description": "HIPC completion point reached with substantial debt relief and climate resilience development funding."
    },
    {
        "country": "Republic of Congo",
        "country_code": "COG",
        "year": 2019,
        "agreement_type": "IMF Program",
        "creditor_type": "Multilateral + bilateral",
        "treatment_type": "Restructuring",
        "debt_amount_usd": 9000000000,
        "npv_reduction_pct": 35.0,
        "has_climate_clause": False,
        "region": "Sub-Saharan Africa",
        "description": "Extended Credit Facility with debt restructuring from China and other bilateral creditors for oil-backed loans."
    }
]


def seed_precedents():
    """Seed precedents data into the database"""
    print("Starting precedents data seeding...")
    print(f"Total records to insert: {len(PRECEDENTS_DATA)}")
    
    db = next(get_db())
    
    try:
        # Clear existing precedents
        db.query(Precedent).delete()
        db.commit()
        print("✓ Cleared existing precedents")
        
        # Insert new precedents
        for i, data in enumerate(PRECEDENTS_DATA, 1):
            precedent = Precedent(**data)
            db.add(precedent)
            print(f"  [{i}/{len(PRECEDENTS_DATA)}] Added: {data['country']} {data['year']}")
        
        db.commit()
        print(f"\n✅ Successfully seeded {len(PRECEDENTS_DATA)} precedents!")
        
        # Verify
        count = db.query(Precedent).count()
        print(f"✓ Database now contains {count} precedents")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding precedents: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_precedents()
