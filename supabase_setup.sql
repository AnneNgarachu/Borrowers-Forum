-- ============================================================
-- Borrower's Forum Platform - Complete Supabase Setup
-- ============================================================
-- Run this entire script in Supabase SQL Editor (one shot)
-- Creates: countries, debt_data, precedents, api_keys
-- Seeds: 17 countries, 20 precedents, 5 debt records, 1 demo API key
-- ============================================================

-- ============================================================
-- 1. EXTENSIONS
-- ============================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 2. CREATE TABLES
-- ============================================================

-- Countries master table
CREATE TABLE IF NOT EXISTS countries (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(3) NOT NULL UNIQUE,
    region VARCHAR(50),
    income_level VARCHAR(10),
    population INTEGER,
    gdp_usd_billions DOUBLE PRECISION,
    climate_vulnerability_score DOUBLE PRECISION,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_countries_name ON countries(name);
CREATE INDEX IF NOT EXISTS idx_countries_code ON countries(code);

-- Debt data (annual debt service + development indicators)
CREATE TABLE IF NOT EXISTS debt_data (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    country_id VARCHAR(36) NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    debt_service_usd_millions DOUBLE PRECISION NOT NULL,
    gdp_usd_millions DOUBLE PRECISION,
    government_revenue_usd_millions DOUBLE PRECISION,
    healthcare_salary_usd_thousands DOUBLE PRECISION,
    school_cost_usd_thousands DOUBLE PRECISION,
    climate_budget_usd_millions DOUBLE PRECISION,
    source_debt VARCHAR(500) NOT NULL,
    source_healthcare VARCHAR(500),
    source_school VARCHAR(500),
    source_climate VARCHAR(500),
    data_quality_score DOUBLE PRECISION,
    notes VARCHAR(2000),
    collected_date TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_country_year UNIQUE (country_id, year),
    CONSTRAINT positive_debt_service CHECK (debt_service_usd_millions > 0),
    CONSTRAINT valid_year_range CHECK (year >= 2015 AND year <= 2030)
);

CREATE INDEX IF NOT EXISTS idx_debt_data_country_id ON debt_data(country_id);
CREATE INDEX IF NOT EXISTS idx_debt_data_year ON debt_data(year);

-- Precedents (historical debt restructuring cases)
CREATE TABLE IF NOT EXISTS precedents (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    country_id VARCHAR(36) NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    debt_amount_millions DOUBLE PRECISION NOT NULL,
    creditor_type VARCHAR(50),
    treatment_type VARCHAR(50),
    duration_months INTEGER,
    npv_reduction_percent DOUBLE PRECISION,
    grace_period_months INTEGER,
    interest_rate_percent DOUBLE PRECISION,
    terms_summary VARCHAR(2000),
    conditions VARCHAR(2000),
    outcomes VARCHAR(2000),
    includes_climate_clause VARCHAR(10),
    climate_notes VARCHAR(1000),
    source_url VARCHAR(500),
    source_document VARCHAR(500),
    notes VARCHAR(2000),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT positive_debt_amount CHECK (debt_amount_millions > 0),
    CONSTRAINT valid_precedent_year CHECK (year >= 1980 AND year <= 2030)
);

CREATE INDEX IF NOT EXISTS idx_precedents_country_id ON precedents(country_id);
CREATE INDEX IF NOT EXISTS idx_precedents_year ON precedents(year);
CREATE INDEX IF NOT EXISTS idx_precedents_creditor_type ON precedents(creditor_type);
CREATE INDEX IF NOT EXISTS idx_precedents_treatment_type ON precedents(treatment_type);

-- API Keys (authentication)
CREATE TABLE IF NOT EXISTS api_keys (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    key_id VARCHAR(16) NOT NULL UNIQUE,
    key_hash VARCHAR(128) NOT NULL,
    name VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    permissions VARCHAR(20) NOT NULL DEFAULT 'read',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 100,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    usage_count INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_api_keys_key_id ON api_keys(key_id);

-- ============================================================
-- 3. AUTO-UPDATE TRIGGER for updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_countries_updated_at
    BEFORE UPDATE ON countries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER trg_debt_data_updated_at
    BEFORE UPDATE ON debt_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER trg_precedents_updated_at
    BEFORE UPDATE ON precedents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- 4. SEED DATA - COUNTRIES (17 profiles)
-- ============================================================
INSERT INTO countries (id, code, name, region, income_level, population, gdp_usd_billions, climate_vulnerability_score)
VALUES
    (uuid_generate_v4()::text, 'ARG', 'Argentina',               'Latin America & Caribbean',  'UMIC',  45810000,  632.8, 52.3),
    (uuid_generate_v4()::text, 'BGD', 'Bangladesh',              'South Asia',                 'LMIC',  171190000, 460.2, 86.4),
    (uuid_generate_v4()::text, 'BLZ', 'Belize',                  'Latin America & Caribbean',  'UMIC',  405000,    3.2,   78.5),
    (uuid_generate_v4()::text, 'TCD', 'Chad',                    'Sub-Saharan Africa',         'LIC',   17720000,  11.8,  82.7),
    (uuid_generate_v4()::text, 'ECU', 'Ecuador',                 'Latin America & Caribbean',  'UMIC',  18000000,  115.0, 66.4),
    (uuid_generate_v4()::text, 'ETH', 'Ethiopia',                'Sub-Saharan Africa',         'LIC',   123380000, 126.8, 77.9),
    (uuid_generate_v4()::text, 'GHA', 'Ghana',                   'Sub-Saharan Africa',         'LMIC',  33480000,  76.4,  68.5),
    (uuid_generate_v4()::text, 'KEN', 'Kenya',                   'Sub-Saharan Africa',         'LMIC',  54030000,  115.4, 72.3),
    (uuid_generate_v4()::text, 'LBN', 'Lebanon',                 'Middle East & North Africa', 'UMIC',  5490000,   21.8,  61.9),
    (uuid_generate_v4()::text, 'MOZ', 'Mozambique',              'Sub-Saharan Africa',         'LIC',   32970000,  20.5,  84.2),
    (uuid_generate_v4()::text, 'PAK', 'Pakistan',                'South Asia',                 'LMIC',  235820000, 374.9, 81.7),
    (uuid_generate_v4()::text, 'SEN', 'Senegal',                 'Sub-Saharan Africa',         'LMIC',  17320000,  27.6,  69.8),
    (uuid_generate_v4()::text, 'LKA', 'Sri Lanka',               'South Asia',                 'LMIC',  22180000,  74.4,  73.6),
    (uuid_generate_v4()::text, 'SUR', 'Suriname',                'Latin America & Caribbean',  'UMIC',  618000,    3.6,   71.4),
    (uuid_generate_v4()::text, 'UKR', 'Ukraine',                 'Europe & Central Asia',      'LMIC',  43310000,  160.5, 48.2),
    (uuid_generate_v4()::text, 'ZMB', 'Zambia',                  'Sub-Saharan Africa',         'LMIC',  20020000,  29.8,  75.1),
    (uuid_generate_v4()::text, 'EGY', 'Egypt',                   'Middle East & North Africa', 'LMIC',  110990000, 398.4, 64.2)
ON CONFLICT (code) DO NOTHING;

-- Additional countries referenced in precedents but not in the 17 profiles
INSERT INTO countries (id, code, name, region, income_level, population, gdp_usd_billions, climate_vulnerability_score)
VALUES
    (uuid_generate_v4()::text, 'SLE', 'Sierra Leone',            'Sub-Saharan Africa',         'LIC',   8420000,   4.3,   79.1),
    (uuid_generate_v4()::text, 'MWI', 'Malawi',                  'Sub-Saharan Africa',         'LIC',   20090000,  12.6,  80.3),
    (uuid_generate_v4()::text, 'SOM', 'Somalia',                 'Sub-Saharan Africa',         'LIC',   17070000,  8.1,   88.5),
    (uuid_generate_v4()::text, 'MDG', 'Madagascar',              'Sub-Saharan Africa',         'LIC',   29610000,  14.6,  82.1),
    (uuid_generate_v4()::text, 'GRD', 'Grenada',                 'Latin America & Caribbean',  'UMIC',  125000,    1.3,   74.8),
    (uuid_generate_v4()::text, 'STP', 'São Tomé and Príncipe',   'Sub-Saharan Africa',         'LMIC',  227000,    0.5,   76.2)
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- 5. SEED DATA - PRECEDENTS (20 historical cases)
-- ============================================================
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, npv_reduction_percent, includes_climate_clause, terms_summary, source_document)
VALUES
    -- Ghana 2020 - Paris Club flow
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'GHA'), 2020, 1800, 'Paris Club', 'Flow', 25,
     'Partial', 'Paris Club flow treatment with climate adaptation considerations', 'Paris Club Agreed Minutes - Ghana 2020'),

    -- Zambia 2023 - Common Framework (landmark)
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'ZMB'), 2023, 4200, 'Official + Private', 'Common Framework', 35,
     'Yes', 'First Common Framework case with explicit climate clauses for copper transition', 'Common Framework Agreement - Zambia 2023'),

    -- Ethiopia 2021 - Common Framework
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'ETH'), 2021, 3500, 'Official', 'Common Framework', 30,
     'Partial', 'Common Framework treatment following COVID-19 with agricultural sustainability provisions', 'Common Framework - Ethiopia 2021'),

    -- Chad 2022 - Common Framework
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'TCD'), 2022, 2100, 'Official', 'Common Framework', 28,
     'Yes', 'Common Framework with climate vulnerability considerations for Sahel region', 'Common Framework - Chad 2022'),

    -- Sierra Leone 2018 - HIPC
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'SLE'), 2018, 1200, 'Paris Club', 'HIPC', 45,
     'No', 'HIPC completion point with substantial debt relief post-Ebola crisis', 'HIPC Completion - Sierra Leone 2018'),

    -- Argentina 2020 - Private stock
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'ARG'), 2020, 65000, 'Private', 'Stock', 35,
     'No', 'Major private creditor restructuring with maturity extension', 'Argentina Bond Exchange 2020'),

    -- Lebanon 2020 - Default
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'LBN'), 2020, 31000, 'Private', 'Default', 0,
     'No', 'Eurobond default amid economic crisis', 'Lebanon Sovereign Default 2020'),

    -- Malawi 2019 - Paris Club flow
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'MWI'), 2019, 950, 'Paris Club', 'Flow', 20,
     'Partial', 'Paris Club flow treatment with agricultural resilience provisions', 'Paris Club - Malawi 2019'),

    -- Somalia 2020 - HIPC
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'SOM'), 2020, 5200, 'Paris Club + Official', 'HIPC', 90,
     'Yes', 'HIPC decision point after decades of conflict with climate adaptation focus', 'HIPC Decision Point - Somalia 2020'),

    -- Senegal 2019 - Paris Club flow
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'SEN'), 2019, 800, 'Paris Club', 'Flow', 15,
     'Partial', 'Paris Club flow with coastal resilience provisions', 'Paris Club - Senegal 2019'),

    -- Kenya 2021 - Bilateral
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'KEN'), 2021, 5600, 'Official', 'Bilateral', 18,
     'Yes', 'Bilateral restructuring with China and official creditors including climate adaptation provisions for drought resilience', 'Bilateral Agreement - Kenya 2021'),

    -- Ecuador 2020 - Private stock with climate clause
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'ECU'), 2020, 17400, 'Private', 'Stock', 32,
     'Yes', 'Comprehensive bond restructuring with innovative Galapagos conservation clause linking debt relief to marine protection', 'Ecuador Bond Restructuring 2020'),

    -- Suriname 2023 - Private stock
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'SUR'), 2023, 675, 'Private', 'Stock', 28,
     'Yes', 'Eurobond restructuring with rainforest protection clauses for Amazon conservation', 'Suriname Bond Restructuring 2023'),

    -- Madagascar 2021 - Paris Club flow
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'MDG'), 2021, 850, 'Paris Club', 'Flow', 22,
     'Yes', 'Paris Club flow treatment with biodiversity protection provisions for unique endemic species', 'Paris Club - Madagascar 2021'),

    -- Mozambique 2019 - Bilateral
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'MOZ'), 2019, 2300, 'Official', 'Bilateral', 20,
     'Partial', 'Bilateral restructuring following cyclone disasters with climate resilience infrastructure provisions', 'Bilateral Agreement - Mozambique 2019'),

    -- Pakistan 2019 - Bilateral
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'PAK'), 2019, 6200, 'Official', 'Bilateral', 15,
     'No', 'Bilateral restructuring with Saudi Arabia and UAE for balance of payments support', 'Bilateral Agreement - Pakistan 2019'),

    -- Bangladesh 2020 - Bilateral
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'BGD'), 2020, 3100, 'Official', 'Bilateral', 12,
     'Yes', 'Bilateral agreement with climate vulnerability provisions for coastal flooding and cyclone adaptation', 'Bilateral Agreement - Bangladesh 2020'),

    -- Belize 2021 - Blue Bond (innovative)
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'BLZ'), 2021, 553, 'Private', 'Blue Bond', 45,
     'Yes', 'Innovative blue bond with 30% debt reduction in exchange for marine conservation commitments protecting coral reefs', 'Belize Blue Bond 2021'),

    -- Grenada 2022 - Private stock
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'GRD'), 2022, 240, 'Private', 'Stock', 25,
     'Yes', 'Hurricane resilience bond with automatic payment suspension clauses for natural disasters', 'Grenada Climate Bond 2022'),

    -- São Tomé and Príncipe 2022 - HIPC
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'STP'), 2022, 85, 'Paris Club', 'HIPC', 50,
     'Partial', 'HIPC completion with ocean conservation provisions for small island developing state', 'HIPC Completion - STP 2022')
ON CONFLICT DO NOTHING;

-- ============================================================
-- 6. SEED DATA - DEBT RECORDS (5 countries, 2023 data)
-- ============================================================
INSERT INTO debt_data (id, country_id, year, debt_service_usd_millions, gdp_usd_millions, government_revenue_usd_millions, healthcare_salary_usd_thousands, school_cost_usd_thousands, climate_budget_usd_millions, source_debt, source_healthcare, source_climate, data_quality_score)
VALUES
    -- Ghana
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'GHA'), 2023, 2500.0, 77000.0, 15000.0, 20.0, 400.0, 200.0,
     'IMF World Economic Outlook 2023', 'WHO Global Health Expenditure Database 2023', 'UNFCCC National Communications Ghana 2023', 85.0),

    -- Kenya
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'KEN'), 2023, 3200.0, 118000.0, 20000.0, 18.0, 350.0, 250.0,
     'IMF World Economic Outlook 2023', 'WHO Global Health Expenditure Database 2023', 'UNFCCC National Communications Kenya 2023', 88.0),

    -- Zambia
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'ZMB'), 2023, 1800.0, 29000.0, 6500.0, 15.0, 300.0, 150.0,
     'IMF World Economic Outlook 2023', 'WHO Global Health Expenditure Database 2023', 'UNFCCC National Communications Zambia 2023', 82.0),

    -- Pakistan
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'PAK'), 2023, 8500.0, 375000.0, 50000.0, 12.0, 250.0, 400.0,
     'IMF World Economic Outlook 2023', 'WHO Global Health Expenditure Database 2023', 'UNFCCC National Communications Pakistan 2023', 80.0),

    -- Bangladesh
    (uuid_generate_v4()::text, (SELECT id FROM countries WHERE code = 'BGD'), 2023, 3800.0, 460000.0, 55000.0, 10.0, 200.0, 500.0,
     'IMF World Economic Outlook 2023', 'WHO Global Health Expenditure Database 2023', 'UNFCCC National Communications Bangladesh 2023', 83.0)
ON CONFLICT ON CONSTRAINT unique_country_year DO NOTHING;

-- ============================================================
-- 7. SEED DATA - DEMO API KEY
-- ============================================================
-- Demo key for testing: bf_demo0123456789_DemoSecretForBorrowersForum12345
-- key_id: demo0123456789
-- secret: DemoSecretForBorrowersForum12345
-- SHA-256 hash of secret: aa54e85a16debbc58d7b9331eda2f545873b94fec9691fcba8785d6ec4fb4e53
INSERT INTO api_keys (id, key_id, key_hash, name, owner, permissions, is_active, rate_limit_per_minute, usage_count)
VALUES (
    uuid_generate_v4()::text,
    'demo0123456789',
    'aa54e85a16debbc58d7b9331eda2f545873b94fec9691fcba8785d6ec4fb4e53',
    'ITU Demo Key',
    'Borrowers Forum Team',
    'admin',
    TRUE,
    200,
    0
)
ON CONFLICT (key_id) DO NOTHING;

-- ============================================================
-- 8. VERIFICATION QUERIES
-- ============================================================
SELECT 'countries' AS table_name, COUNT(*) AS row_count FROM countries
UNION ALL
SELECT 'precedents', COUNT(*) FROM precedents
UNION ALL
SELECT 'debt_data', COUNT(*) FROM debt_data
UNION ALL
SELECT 'api_keys', COUNT(*) FROM api_keys
ORDER BY table_name;
