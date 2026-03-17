"""
Add Sample Precedent Data to Database

This script adds realistic historical debt restructuring precedents.
Run: python -m src.utils.add_precedent_test_data
"""

from datetime import datetime
from sqlalchemy import select
from src.services.database import SessionLocal
from src.models.debt_data import Country, Precedent


def add_precedent_test_data():
    """Add sample precedent records for testing precedents search"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("📚 ADDING SAMPLE PRECEDENT DATA")
        print("=" * 60)
        
        # Get countries
        countries = {}
        for country in db.execute(select(Country)).scalars().all():
            countries[country.code] = country
        
        if not countries:
            print("❌ No countries found! Please run add_test_data.py first.")
            return
        
        print(f"\n✓ Found {len(countries)} countries in database")
        
        # Sample precedents data (5 realistic cases)
        precedents_data = [
            {
                "country_code": "GHA",
                "year": 2020,
                "debt_amount_millions": 1800.0,
                "creditor_type": "Paris Club",
                "treatment_type": "Flow",
                "duration_months": 36,
                "npv_reduction_percent": 25.0,
                "grace_period_months": 12,
                "interest_rate_percent": 2.5,
                "terms_summary": "Paris Club flow treatment providing 3-year debt service deferral with 1-year grace period. Interest rate reduced to 2.5%.",
                "conditions": "IMF program compliance required. Quarterly reporting on fiscal reforms. No new non-concessional borrowing.",
                "outcomes": "Successfully completed. Debt service reduced by 25% NPV. Allowed fiscal space for COVID-19 response.",
                "includes_climate_clause": "Partial",
                "climate_notes": "Included provisions for climate adaptation spending protection",
                "source_url": "https://clubdeparis.org/en/communications/press-release/ghana-2020",
                "source_document": "Paris Club Agreed Minutes - Ghana 2020"
            },
            {
                "country_code": "KEN",
                "year": 2021,
                "debt_amount_millions": 2500.0,
                "creditor_type": "Mixed",
                "treatment_type": "Flow",
                "duration_months": 24,
                "npv_reduction_percent": 20.0,
                "grace_period_months": 6,
                "interest_rate_percent": 3.0,
                "terms_summary": "Mixed creditor treatment combining Paris Club and commercial creditors. Flow rescheduling with comparable treatment.",
                "conditions": "Debt sustainability analysis required. Comparable treatment clause for all creditors. Revenue mobilization targets.",
                "outcomes": "Partial success. Paris Club completed but commercial creditors delayed. Liquidity improved but sustainability challenges remain.",
                "includes_climate_clause": "Yes",
                "climate_notes": "Explicit carve-out for climate adaptation spending. Green bond proceeds protected from restructuring.",
                "source_url": "https://clubdeparis.org/kenya-treatment",
                "source_document": "Paris Club - Kenya Treatment 2021"
            },
            {
                "country_code": "ZMB",
                "year": 2022,
                "debt_amount_millions": 3500.0,
                "creditor_type": "Mixed",
                "treatment_type": "Common Framework",
                "duration_months": 60,
                "npv_reduction_percent": 35.0,
                "grace_period_months": 36,
                "interest_rate_percent": 2.0,
                "terms_summary": "G20 Common Framework treatment. First successful case. Deep NPV reduction with extended grace period and low interest rate.",
                "conditions": "IMF Extended Credit Facility required. Transparency requirements for all creditors. Comparability of treatment clause.",
                "outcomes": "Landmark success. Restored debt sustainability. Set precedent for Common Framework. Strong creditor coordination achieved.",
                "includes_climate_clause": "Yes",
                "climate_notes": "Innovative climate adaptation clause. Protected climate spending floors. Linked to NDC targets.",
                "source_url": "https://www.imf.org/zambia-common-framework",
                "source_document": "Common Framework Agreement - Zambia 2022"
            },
            {
                "country_code": "PAK",
                "year": 2023,
                "debt_amount_millions": 5200.0,
                "creditor_type": "Official",
                "treatment_type": "Flow",
                "duration_months": 36,
                "npv_reduction_percent": 18.0,
                "grace_period_months": 18,
                "interest_rate_percent": 3.5,
                "terms_summary": "Bilateral flow treatment following devastating floods. Emergency debt relief to support reconstruction and climate resilience.",
                "conditions": "Flood reconstruction program. Climate resilience investments. Energy sector reforms. IMF program track record.",
                "outcomes": "Ongoing. Initial liquidity relief successful. Reconstruction progressing. Climate adaptation planning initiated.",
                "includes_climate_clause": "Yes",
                "climate_notes": "Explicit climate emergency recognition. Protected disaster response and climate resilience spending. Linked to climate adaptation plan.",
                "source_url": "https://clubdeparis.org/pakistan-floods-2023",
                "source_document": "Emergency Treatment - Pakistan Floods 2023"
            },
            {
                "country_code": "BGD",
                "year": 2017,
                "debt_amount_millions": 1500.0,
                "creditor_type": "Official",
                "treatment_type": "Flow",
                "duration_months": 24,
                "npv_reduction_percent": 12.0,
                "grace_period_months": 12,
                "interest_rate_percent": 2.5,
                "terms_summary": "Concessional rescheduling following Rohingya refugee crisis. Humanitarian emergency treatment with debt service relief.",
                "conditions": "Refugee response program. International humanitarian coordination. Budget transparency on refugee spending.",
                "outcomes": "Successfully completed. Enabled humanitarian response without fiscal destabilization. International solidarity demonstrated.",
                "includes_climate_clause": "Partial",
                "climate_notes": "Recognized climate-migration nexus. Protected refugee response spending including climate adaptation for refugee-hosting areas.",
                "source_url": "https://clubdeparis.org/bangladesh-refugee-2017",
                "source_document": "Humanitarian Emergency Treatment - Bangladesh 2017"
            }
        ]
        
        print("\n" + "=" * 60)
        print("Adding precedent records...")
        print("=" * 60 + "\n")
        
        added_count = 0
        skipped_count = 0
        
        for prec_data in precedents_data:
            country_code = prec_data["country_code"]
            
            if country_code not in countries:
                print(f"⚠️  Country {country_code} not found - skipping")
                skipped_count += 1
                continue
            
            country = countries[country_code]
            
            # Check if precedent already exists
            existing = db.execute(
                select(Precedent).where(
                    Precedent.country_id == country.id,
                    Precedent.year == prec_data["year"],
                    Precedent.creditor_type == prec_data["creditor_type"]
                )
            ).scalar_one_or_none()
            
            if existing:
                print(f"ℹ️  {country.name} ({prec_data['year']}, {prec_data['creditor_type']}) - already exists")
                skipped_count += 1
                continue
            
            # Create precedent
            precedent = Precedent(
                country_id=country.id,
                year=prec_data["year"],
                debt_amount_millions=prec_data["debt_amount_millions"],
                creditor_type=prec_data["creditor_type"],
                treatment_type=prec_data["treatment_type"],
                duration_months=prec_data["duration_months"],
                npv_reduction_percent=prec_data["npv_reduction_percent"],
                grace_period_months=prec_data["grace_period_months"],
                interest_rate_percent=prec_data["interest_rate_percent"],
                terms_summary=prec_data["terms_summary"],
                conditions=prec_data["conditions"],
                outcomes=prec_data["outcomes"],
                includes_climate_clause=prec_data["includes_climate_clause"],
                climate_notes=prec_data["climate_notes"],
                source_url=prec_data["source_url"],
                source_document=prec_data["source_document"],
                created_at=datetime.utcnow()
            )
            
            db.add(precedent)
            
            print(f"✓ {country.name} ({prec_data['year']}):")
            print(f"  - Type: {prec_data['treatment_type']} ({prec_data['creditor_type']})")
            print(f"  - Debt: ${prec_data['debt_amount_millions']:,.0f}M")
            print(f"  - NPV Reduction: {prec_data['npv_reduction_percent']}%")
            print(f"  - Climate Clause: {prec_data['includes_climate_clause']}\n")
            
            added_count += 1
        
        # Commit all changes
        db.commit()
        
        print("=" * 60)
        print(f"✅ Successfully added {added_count} precedent records")
        if skipped_count > 0:
            print(f"ℹ️  Skipped {skipped_count} records (already exist)")
        print("=" * 60)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DATABASE SUMMARY")
        print("=" * 60)
        
        total_precedents = len(db.execute(select(Precedent)).scalars().all())
        
        print(f"Total Countries: {len(countries)}")
        print(f"Total Precedents: {total_precedents}")
        
        print("\n🎉 Precedents search is now ready to test!")
        print("   Try searching by: country, year, creditor type, treatment type")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error adding precedent data: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    add_precedent_test_data()