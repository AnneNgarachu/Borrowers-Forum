"""
Script to create the api_keys table in Supabase.

Run this ONCE to set up the table:
    python -m src.utils.add_api_keys_table

IMPORTANT: Stop the API server before running this script!
"""

from sqlalchemy import text
from src.services.database import engine, SessionLocal
from src.models.debt_data import Base, APIKey


def create_api_keys_table():
    """Create the api_keys table if it doesn't exist."""
    print("=" * 60)
    print("Creating API Keys Table")
    print("=" * 60)
    
    try:
        # Create the table
        print("\n1. Creating api_keys table...")
        
        # This creates only the APIKey table if it doesn't exist
        APIKey.__table__.create(engine, checkfirst=True)
        
        print("   ✅ Table created successfully!")
        
        # Verify the table exists
        print("\n2. Verifying table exists...")
        db = SessionLocal()
        try:
            result = db.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'api_keys'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            
            if columns:
                print("   ✅ Table verified! Columns:")
                for col_name, col_type in columns:
                    print(f"      - {col_name}: {col_type}")
            else:
                print("   ⚠️  Table created but no columns found (unusual)")
                
        finally:
            db.close()
            
        print("\n" + "=" * 60)
        print("✅ API Keys table setup complete!")
        print("=" * 60)
        print("\nNext step: Create the auth service (Step 2)")
        
    except Exception as e:
        print(f"\n❌ Error creating table: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure .env has correct DATABASE_URL")
        print("2. Make sure API server is stopped (Ctrl+C)")
        print("3. Check your internet connection")
        raise


if __name__ == "__main__":
    create_api_keys_table()