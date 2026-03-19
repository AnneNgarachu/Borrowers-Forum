"""
Seed All Precedents + Required Countries
==========================================

Unified seed script that populates the database with:
- 20 countries (5 existing + 15 new) required by the precedent dataset
- 23 precedents (20 canonical cases from frontend + 3 backend-only extras)

This is the single source of truth. Run it to bring a fresh or existing
database to the canonical state.

Usage:
    python -m src.utils.seed_all_precedents
"""

from datetime import datetime
from sqlalchemy import select
from src.services.database import SessionLocal, init_database
from src.models.debt_data import Country, Precedent


# ============================================================
# COUNTRY DATA
# Sources: World Bank, IMF, UN (2023 estimates)
# income_level uses World Bank codes: LIC, LMIC, UMIC, HIC
# climate_vulnerability_score: ND-GAIN index 0-100
# ============================================================

COUNTRIES = [
    # --- Already in backend (5) — update to match frontend countries-data.ts ---
    {"code": "GHA", "name": "Ghana",       "region": "Sub-Saharan Africa",         "income_level": "LMIC", "population": 33480000,  "gdp_usd_billions": 76.4,  "climate_vulnerability_score": 68.5},
    {"code": "KEN", "name": "Kenya",       "region": "Sub-Saharan Africa",         "income_level": "LMIC", "population": 54030000,  "gdp_usd_billions": 115.4, "climate_vulnerability_score": 72.3},
    {"code": "ZMB", "name": "Zambia",      "region": "Sub-Saharan Africa",         "income_level": "LMIC", "population": 20020000,  "gdp_usd_billions": 29.8,  "climate_vulnerability_score": 75.1},
    {"code": "PAK", "name": "Pakistan",    "region": "South Asia",                 "income_level": "LMIC", "population": 235820000, "gdp_usd_billions": 374.9, "climate_vulnerability_score": 81.7},
    {"code": "BGD", "name": "Bangladesh",  "region": "South Asia",                 "income_level": "LMIC", "population": 171190000, "gdp_usd_billions": 460.2, "climate_vulnerability_score": 86.4},

    # --- New: from frontend countries-data.ts (9) ---
    {"code": "ETH", "name": "Ethiopia",    "region": "Sub-Saharan Africa",         "income_level": "LIC",  "population": 123380000, "gdp_usd_billions": 126.8, "climate_vulnerability_score": 77.9},
    {"code": "TCD", "name": "Chad",        "region": "Sub-Saharan Africa",         "income_level": "LIC",  "population": 17720000,  "gdp_usd_billions": 11.8,  "climate_vulnerability_score": 82.7},
    {"code": "ARG", "name": "Argentina",   "region": "Latin America & Caribbean",  "income_level": "UMIC", "population": 45810000,  "gdp_usd_billions": 632.8, "climate_vulnerability_score": 52.3},
    {"code": "LBN", "name": "Lebanon",     "region": "Middle East & North Africa", "income_level": "UMIC", "population": 5490000,   "gdp_usd_billions": 21.8,  "climate_vulnerability_score": 61.9},
    {"code": "SEN", "name": "Senegal",     "region": "Sub-Saharan Africa",         "income_level": "LMIC", "population": 17320000,  "gdp_usd_billions": 27.6,  "climate_vulnerability_score": 69.8},
    {"code": "ECU", "name": "Ecuador",     "region": "Latin America & Caribbean",  "income_level": "UMIC", "population": 18000000,  "gdp_usd_billions": 115.0, "climate_vulnerability_score": 66.4},
    {"code": "SUR", "name": "Suriname",    "region": "Latin America & Caribbean",  "income_level": "UMIC", "population": 618000,    "gdp_usd_billions": 3.6,   "climate_vulnerability_score": 71.4},
    {"code": "MOZ", "name": "Mozambique",  "region": "Sub-Saharan Africa",         "income_level": "LIC",  "population": 32970000,  "gdp_usd_billions": 20.5,  "climate_vulnerability_score": 84.2},
    {"code": "BLZ", "name": "Belize",      "region": "Latin America & Caribbean",  "income_level": "UMIC", "population": 405000,    "gdp_usd_billions": 3.2,   "climate_vulnerability_score": 78.5},

    # --- New: not in frontend countries-data.ts, estimated from World Bank 2023 (6) ---
    {"code": "SLE", "name": "Sierra Leone",           "region": "Sub-Saharan Africa",        "income_level": "LIC",  "population": 8610000,  "gdp_usd_billions": 4.2,  "climate_vulnerability_score": 78.0},
    {"code": "MWI", "name": "Malawi",                 "region": "Sub-Saharan Africa",        "income_level": "LIC",  "population": 20400000, "gdp_usd_billions": 12.6, "climate_vulnerability_score": 80.0},
    {"code": "SOM", "name": "Somalia",                 "region": "Sub-Saharan Africa",        "income_level": "LIC",  "population": 17100000, "gdp_usd_billions": 8.1,  "climate_vulnerability_score": 85.0},
    {"code": "MDG", "name": "Madagascar",              "region": "Sub-Saharan Africa",        "income_level": "LIC",  "population": 29600000, "gdp_usd_billions": 15.1, "climate_vulnerability_score": 79.0},
    {"code": "GRD", "name": "Grenada",                 "region": "Latin America & Caribbean", "income_level": "UMIC", "population": 125000,   "gdp_usd_billions": 1.3,  "climate_vulnerability_score": 72.0},
    {"code": "STP", "name": "São Tomé and Príncipe",   "region": "Sub-Saharan Africa",        "income_level": "LMIC", "population": 227000,   "gdp_usd_billions": 0.6,  "climate_vulnerability_score": 75.0},
]


# ============================================================
# PRECEDENT DATA
#
# IDs 1-20: canonical dataset (matches frontend precedents-data.ts)
# IDs 21-23: backend-only extras (different events for PAK, BGD, KEN)
#
# Every record that also exists in the frontend shares exactly the
# same year, debt_amount_millions, creditor_type, treatment_type,
# npv_reduction_percent, and includes_climate_clause values.
# ============================================================

PRECEDENTS = [
    # ------------------------------------------------------------------
    # 1. Ghana 2020 — Paris Club Flow
    # ------------------------------------------------------------------
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
        "climate_notes": "Included provisions for climate adaptation spending protection.",
        "source_url": "https://clubdeparis.org/en/communications/press-release/ghana-2020",
        "source_document": "Paris Club Agreed Minutes - Ghana 2020",
    },
    # ------------------------------------------------------------------
    # 2. Zambia 2023 — Common Framework (resolved: year 2023, amount $4,200M)
    # ------------------------------------------------------------------
    {
        "country_code": "ZMB",
        "year": 2023,
        "debt_amount_millions": 4200.0,
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
        "climate_notes": "Explicit climate clauses for copper transition. Protected climate spending floors. Linked to NDC targets.",
        "source_url": "https://www.imf.org/en/News/Articles/2023/06/22/zambia-common-framework",
        "source_document": "Common Framework Agreement - Zambia 2023",
    },
    # ------------------------------------------------------------------
    # 3. Ethiopia 2021 — Common Framework
    # ------------------------------------------------------------------
    {
        "country_code": "ETH",
        "year": 2021,
        "debt_amount_millions": 3500.0,
        "creditor_type": "Official",
        "treatment_type": "Common Framework",
        "duration_months": 36,
        "npv_reduction_percent": 30.0,
        "grace_period_months": 18,
        "interest_rate_percent": 2.5,
        "terms_summary": "Common Framework treatment following COVID-19 with agricultural sustainability provisions. Creditor committee formed mid-2021.",
        "conditions": "IMF program participation. Fiscal consolidation. Conflict resolution progress required.",
        "outcomes": "Protracted process due to civil conflict. Creditor committee formed but full agreement delayed. Partial relief achieved.",
        "includes_climate_clause": "Partial",
        "climate_notes": "Agricultural sustainability provisions included. Climate adaptation for drought-prone regions.",
        "source_url": "https://www.imf.org/en/Countries/ETH",
        "source_document": "Common Framework Application - Ethiopia 2021",
    },
    # ------------------------------------------------------------------
    # 4. Chad 2022 — Common Framework
    # ------------------------------------------------------------------
    {
        "country_code": "TCD",
        "year": 2022,
        "debt_amount_millions": 2100.0,
        "creditor_type": "Official",
        "treatment_type": "Common Framework",
        "duration_months": 48,
        "npv_reduction_percent": 28.0,
        "grace_period_months": 24,
        "interest_rate_percent": 2.5,
        "terms_summary": "Common Framework treatment with climate vulnerability considerations for Sahel region. Oil-linked repayment mechanism.",
        "conditions": "IMF program compliance. Oil revenue transparency. Public investment reforms. Debt management capacity building.",
        "outcomes": "Agreement reached after protracted negotiations. Oil price contingency mechanism included. Debt sustainability partially restored.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Climate vulnerability considerations for Sahel region. Lake Chad restoration spending protected.",
        "source_url": "https://www.imf.org/en/Countries/TCD",
        "source_document": "Common Framework Agreement - Chad 2022",
    },
    # ------------------------------------------------------------------
    # 5. Sierra Leone 2018 — HIPC
    # ------------------------------------------------------------------
    {
        "country_code": "SLE",
        "year": 2018,
        "debt_amount_millions": 1200.0,
        "creditor_type": "Paris Club",
        "treatment_type": "HIPC",
        "duration_months": 36,
        "npv_reduction_percent": 45.0,
        "grace_period_months": 24,
        "interest_rate_percent": 1.5,
        "terms_summary": "HIPC completion point with substantial debt relief post-Ebola crisis. Paris Club bilateral treatment.",
        "conditions": "PRSP implementation. Health sector reforms post-Ebola. Revenue mobilization. Governance improvements.",
        "outcomes": "Successfully completed HIPC process. Significant fiscal space created. Health sector recovery supported.",
        "includes_climate_clause": "No",
        "climate_notes": None,
        "source_url": "https://www.imf.org/en/About/Factsheets/Sheets/2023/HIPC",
        "source_document": "HIPC Completion Point - Sierra Leone 2018",
    },
    # ------------------------------------------------------------------
    # 6. Argentina 2020 — Private Stock
    # ------------------------------------------------------------------
    {
        "country_code": "ARG",
        "year": 2020,
        "debt_amount_millions": 65000.0,
        "creditor_type": "Private",
        "treatment_type": "Stock",
        "duration_months": 48,
        "npv_reduction_percent": 35.0,
        "grace_period_months": 30,
        "interest_rate_percent": 3.5,
        "terms_summary": "Major private creditor restructuring with maturity extension. New bonds issued with lower coupons and extended maturities.",
        "conditions": "IMF Extended Fund Facility compliance. Fiscal primary surplus targets. Central bank independence reforms.",
        "outcomes": "Agreement reached with main bondholder groups. Reduced near-term debt service burden. Long-term sustainability challenges remain.",
        "includes_climate_clause": "No",
        "climate_notes": None,
        "source_url": "https://www.argentina.gob.ar/economia/finanzas",
        "source_document": "Argentina Debt Exchange Offer 2020",
    },
    # ------------------------------------------------------------------
    # 7. Lebanon 2020 — Default
    # ------------------------------------------------------------------
    {
        "country_code": "LBN",
        "year": 2020,
        "debt_amount_millions": 31000.0,
        "creditor_type": "Private",
        "treatment_type": "Default",
        "duration_months": None,
        "npv_reduction_percent": 0.0,
        "grace_period_months": None,
        "interest_rate_percent": None,
        "terms_summary": "Eurobond default amid economic crisis. Government ceased payments on all Eurobonds in March 2020.",
        "conditions": "IMF program negotiations ongoing. Banking sector restructuring required. Capital controls in place.",
        "outcomes": "Default ongoing. No comprehensive restructuring agreement reached. Economy contracted severely.",
        "includes_climate_clause": "No",
        "climate_notes": None,
        "source_url": "https://www.imf.org/en/Countries/LBN",
        "source_document": "Lebanon Default Documentation 2020",
    },
    # ------------------------------------------------------------------
    # 8. Malawi 2019 — Paris Club Flow
    # ------------------------------------------------------------------
    {
        "country_code": "MWI",
        "year": 2019,
        "debt_amount_millions": 950.0,
        "creditor_type": "Paris Club",
        "treatment_type": "Flow",
        "duration_months": 24,
        "npv_reduction_percent": 20.0,
        "grace_period_months": 12,
        "interest_rate_percent": 2.0,
        "terms_summary": "Paris Club flow treatment with agricultural resilience provisions. Debt service deferral to protect development spending.",
        "conditions": "IMF Extended Credit Facility. Agricultural sector reform program. Fiscal discipline commitments.",
        "outcomes": "Successfully completed. Enabled continued agricultural investment. Fiscal space preserved during drought period.",
        "includes_climate_clause": "Partial",
        "climate_notes": "Agricultural resilience provisions included. Protected spending on climate-adaptive farming programs.",
        "source_url": "https://clubdeparis.org/en/communications/press-release/malawi-2019",
        "source_document": "Paris Club Agreed Minutes - Malawi 2019",
    },
    # ------------------------------------------------------------------
    # 9. Somalia 2020 — HIPC
    # ------------------------------------------------------------------
    {
        "country_code": "SOM",
        "year": 2020,
        "debt_amount_millions": 5200.0,
        "creditor_type": "Official",
        "treatment_type": "HIPC",
        "duration_months": 36,
        "npv_reduction_percent": 90.0,
        "grace_period_months": 36,
        "interest_rate_percent": 0.5,
        "terms_summary": "HIPC decision point after decades of conflict. Paris Club and other official creditors provided near-total debt relief.",
        "conditions": "Continued IMF engagement. Poverty reduction strategy. Governance and anti-corruption reforms. Security sector stabilization.",
        "outcomes": "Historic achievement. Reached HIPC decision point for first time. Massive debt stock reduction enabling fresh start.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Climate adaptation focus for drought-prone pastoral communities. Protected humanitarian and resilience spending.",
        "source_url": "https://www.imf.org/en/News/Articles/2020/03/25/pr2098-somalia-imf-executive-board-decision-hipc",
        "source_document": "HIPC Decision Point - Somalia 2020",
    },
    # ------------------------------------------------------------------
    # 10. Senegal 2019 — Paris Club Flow
    # ------------------------------------------------------------------
    {
        "country_code": "SEN",
        "year": 2019,
        "debt_amount_millions": 800.0,
        "creditor_type": "Paris Club",
        "treatment_type": "Flow",
        "duration_months": 24,
        "npv_reduction_percent": 15.0,
        "grace_period_months": 12,
        "interest_rate_percent": 2.5,
        "terms_summary": "Paris Club flow treatment with coastal resilience provisions. Moderate relief to support development agenda.",
        "conditions": "IMF Policy Support Instrument. Revenue mobilization. Public investment efficiency improvements.",
        "outcomes": "Successfully completed. Coastal protection programs maintained. Fiscal position stabilized.",
        "includes_climate_clause": "Partial",
        "climate_notes": "Coastal resilience provisions. Protected spending on sea-level rise adaptation and fishing community support.",
        "source_url": "https://clubdeparis.org/en/communications/press-release/senegal-2019",
        "source_document": "Paris Club Agreed Minutes - Senegal 2019",
    },
    # ------------------------------------------------------------------
    # 11. Kenya 2021 — Bilateral (canonical frontend version)
    # ------------------------------------------------------------------
    {
        "country_code": "KEN",
        "year": 2021,
        "debt_amount_millions": 5600.0,
        "creditor_type": "Official",
        "treatment_type": "Bilateral",
        "duration_months": 36,
        "npv_reduction_percent": 18.0,
        "grace_period_months": 12,
        "interest_rate_percent": 3.0,
        "terms_summary": "Bilateral restructuring with China and official creditors including climate adaptation provisions for drought resilience and renewable energy transition.",
        "conditions": "Revenue mobilization reforms. Debt transparency commitments. Climate resilience investment plan.",
        "outcomes": "Agreement reached with major bilateral creditors. Climate provisions established precedent for region. Debt service profile improved.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Climate adaptation provisions for drought resilience and renewable energy transition.",
        "source_url": "https://www.treasury.go.ke/debt-management/",
        "source_document": "Bilateral Restructuring Agreement - Kenya 2021",
    },
    # ------------------------------------------------------------------
    # 12. Ecuador 2020 — Private Stock
    # ------------------------------------------------------------------
    {
        "country_code": "ECU",
        "year": 2020,
        "debt_amount_millions": 17400.0,
        "creditor_type": "Private",
        "treatment_type": "Stock",
        "duration_months": 60,
        "npv_reduction_percent": 32.0,
        "grace_period_months": 36,
        "interest_rate_percent": 5.0,
        "terms_summary": "Comprehensive bond restructuring with innovative Galapagos conservation clause linking debt relief to marine protection targets.",
        "conditions": "IMF Extended Fund Facility. Fiscal reforms. Conservation commitments for Galapagos marine reserve.",
        "outcomes": "Successfully completed. Freed $1.1B for Galapagos conservation. Established model for debt-for-nature swaps.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Innovative Galapagos conservation clause. Debt relief linked to marine protection targets and biodiversity commitments.",
        "source_url": "https://www.finanzas.gob.ec/",
        "source_document": "Ecuador Bond Exchange - Galapagos Conservation 2020",
    },
    # ------------------------------------------------------------------
    # 13. Suriname 2023 — Private Stock
    # ------------------------------------------------------------------
    {
        "country_code": "SUR",
        "year": 2023,
        "debt_amount_millions": 675.0,
        "creditor_type": "Private",
        "treatment_type": "Stock",
        "duration_months": 36,
        "npv_reduction_percent": 28.0,
        "grace_period_months": 18,
        "interest_rate_percent": 4.5,
        "terms_summary": "Eurobond restructuring with rainforest protection clauses for Amazon conservation and indigenous rights.",
        "conditions": "IMF Extended Fund Facility. Amazon conservation commitments. Indigenous rights protections. Fiscal reforms.",
        "outcomes": "Agreement reached with bondholders. Rainforest protection provisions included. Fiscal sustainability path established.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Rainforest protection clauses for Amazon conservation and indigenous rights.",
        "source_url": "https://www.imf.org/en/Countries/SUR",
        "source_document": "Suriname Eurobond Restructuring 2023",
    },
    # ------------------------------------------------------------------
    # 14. Madagascar 2021 — Paris Club Flow
    # ------------------------------------------------------------------
    {
        "country_code": "MDG",
        "year": 2021,
        "debt_amount_millions": 850.0,
        "creditor_type": "Paris Club",
        "treatment_type": "Flow",
        "duration_months": 24,
        "npv_reduction_percent": 22.0,
        "grace_period_months": 12,
        "interest_rate_percent": 2.0,
        "terms_summary": "Paris Club flow treatment with biodiversity protection provisions for unique endemic species.",
        "conditions": "IMF Extended Credit Facility. Biodiversity conservation commitments. Forest protection program. Fiscal reforms.",
        "outcomes": "Successfully completed. Biodiversity protection provisions implemented. Fiscal space for conservation created.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Biodiversity protection provisions for unique endemic species. Forest conservation spending protected.",
        "source_url": "https://clubdeparis.org/en/communications/press-release/madagascar-2021",
        "source_document": "Paris Club Agreed Minutes - Madagascar 2021",
    },
    # ------------------------------------------------------------------
    # 15. Mozambique 2019 — Bilateral
    # ------------------------------------------------------------------
    {
        "country_code": "MOZ",
        "year": 2019,
        "debt_amount_millions": 2300.0,
        "creditor_type": "Official",
        "treatment_type": "Bilateral",
        "duration_months": 36,
        "npv_reduction_percent": 20.0,
        "grace_period_months": 18,
        "interest_rate_percent": 2.5,
        "terms_summary": "Bilateral restructuring following cyclone disasters with climate resilience infrastructure provisions.",
        "conditions": "Post-cyclone reconstruction plan. Debt transparency reforms. Infrastructure resilience standards.",
        "outcomes": "Agreement reached with bilateral creditors. Reconstruction progressed. Climate-resilient infrastructure standards adopted.",
        "includes_climate_clause": "Partial",
        "climate_notes": "Climate resilience infrastructure provisions following Cyclone Idai and Kenneth. Disaster preparedness spending protected.",
        "source_url": "https://www.imf.org/en/Countries/MOZ",
        "source_document": "Bilateral Restructuring - Mozambique 2019",
    },
    # ------------------------------------------------------------------
    # 16. Pakistan 2019 — Bilateral (frontend version, distinct from PAK 2023)
    # ------------------------------------------------------------------
    {
        "country_code": "PAK",
        "year": 2019,
        "debt_amount_millions": 6200.0,
        "creditor_type": "Official",
        "treatment_type": "Bilateral",
        "duration_months": 36,
        "npv_reduction_percent": 15.0,
        "grace_period_months": 12,
        "interest_rate_percent": 3.5,
        "terms_summary": "Bilateral restructuring with Saudi Arabia and UAE for balance of payments support.",
        "conditions": "IMF Extended Fund Facility. Fiscal consolidation. Energy sector reforms. Tax base broadening.",
        "outcomes": "Successfully completed. Balance of payments stabilized. Bilateral relationships preserved.",
        "includes_climate_clause": "No",
        "climate_notes": None,
        "source_url": "https://www.finance.gov.pk/",
        "source_document": "Bilateral Restructuring - Pakistan 2019",
    },
    # ------------------------------------------------------------------
    # 17. Bangladesh 2020 — Bilateral (frontend version, distinct from BGD 2017)
    # ------------------------------------------------------------------
    {
        "country_code": "BGD",
        "year": 2020,
        "debt_amount_millions": 3100.0,
        "creditor_type": "Official",
        "treatment_type": "Bilateral",
        "duration_months": 24,
        "npv_reduction_percent": 12.0,
        "grace_period_months": 12,
        "interest_rate_percent": 2.0,
        "terms_summary": "Bilateral agreement with climate vulnerability provisions for coastal flooding and cyclone adaptation.",
        "conditions": "Climate adaptation investment plan. Coastal protection commitments. Budget transparency on climate spending.",
        "outcomes": "Successfully completed. Climate adaptation programs maintained during COVID-19. Coastal protection investments continued.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Climate vulnerability provisions for coastal flooding and cyclone adaptation.",
        "source_url": "https://mof.gov.bd/",
        "source_document": "Bilateral Agreement - Bangladesh 2020",
    },
    # ------------------------------------------------------------------
    # 18. Belize 2021 — Blue Bond
    # ------------------------------------------------------------------
    {
        "country_code": "BLZ",
        "year": 2021,
        "debt_amount_millions": 553.0,
        "creditor_type": "Private",
        "treatment_type": "Blue Bond",
        "duration_months": 228,  # 19-year term
        "npv_reduction_percent": 45.0,
        "grace_period_months": 60,
        "interest_rate_percent": 4.0,
        "terms_summary": "Innovative blue bond with 30% debt reduction in exchange for marine conservation commitments protecting coral reefs.",
        "conditions": "Marine conservation commitments. Belize Barrier Reef protection. 30% of ocean waters protected. Endowment fund creation.",
        "outcomes": "Landmark deal. $553M superbond retired. Marine conservation commitments legally binding. Model for blue economy finance.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Marine conservation commitments protecting coral reefs. Belize Barrier Reef World Heritage Site protections.",
        "source_url": "https://www.nature.org/en-us/about-us/where-we-work/caribbean/belize/",
        "source_document": "Belize Blue Bond - TNC 2021",
    },
    # ------------------------------------------------------------------
    # 19. Grenada 2022 — Private Stock
    # ------------------------------------------------------------------
    {
        "country_code": "GRD",
        "year": 2022,
        "debt_amount_millions": 240.0,
        "creditor_type": "Private",
        "treatment_type": "Stock",
        "duration_months": 36,
        "npv_reduction_percent": 25.0,
        "grace_period_months": 12,
        "interest_rate_percent": 5.0,
        "terms_summary": "Hurricane resilience bond with automatic payment suspension clauses for natural disasters.",
        "conditions": "Disaster preparedness plan. Building code enforcement. Climate resilience investment targets.",
        "outcomes": "Successfully restructured. Hurricane clause provides automatic fiscal breathing room. Model for SIDS climate-resilient debt.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Automatic payment suspension clauses triggered by qualifying natural disasters. Hurricane resilience provisions.",
        "source_url": "https://www.gov.gd/",
        "source_document": "Grenada Hurricane Resilience Bond 2022",
    },
    # ------------------------------------------------------------------
    # 20. São Tomé and Príncipe 2022 — HIPC
    # ------------------------------------------------------------------
    {
        "country_code": "STP",
        "year": 2022,
        "debt_amount_millions": 85.0,
        "creditor_type": "Paris Club",
        "treatment_type": "HIPC",
        "duration_months": 24,
        "npv_reduction_percent": 50.0,
        "grace_period_months": 18,
        "interest_rate_percent": 1.0,
        "terms_summary": "HIPC completion with ocean conservation provisions for small island developing state.",
        "conditions": "PRSP implementation. Ocean conservation commitments. Fisheries management reforms. Public financial management improvements.",
        "outcomes": "HIPC completion point reached. Significant debt stock reduction. Ocean conservation framework established.",
        "includes_climate_clause": "Partial",
        "climate_notes": "Ocean conservation provisions for small island developing state. Marine resource protection spending safeguarded.",
        "source_url": "https://www.imf.org/en/About/Factsheets/Sheets/2023/HIPC",
        "source_document": "HIPC Completion Point - São Tomé and Príncipe 2022",
    },

    # ==================================================================
    # BACKEND-ONLY EXTRAS (21-23)
    # These represent distinct events not in the frontend's 20 cases.
    # They carry richer detail fields from the original backend seed.
    # ==================================================================

    # ------------------------------------------------------------------
    # 21. Pakistan 2023 — Post-floods emergency (backend-only)
    # ------------------------------------------------------------------
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
        "terms_summary": "Bilateral flow treatment following devastating 2022 floods. Emergency debt relief to support reconstruction and climate resilience.",
        "conditions": "Flood reconstruction program. Climate resilience investments. Energy sector reforms. IMF program track record.",
        "outcomes": "Ongoing. Initial liquidity relief successful. Reconstruction progressing. Climate adaptation planning initiated.",
        "includes_climate_clause": "Yes",
        "climate_notes": "Explicit climate emergency recognition. Protected disaster response and climate resilience spending. Linked to climate adaptation plan.",
        "source_url": "https://www.imf.org/en/Countries/PAK",
        "source_document": "Emergency Treatment - Pakistan Floods 2023",
    },
    # ------------------------------------------------------------------
    # 22. Bangladesh 2017 — Rohingya crisis (backend-only)
    # ------------------------------------------------------------------
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
        "source_url": "https://mof.gov.bd/",
        "source_document": "Humanitarian Emergency Treatment - Bangladesh 2017",
    },
    # ------------------------------------------------------------------
    # 23. Kenya 2021 — Mixed creditor flow (backend-only, distinct from #11)
    # ------------------------------------------------------------------
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
        "source_url": "https://www.treasury.go.ke/debt-management/",
        "source_document": "Paris Club - Kenya Treatment 2021",
    },
]


def seed_all():
    """Seed countries and precedents. Idempotent — safe to run repeatedly."""
    init_database()
    db = SessionLocal()

    try:
        # ---- COUNTRIES ----
        print("=" * 60)
        print("COUNTRIES")
        print("=" * 60)

        country_map = {}  # code -> Country ORM object
        added_c = 0
        updated_c = 0

        for c in COUNTRIES:
            existing = db.execute(
                select(Country).where(Country.code == c["code"])
            ).scalar_one_or_none()

            if existing:
                # Update fields to match canonical data
                changed = False
                for field in ("name", "region", "income_level", "population",
                              "gdp_usd_billions", "climate_vulnerability_score"):
                    if getattr(existing, field) != c[field]:
                        setattr(existing, field, c[field])
                        changed = True
                if changed:
                    updated_c += 1
                    print(f"  Updated: {c['name']} ({c['code']})")
                else:
                    print(f"  OK:      {c['name']} ({c['code']})")
                country_map[c["code"]] = existing
            else:
                new = Country(**c)
                db.add(new)
                db.flush()  # get id
                country_map[c["code"]] = new
                added_c += 1
                print(f"  Added:   {c['name']} ({c['code']})")

        db.commit()
        print(f"\nCountries: {added_c} added, {updated_c} updated, "
              f"{len(COUNTRIES) - added_c - updated_c} unchanged")

        # ---- PRECEDENTS ----
        print("\n" + "=" * 60)
        print("PRECEDENTS")
        print("=" * 60)

        added_p = 0
        updated_p = 0
        skipped_p = 0

        for p in PRECEDENTS:
            code = p["country_code"]
            country = country_map.get(code)
            if not country:
                print(f"  SKIP: country {code} not found")
                skipped_p += 1
                continue

            # Look for existing record on (country_id, year, creditor_type, treatment_type)
            existing = db.execute(
                select(Precedent).where(
                    Precedent.country_id == country.id,
                    Precedent.year == p["year"],
                    Precedent.creditor_type == p["creditor_type"],
                    Precedent.treatment_type == p["treatment_type"],
                )
            ).scalar_one_or_none()

            # Also check for the old Zambia 2022 record that we're replacing with 2023
            if code == "ZMB" and p["year"] == 2023:
                old_zmb = db.execute(
                    select(Precedent).where(
                        Precedent.country_id == country.id,
                        Precedent.year == 2022,
                        Precedent.treatment_type == "Common Framework",
                    )
                ).scalar_one_or_none()
                if old_zmb:
                    db.delete(old_zmb)
                    print(f"  Removed: ZMB 2022 Common Framework (superseded by 2023)")

            fields = {
                "country_id": country.id,
                "year": p["year"],
                "debt_amount_millions": p["debt_amount_millions"],
                "creditor_type": p["creditor_type"],
                "treatment_type": p["treatment_type"],
                "duration_months": p.get("duration_months"),
                "npv_reduction_percent": p.get("npv_reduction_percent"),
                "grace_period_months": p.get("grace_period_months"),
                "interest_rate_percent": p.get("interest_rate_percent"),
                "terms_summary": p.get("terms_summary"),
                "conditions": p.get("conditions"),
                "outcomes": p.get("outcomes"),
                "includes_climate_clause": p.get("includes_climate_clause"),
                "climate_notes": p.get("climate_notes"),
                "source_url": p.get("source_url"),
                "source_document": p.get("source_document"),
            }

            if existing:
                changed = False
                for k, v in fields.items():
                    if getattr(existing, k) != v:
                        setattr(existing, k, v)
                        changed = True
                if changed:
                    updated_p += 1
                    print(f"  Updated: {code} {p['year']} {p['treatment_type']}")
                else:
                    print(f"  OK:      {code} {p['year']} {p['treatment_type']}")
            else:
                new = Precedent(**fields, created_at=datetime.utcnow())
                db.add(new)
                added_p += 1
                print(f"  Added:   {code} {p['year']} {p['treatment_type']} "
                      f"(${p['debt_amount_millions']:,.0f}M)")

        db.commit()
        print(f"\nPrecedents: {added_p} added, {updated_p} updated, "
              f"{skipped_p} skipped")

        # ---- SUMMARY ----
        total_c = db.execute(select(Country)).scalars().all()
        total_p = db.execute(select(Precedent)).scalars().all()

        print("\n" + "=" * 60)
        print("DATABASE SUMMARY")
        print("=" * 60)
        print(f"  Countries:  {len(total_c)}")
        print(f"  Precedents: {len(total_p)}")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
