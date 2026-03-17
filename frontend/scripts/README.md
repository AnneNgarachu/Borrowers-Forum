# Database Seeding Scripts

This directory contains scripts to populate your Borrower's Forum database with verified data.

## Quick Start

1. **Ensure your backend is running** and database is configured:
   \`\`\`bash
   # Check your .env file has DATABASE_URL set
   cat .env | grep DATABASE_URL
   \`\`\`

2. **Run the seeding script**:
   \`\`\`bash
   python scripts/seed_database.py
   \`\`\`

## What Gets Seeded

### Precedents (20 cases)
- Ghana 2020 - Paris Club Flow Treatment
- Zambia 2023 - Common Framework (First with climate clauses)
- Ethiopia 2021 - Common Framework
- Chad 2022 - Common Framework
- Argentina 2020 - Private Creditor Restructuring ($65B)
- Ecuador 2020 - Galapagos Debt-for-Nature Swap
- Belize 2021 - Blue Bond ($553M)
- Kenya 2021 - Bilateral with climate provisions
- Pakistan 2019 - Bilateral restructuring
- Bangladesh 2020 - Climate vulnerability provisions
- And 10 more verified cases...

**Data Sources**: Paris Club, IMF HIPC Documents, World Bank, Common Framework

### Countries (17 profiles)
All 16 debt-stressed countries plus Egypt:
- Argentina, Bangladesh, Belize, Chad, Ecuador
- Egypt, Ethiopia, Ghana, Kenya, Lebanon
- Mozambique, Pakistan, Senegal, Sri Lanka
- Suriname, Ukraine, Zambia

**Data Sources**: World Bank WDI, IMF WEO, ND-GAIN Climate Index (2023 data)

## Database Schema Requirements

The script expects these tables to exist:

### `precedents` table
\`\`\`sql
CREATE TABLE precedents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT NOT NULL,
    country_name TEXT NOT NULL,
    region TEXT NOT NULL,
    year INTEGER NOT NULL,
    debt_amount_millions REAL NOT NULL,
    creditor_type TEXT NOT NULL,
    treatment_type TEXT NOT NULL,
    npv_reduction_percent REAL NOT NULL,
    includes_climate_clause TEXT NOT NULL,
    description TEXT NOT NULL,
    source TEXT NOT NULL,
    last_updated TEXT NOT NULL
);
\`\`\`

### `countries` table
\`\`\`sql
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    income_level TEXT NOT NULL,
    gdp_usd_billions REAL NOT NULL,
    population INTEGER NOT NULL,
    climate_vulnerability_score REAL NOT NULL,
    debt_to_gdp_percent REAL NOT NULL,
    summary TEXT NOT NULL
);
\`\`\`

## Troubleshooting

### Error: "cannot find module 'src'"
- Make sure you're running from the root directory: `python scripts/seed_database.py`
- Or add the parent directory to PYTHONPATH

### Error: "no such table: precedents"
- Run your database migrations first
- Check that your SQLAlchemy models are properly defined

### Error: "connection refused"
- Verify DATABASE_URL in your .env file
- Check database server is running
- For Render: Use the internal database URL provided by Render

### Error: "permission denied"
- Database user needs INSERT, DELETE permissions
- Check database connection credentials

## Verifying the Seeding

After running the script, verify data was inserted:

\`\`\`bash
# For SQLite
sqlite3 borrowers_forum.db "SELECT COUNT(*) FROM precedents;"
sqlite3 borrowers_forum.db "SELECT COUNT(*) FROM countries;"

# For PostgreSQL
psql $DATABASE_URL -c "SELECT COUNT(*) FROM precedents;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM countries;"
\`\`\`

You should see:
- 20 precedents
- 17 countries

## Running on Render

1. **Connect to your Render shell**:
   \`\`\`bash
   render shell <your-service-name>
   \`\`\`

2. **Navigate to your app directory and run**:
   \`\`\`bash
   cd /opt/render/project/src
   python scripts/seed_database.py
   \`\`\`

3. **Verify via API**:
   \`\`\`bash
   curl https://your-app.onrender.com/api/v1/precedents
   curl https://your-app.onrender.com/api/v1/countries
   \`\`\`

## Notes

- The script will **clear existing data** before inserting
- Run it only once per deployment
- Safe to re-run if you need to refresh data
- All data is factual and sourced from official reports
