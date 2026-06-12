-- ============================================================
-- Borrowers Forum: Seed 20 countries + 23 precedents
-- Safe to run multiple times (ON CONFLICT DO NOTHING)
-- ============================================================

BEGIN;

-- ============================================================
-- COUNTRIES (20)
-- ============================================================

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('a135c424-312f-4681-95a0-a6c0daf06c57', 'Ghana', 'GHA', 'Sub-Saharan Africa', 'LMIC', 33480000, 76.4, 68.5, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('332995a4-d19a-49b9-8c28-496b17a12e56', 'Kenya', 'KEN', 'Sub-Saharan Africa', 'LMIC', 54030000, 115.4, 72.3, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('dcdbeabc-efc2-44db-b5a8-ee6d781c47cb', 'Zambia', 'ZMB', 'Sub-Saharan Africa', 'LMIC', 20020000, 29.8, 75.1, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('18c454bd-e9f3-44d0-84bc-c697d2d04b50', 'Pakistan', 'PAK', 'South Asia', 'LMIC', 235820000, 374.9, 81.7, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('adb25c89-3b1b-4a60-a225-4edf9abc3fc7', 'Bangladesh', 'BGD', 'South Asia', 'LMIC', 171190000, 460.2, 86.4, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('49ca3e07-a177-4b1f-8f0a-62ffb2b6f603', 'Ethiopia', 'ETH', 'Sub-Saharan Africa', 'LIC', 123380000, 126.8, 77.9, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('3a7bfd3b-18cb-4b60-8ee3-ce8b554d01cb', 'Chad', 'TCD', 'Sub-Saharan Africa', 'LIC', 17720000, 11.8, 82.7, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('2d941c26-2b82-4d22-aafc-4c391a208d98', 'Argentina', 'ARG', 'Latin America & Caribbean', 'UMIC', 45810000, 632.8, 52.3, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('54c666d9-7a3c-4cc5-8401-4b82717e2bed', 'Lebanon', 'LBN', 'Middle East & North Africa', 'UMIC', 5490000, 21.8, 61.9, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('c971bf7b-43a4-4a40-90af-528f75b6c5a6', 'Senegal', 'SEN', 'Sub-Saharan Africa', 'LMIC', 17320000, 27.6, 69.8, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('941d886a-5174-4d22-8a21-6286f3cb2332', 'Ecuador', 'ECU', 'Latin America & Caribbean', 'UMIC', 18000000, 115.0, 66.4, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('2aecc1d4-c9d2-4450-9291-87be9c6bdf42', 'Suriname', 'SUR', 'Latin America & Caribbean', 'UMIC', 618000, 3.6, 71.4, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('df20962e-9826-40bd-9b1f-2a6d188e6f60', 'Mozambique', 'MOZ', 'Sub-Saharan Africa', 'LIC', 32970000, 20.5, 84.2, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('805fb86b-a371-402c-8539-c7b844bc3b3e', 'Belize', 'BLZ', 'Latin America & Caribbean', 'UMIC', 405000, 3.2, 78.5, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('771a030f-f41e-4df2-9a4c-24fda26a8322', 'Sierra Leone', 'SLE', 'Sub-Saharan Africa', 'LIC', 8610000, 4.2, 78.0, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('a4b1a274-15d5-455b-8ce6-4d1b85d1cd68', 'Malawi', 'MWI', 'Sub-Saharan Africa', 'LIC', 20400000, 12.6, 80.0, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('2ef57b91-aa12-461c-a844-ce3628f87bf6', 'Somalia', 'SOM', 'Sub-Saharan Africa', 'LIC', 17100000, 8.1, 85.0, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('67ce2b1c-d006-4a55-95da-68ceed0e544f', 'Madagascar', 'MDG', 'Sub-Saharan Africa', 'LIC', 29600000, 15.1, 79.0, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('d726d1eb-56e4-4153-9f79-a82c851750f4', 'Grenada', 'GRD', 'Latin America & Caribbean', 'UMIC', 125000, 1.3, 72.0, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

INSERT INTO countries (id, name, code, region, income_level, population, gdp_usd_billions, climate_vulnerability_score, created_at, updated_at)
VALUES ('2415c233-500d-4fa4-bf47-f9ce95044ca1', 'São Tomé and Príncipe', 'STP', 'Sub-Saharan Africa', 'LMIC', 227000, 0.6, 75.0, '2026-03-19T00:00:00', '2026-03-19T00:00:00')
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- PRECEDENTS (23)
-- ============================================================

-- 1. GHA 2020 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'd783d93c-7ad1-4629-bee2-1a19f4b716d6', (SELECT id FROM countries WHERE code = 'GHA'), 2020, 1800.0, 'Paris Club', 'Flow', 36, 25.0, 12, 2.5, 'Paris Club flow treatment providing 3-year debt service deferral with 1-year grace period. Interest rate reduced to 2.5%.', 'IMF program compliance required. Quarterly reporting on fiscal reforms. No new non-concessional borrowing.', 'Successfully completed. Debt service reduced by 25% NPV. Allowed fiscal space for COVID-19 response.', 'Partial', 'Included provisions for climate adaptation spending protection.', 'https://clubdeparis.org/en/communications/press-release/ghana-2020', 'Paris Club Agreed Minutes - Ghana 2020', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'GHA'
    AND p.year = 2020
    AND p.creditor_type = 'Paris Club'
    AND p.treatment_type = 'Flow'
);

-- 2. ZMB 2023 Common Framework
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'dd82daf3-d2ff-45c6-a160-bf1904f678b9', (SELECT id FROM countries WHERE code = 'ZMB'), 2023, 4200.0, 'Mixed', 'Common Framework', 60, 35.0, 36, 2.0, 'G20 Common Framework treatment. First successful case. Deep NPV reduction with extended grace period and low interest rate.', 'IMF Extended Credit Facility required. Transparency requirements for all creditors. Comparability of treatment clause.', 'Landmark success. Restored debt sustainability. Set precedent for Common Framework. Strong creditor coordination achieved.', 'Yes', 'Explicit climate clauses for copper transition. Protected climate spending floors. Linked to NDC targets.', 'https://www.imf.org/en/News/Articles/2023/06/22/zambia-common-framework', 'Common Framework Agreement - Zambia 2023', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'ZMB'
    AND p.year = 2023
    AND p.creditor_type = 'Mixed'
    AND p.treatment_type = 'Common Framework'
);

-- 3. ETH 2021 Common Framework
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'ce5de6c9-e12d-4bc1-a118-851feba54201', (SELECT id FROM countries WHERE code = 'ETH'), 2021, 3500.0, 'Official', 'Common Framework', 36, 30.0, 18, 2.5, 'Common Framework treatment following COVID-19 with agricultural sustainability provisions. Creditor committee formed mid-2021.', 'IMF program participation. Fiscal consolidation. Conflict resolution progress required.', 'Protracted process due to civil conflict. Creditor committee formed but full agreement delayed. Partial relief achieved.', 'Partial', 'Agricultural sustainability provisions included. Climate adaptation for drought-prone regions.', 'https://www.imf.org/en/Countries/ETH', 'Common Framework Application - Ethiopia 2021', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'ETH'
    AND p.year = 2021
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Common Framework'
);

-- 4. TCD 2022 Common Framework
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'ac11c16e-d2bb-485c-9af6-34e8a8ebecd6', (SELECT id FROM countries WHERE code = 'TCD'), 2022, 2100.0, 'Official', 'Common Framework', 48, 28.0, 24, 2.5, 'Common Framework treatment with climate vulnerability considerations for Sahel region. Oil-linked repayment mechanism.', 'IMF program compliance. Oil revenue transparency. Public investment reforms. Debt management capacity building.', 'Agreement reached after protracted negotiations. Oil price contingency mechanism included. Debt sustainability partially restored.', 'Yes', 'Climate vulnerability considerations for Sahel region. Lake Chad restoration spending protected.', 'https://www.imf.org/en/Countries/TCD', 'Common Framework Agreement - Chad 2022', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'TCD'
    AND p.year = 2022
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Common Framework'
);

-- 5. SLE 2018 HIPC
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '85412ce9-bd6c-4c8b-9d3b-107b4bdff35a', (SELECT id FROM countries WHERE code = 'SLE'), 2018, 1200.0, 'Paris Club', 'HIPC', 36, 45.0, 24, 1.5, 'HIPC completion point with substantial debt relief post-Ebola crisis. Paris Club bilateral treatment.', 'PRSP implementation. Health sector reforms post-Ebola. Revenue mobilization. Governance improvements.', 'Successfully completed HIPC process. Significant fiscal space created. Health sector recovery supported.', 'No', NULL, 'https://www.imf.org/en/About/Factsheets/Sheets/2023/HIPC', 'HIPC Completion Point - Sierra Leone 2018', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'SLE'
    AND p.year = 2018
    AND p.creditor_type = 'Paris Club'
    AND p.treatment_type = 'HIPC'
);

-- 6. ARG 2020 Stock
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '85c8c62f-39b3-4ac6-ab99-bf37c11c012d', (SELECT id FROM countries WHERE code = 'ARG'), 2020, 65000.0, 'Private', 'Stock', 48, 35.0, 30, 3.5, 'Major private creditor restructuring with maturity extension. New bonds issued with lower coupons and extended maturities.', 'IMF Extended Fund Facility compliance. Fiscal primary surplus targets. Central bank independence reforms.', 'Agreement reached with main bondholder groups. Reduced near-term debt service burden. Long-term sustainability challenges remain.', 'No', NULL, 'https://www.argentina.gob.ar/economia/finanzas', 'Argentina Debt Exchange Offer 2020', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'ARG'
    AND p.year = 2020
    AND p.creditor_type = 'Private'
    AND p.treatment_type = 'Stock'
);

-- 7. LBN 2020 Default
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '2c1542d4-9116-4787-a2f9-4e615ec05b47', (SELECT id FROM countries WHERE code = 'LBN'), 2020, 31000.0, 'Private', 'Default', NULL, 0.0, NULL, NULL, 'Eurobond default amid economic crisis. Government ceased payments on all Eurobonds in March 2020.', 'IMF program negotiations ongoing. Banking sector restructuring required. Capital controls in place.', 'Default ongoing. No comprehensive restructuring agreement reached. Economy contracted severely.', 'No', NULL, 'https://www.imf.org/en/Countries/LBN', 'Lebanon Default Documentation 2020', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'LBN'
    AND p.year = 2020
    AND p.creditor_type = 'Private'
    AND p.treatment_type = 'Default'
);

-- 8. MWI 2019 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '571c622c-6ba8-4553-b51e-3ea85a8b3dfa', (SELECT id FROM countries WHERE code = 'MWI'), 2019, 950.0, 'Paris Club', 'Flow', 24, 20.0, 12, 2.0, 'Paris Club flow treatment with agricultural resilience provisions. Debt service deferral to protect development spending.', 'IMF Extended Credit Facility. Agricultural sector reform program. Fiscal discipline commitments.', 'Successfully completed. Enabled continued agricultural investment. Fiscal space preserved during drought period.', 'Partial', 'Agricultural resilience provisions included. Protected spending on climate-adaptive farming programs.', 'https://clubdeparis.org/en/communications/press-release/malawi-2019', 'Paris Club Agreed Minutes - Malawi 2019', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'MWI'
    AND p.year = 2019
    AND p.creditor_type = 'Paris Club'
    AND p.treatment_type = 'Flow'
);

-- 9. SOM 2020 HIPC
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'ff1c03b9-f133-4afe-80ef-f78010fd7440', (SELECT id FROM countries WHERE code = 'SOM'), 2020, 5200.0, 'Official', 'HIPC', 36, 90.0, 36, 0.5, 'HIPC decision point after decades of conflict. Paris Club and other official creditors provided near-total debt relief.', 'Continued IMF engagement. Poverty reduction strategy. Governance and anti-corruption reforms. Security sector stabilization.', 'Historic achievement. Reached HIPC decision point for first time. Massive debt stock reduction enabling fresh start.', 'Yes', 'Climate adaptation focus for drought-prone pastoral communities. Protected humanitarian and resilience spending.', 'https://www.imf.org/en/News/Articles/2020/03/25/pr2098-somalia-imf-executive-board-decision-hipc', 'HIPC Decision Point - Somalia 2020', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'SOM'
    AND p.year = 2020
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'HIPC'
);

-- 10. SEN 2019 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '68ad0b59-9762-442c-8ab8-e32d81f97d66', (SELECT id FROM countries WHERE code = 'SEN'), 2019, 800.0, 'Paris Club', 'Flow', 24, 15.0, 12, 2.5, 'Paris Club flow treatment with coastal resilience provisions. Moderate relief to support development agenda.', 'IMF Policy Support Instrument. Revenue mobilization. Public investment efficiency improvements.', 'Successfully completed. Coastal protection programs maintained. Fiscal position stabilized.', 'Partial', 'Coastal resilience provisions. Protected spending on sea-level rise adaptation and fishing community support.', 'https://clubdeparis.org/en/communications/press-release/senegal-2019', 'Paris Club Agreed Minutes - Senegal 2019', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'SEN'
    AND p.year = 2019
    AND p.creditor_type = 'Paris Club'
    AND p.treatment_type = 'Flow'
);

-- 11. KEN 2021 Bilateral
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '67253447-7682-4d6e-bd3d-c23c487501d9', (SELECT id FROM countries WHERE code = 'KEN'), 2021, 5600.0, 'Official', 'Bilateral', 36, 18.0, 12, 3.0, 'Bilateral restructuring with China and official creditors including climate adaptation provisions for drought resilience and renewable energy transition.', 'Revenue mobilization reforms. Debt transparency commitments. Climate resilience investment plan.', 'Agreement reached with major bilateral creditors. Climate provisions established precedent for region. Debt service profile improved.', 'Yes', 'Climate adaptation provisions for drought resilience and renewable energy transition.', 'https://www.treasury.go.ke/debt-management/', 'Bilateral Restructuring Agreement - Kenya 2021', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'KEN'
    AND p.year = 2021
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Bilateral'
);

-- 12. ECU 2020 Stock
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'd2808b29-4587-41e7-a9ed-62a0d52e5dcd', (SELECT id FROM countries WHERE code = 'ECU'), 2020, 17400.0, 'Private', 'Stock', 60, 32.0, 36, 5.0, 'Comprehensive bond restructuring with innovative Galapagos conservation clause linking debt relief to marine protection targets.', 'IMF Extended Fund Facility. Fiscal reforms. Conservation commitments for Galapagos marine reserve.', 'Successfully completed. Freed $1.1B for Galapagos conservation. Established model for debt-for-nature swaps.', 'Yes', 'Innovative Galapagos conservation clause. Debt relief linked to marine protection targets and biodiversity commitments.', 'https://www.finanzas.gob.ec/', 'Ecuador Bond Exchange - Galapagos Conservation 2020', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'ECU'
    AND p.year = 2020
    AND p.creditor_type = 'Private'
    AND p.treatment_type = 'Stock'
);

-- 13. SUR 2023 Stock
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '285c87c9-877a-4c02-b500-d408542611e8', (SELECT id FROM countries WHERE code = 'SUR'), 2023, 675.0, 'Private', 'Stock', 36, 28.0, 18, 4.5, 'Eurobond restructuring with rainforest protection clauses for Amazon conservation and indigenous rights.', 'IMF Extended Fund Facility. Amazon conservation commitments. Indigenous rights protections. Fiscal reforms.', 'Agreement reached with bondholders. Rainforest protection provisions included. Fiscal sustainability path established.', 'Yes', 'Rainforest protection clauses for Amazon conservation and indigenous rights.', 'https://www.imf.org/en/Countries/SUR', 'Suriname Eurobond Restructuring 2023', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'SUR'
    AND p.year = 2023
    AND p.creditor_type = 'Private'
    AND p.treatment_type = 'Stock'
);

-- 14. MDG 2021 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'aaff9333-29f8-4973-bd03-c1eec09a52b0', (SELECT id FROM countries WHERE code = 'MDG'), 2021, 850.0, 'Paris Club', 'Flow', 24, 22.0, 12, 2.0, 'Paris Club flow treatment with biodiversity protection provisions for unique endemic species.', 'IMF Extended Credit Facility. Biodiversity conservation commitments. Forest protection program. Fiscal reforms.', 'Successfully completed. Biodiversity protection provisions implemented. Fiscal space for conservation created.', 'Yes', 'Biodiversity protection provisions for unique endemic species. Forest conservation spending protected.', 'https://clubdeparis.org/en/communications/press-release/madagascar-2021', 'Paris Club Agreed Minutes - Madagascar 2021', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'MDG'
    AND p.year = 2021
    AND p.creditor_type = 'Paris Club'
    AND p.treatment_type = 'Flow'
);

-- 15. MOZ 2019 Bilateral
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'd5b32a50-b480-4df7-995a-b4ceb9975858', (SELECT id FROM countries WHERE code = 'MOZ'), 2019, 2300.0, 'Official', 'Bilateral', 36, 20.0, 18, 2.5, 'Bilateral restructuring following cyclone disasters with climate resilience infrastructure provisions.', 'Post-cyclone reconstruction plan. Debt transparency reforms. Infrastructure resilience standards.', 'Agreement reached with bilateral creditors. Reconstruction progressed. Climate-resilient infrastructure standards adopted.', 'Partial', 'Climate resilience infrastructure provisions following Cyclone Idai and Kenneth. Disaster preparedness spending protected.', 'https://www.imf.org/en/Countries/MOZ', 'Bilateral Restructuring - Mozambique 2019', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'MOZ'
    AND p.year = 2019
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Bilateral'
);

-- 16. PAK 2019 Bilateral
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '488275f3-8e2d-449c-b00e-d399701dc0cd', (SELECT id FROM countries WHERE code = 'PAK'), 2019, 6200.0, 'Official', 'Bilateral', 36, 15.0, 12, 3.5, 'Bilateral restructuring with Saudi Arabia and UAE for balance of payments support.', 'IMF Extended Fund Facility. Fiscal consolidation. Energy sector reforms. Tax base broadening.', 'Successfully completed. Balance of payments stabilized. Bilateral relationships preserved.', 'No', NULL, 'https://www.finance.gov.pk/', 'Bilateral Restructuring - Pakistan 2019', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'PAK'
    AND p.year = 2019
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Bilateral'
);

-- 17. BGD 2020 Bilateral
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '0315104a-802f-4493-8f96-4f93cd213aa0', (SELECT id FROM countries WHERE code = 'BGD'), 2020, 3100.0, 'Official', 'Bilateral', 24, 12.0, 12, 2.0, 'Bilateral agreement with climate vulnerability provisions for coastal flooding and cyclone adaptation.', 'Climate adaptation investment plan. Coastal protection commitments. Budget transparency on climate spending.', 'Successfully completed. Climate adaptation programs maintained during COVID-19. Coastal protection investments continued.', 'Yes', 'Climate vulnerability provisions for coastal flooding and cyclone adaptation.', 'https://mof.gov.bd/', 'Bilateral Agreement - Bangladesh 2020', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'BGD'
    AND p.year = 2020
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Bilateral'
);

-- 18. BLZ 2021 Blue Bond
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '8f621978-80b3-4fe8-a60b-62c07f0c7a08', (SELECT id FROM countries WHERE code = 'BLZ'), 2021, 553.0, 'Private', 'Blue Bond', 228, 45.0, 60, 4.0, 'Innovative blue bond with 30% debt reduction in exchange for marine conservation commitments protecting coral reefs.', 'Marine conservation commitments. Belize Barrier Reef protection. 30% of ocean waters protected. Endowment fund creation.', 'Landmark deal. $553M superbond retired. Marine conservation commitments legally binding. Model for blue economy finance.', 'Yes', 'Marine conservation commitments protecting coral reefs. Belize Barrier Reef World Heritage Site protections.', 'https://www.nature.org/en-us/about-us/where-we-work/caribbean/belize/', 'Belize Blue Bond - TNC 2021', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'BLZ'
    AND p.year = 2021
    AND p.creditor_type = 'Private'
    AND p.treatment_type = 'Blue Bond'
);

-- 19. GRD 2022 Stock
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '83834b50-6ec5-4c9f-b678-f5fa6ec365f4', (SELECT id FROM countries WHERE code = 'GRD'), 2022, 240.0, 'Private', 'Stock', 36, 25.0, 12, 5.0, 'Hurricane resilience bond with automatic payment suspension clauses for natural disasters.', 'Disaster preparedness plan. Building code enforcement. Climate resilience investment targets.', 'Successfully restructured. Hurricane clause provides automatic fiscal breathing room. Model for SIDS climate-resilient debt.', 'Yes', 'Automatic payment suspension clauses triggered by qualifying natural disasters. Hurricane resilience provisions.', 'https://www.gov.gd/', 'Grenada Hurricane Resilience Bond 2022', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'GRD'
    AND p.year = 2022
    AND p.creditor_type = 'Private'
    AND p.treatment_type = 'Stock'
);

-- 20. STP 2022 HIPC
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT '9b899726-98f0-40fa-9c28-9f70aea6d140', (SELECT id FROM countries WHERE code = 'STP'), 2022, 85.0, 'Paris Club', 'HIPC', 24, 50.0, 18, 1.0, 'HIPC completion with ocean conservation provisions for small island developing state.', 'PRSP implementation. Ocean conservation commitments. Fisheries management reforms. Public financial management improvements.', 'HIPC completion point reached. Significant debt stock reduction. Ocean conservation framework established.', 'Partial', 'Ocean conservation provisions for small island developing state. Marine resource protection spending safeguarded.', 'https://www.imf.org/en/About/Factsheets/Sheets/2023/HIPC', 'HIPC Completion Point - São Tomé and Príncipe 2022', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'STP'
    AND p.year = 2022
    AND p.creditor_type = 'Paris Club'
    AND p.treatment_type = 'HIPC'
);

-- 21. PAK 2023 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'e9769fd8-9f9d-4cce-bcd1-6a2289e39e9a', (SELECT id FROM countries WHERE code = 'PAK'), 2023, 5200.0, 'Official', 'Flow', 36, 18.0, 18, 3.5, 'Bilateral flow treatment following devastating 2022 floods. Emergency debt relief to support reconstruction and climate resilience.', 'Flood reconstruction program. Climate resilience investments. Energy sector reforms. IMF program track record.', 'Ongoing. Initial liquidity relief successful. Reconstruction progressing. Climate adaptation planning initiated.', 'Yes', 'Explicit climate emergency recognition. Protected disaster response and climate resilience spending. Linked to climate adaptation plan.', 'https://www.imf.org/en/Countries/PAK', 'Emergency Treatment - Pakistan Floods 2023', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'PAK'
    AND p.year = 2023
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Flow'
);

-- 22. BGD 2017 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'cccbdbad-6ca9-4763-b8b6-290ccc9f43ab', (SELECT id FROM countries WHERE code = 'BGD'), 2017, 1500.0, 'Official', 'Flow', 24, 12.0, 12, 2.5, 'Concessional rescheduling following Rohingya refugee crisis. Humanitarian emergency treatment with debt service relief.', 'Refugee response program. International humanitarian coordination. Budget transparency on refugee spending.', 'Successfully completed. Enabled humanitarian response without fiscal destabilization. International solidarity demonstrated.', 'Partial', 'Recognized climate-migration nexus. Protected refugee response spending including climate adaptation for refugee-hosting areas.', 'https://mof.gov.bd/', 'Humanitarian Emergency Treatment - Bangladesh 2017', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'BGD'
    AND p.year = 2017
    AND p.creditor_type = 'Official'
    AND p.treatment_type = 'Flow'
);

-- 23. KEN 2021 Flow
INSERT INTO precedents (id, country_id, year, debt_amount_millions, creditor_type, treatment_type, duration_months, npv_reduction_percent, grace_period_months, interest_rate_percent, terms_summary, conditions, outcomes, includes_climate_clause, climate_notes, source_url, source_document, created_at)
SELECT 'da3edfe3-f6ec-4cf7-b049-1fdb665681da', (SELECT id FROM countries WHERE code = 'KEN'), 2021, 2500.0, 'Mixed', 'Flow', 24, 20.0, 6, 3.0, 'Mixed creditor treatment combining Paris Club and commercial creditors. Flow rescheduling with comparable treatment.', 'Debt sustainability analysis required. Comparable treatment clause for all creditors. Revenue mobilization targets.', 'Partial success. Paris Club completed but commercial creditors delayed. Liquidity improved but sustainability challenges remain.', 'Yes', 'Explicit carve-out for climate adaptation spending. Green bond proceeds protected from restructuring.', 'https://www.treasury.go.ke/debt-management/', 'Paris Club - Kenya Treatment 2021', '2026-03-19T00:00:00'
WHERE NOT EXISTS (
  SELECT 1 FROM precedents p
  JOIN countries c ON p.country_id = c.id
  WHERE c.code = 'KEN'
    AND p.year = 2021
    AND p.creditor_type = 'Mixed'
    AND p.treatment_type = 'Flow'
);

COMMIT;
