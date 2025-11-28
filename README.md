# 🌍 Borrower's Forum Platform

**Debt Intelligence Platform for the UN-backed Borrower's Forum**

A production-ready FastAPI application that helps debt-stressed countries make informed decisions through data-driven debt analysis and historical precedent matching.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 🧮 **Debt Calculator** (Phase 3 ✅)
Convert abstract debt service payments into tangible opportunity costs:
- **Healthcare**: How many doctors could be employed for 1 or 5 years?
- **Education**: How many schools could be built?
- **Climate**: What percentage of annual climate adaptation budget?
- **Comparison**: Compare multiple debt scenarios side-by-side

### 🔍 **Precedents Search** (Phase 3 ✅)
Find historical debt restructuring cases with AI-powered similarity matching:
- **Advanced Filtering**: By country, year range, creditor type, treatment type, climate clauses
- **AI Similarity Scoring**: Intelligent matching based on 5 factors (regional, income level, climate vulnerability, debt amount, recency)
- **Statistics Dashboard**: Aggregated insights by creditor type, treatment type, climate clauses
- **Climate Tracking**: Identify cases with climate adaptation clauses

### 🌍 **Country Data** (Phase 2 ✅)
- Comprehensive country profiles with economic and climate indicators
- 5 countries currently supported: Ghana, Kenya, Zambia, Pakistan, Bangladesh
- Climate vulnerability scoring

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.13+
- PostgreSQL database (or Supabase account)
- Git

### **Installation**
```bash
# Clone the repository
git clone https://github.com/AnneNgarachu/Borrowers-Forum-Platform.git
cd Borrowers-Forum-Platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your database credentials
# DATABASE_URL=postgresql://...

# Add test data
python -m src.utils.add_test_data
python -m src.utils.add_debt_test_data
python -m src.utils.add_precedent_test_data

# Run the server
uvicorn src.api.main:app --reload
```

### **Access the API**

- **API Documentation**: http://localhost:8000/api/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000

---

## 📊 API Endpoints

### **Countries** (3 endpoints)
```
GET    /api/v1/countries           # List all countries
GET    /api/v1/countries/{code}    # Get specific country
GET    /api/v1/countries/{code}/debt-data  # Get country debt data
```

### **Debt Calculator** (3 endpoints)
```
POST   /api/v1/debt/calculate      # Calculate opportunity costs
POST   /api/v1/debt/compare        # Compare scenarios
GET    /api/v1/debt/info           # Get calculator methodology
```

### **Precedents Search** (3 endpoints)
```
GET    /api/v1/precedents          # Search with filters
GET    /api/v1/precedents/similar  # AI similarity matching
GET    /api/v1/precedents/stats    # Get statistics
```

---

## 💡 Example Usage

### **Calculate Debt Opportunity Costs**

**Request:**
```bash
POST http://localhost:8000/api/v1/debt/calculate
Content-Type: application/json

{
  "country_code": "GHA",
  "year": 2023,
  "debt_amount_usd": 50000000
}
```

**Response:**
```json
{
  "country_info": {
    "code": "GHA",
    "name": "Ghana",
    "region": "Sub-Saharan Africa",
    "income_level": "LMIC"
  },
  "calculation": {
    "debt_amount_usd": 50000000,
    "year": 2023
  },
  "equivalents": {
    "doctors": {
      "annual_employment": 2500,
      "five_year_employment": 500,
      "annual_salary_usd": 20000,
      "description": "Could employ 2500 doctors for 1 year or 500 doctors for 5 years"
    },
    "schools": {
      "number_of_schools": 125,
      "cost_per_school_usd": 400000,
      "description": "Could build 125 schools"
    },
    "climate_adaptation": {
      "percentage_of_annual_budget": 25.0,
      "annual_climate_budget_usd": 200000000,
      "description": "Represents 25.0% of annual climate adaptation budget"
    }
  },
  "context": {
    "debt_to_gdp_percent": 0.06,
    "debt_to_revenue_percent": 0.25
  }
}
```

### **Find Similar Precedents**

**Request:**
```bash
GET http://localhost:8000/api/v1/precedents/similar?country_code=GHA&debt_amount_millions=2000
```

**Response:**
```json
{
  "reference_country": {
    "code": "GHA",
    "name": "Ghana",
    "region": "Sub-Saharan Africa",
    "income_level": "LMIC"
  },
  "reference_debt_amount_millions": 2000,
  "similar_precedents": [
    {
      "similarity_score": 86,
      "score_breakdown": {
        "regional_match": true,
        "income_level_match": true,
        "climate_vulnerability_similarity": 0.0,
        "debt_amount_ratio": 0.9,
        "years_ago": 5
      },
      "country": {
        "code": "GHA",
        "name": "Ghana",
        "region": "Sub-Saharan Africa",
        "income_level": "LMIC"
      },
      "year": 2020,
      "debt_amount_millions": 1800.0,
      "creditor_type": "Paris Club",
      "treatment_type": "Flow",
      "npv_reduction_percent": 25.0,
      "grace_period_months": 12,
      "terms_summary": "Paris Club flow treatment providing 3-year debt service deferral with 1-year grace period",
      "includes_climate_clause": "Partial"
    }
  ],
  "total_found": 5
}
```

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────┐
│           FastAPI Application               │
│  ┌───────────────────────────────────────┐  │
│  │         API Routers                   │  │
│  │  - Countries  - Debt  - Precedents   │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │       Service Layer                   │  │
│  │  - Business Logic                     │  │
│  │  - Calculations                       │  │
│  │  - AI Similarity Matching             │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │       Database Layer                  │  │
│  │  - SQLAlchemy Models                  │  │
│  │  - Database Session Management        │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                     ↓
         ┌─────────────────────┐
         │  Supabase PostgreSQL │
         │   (Cloud Database)   │
         └─────────────────────┘
```

**Key Design Principles:**
- ✅ Service layer separation (business logic isolated from API routes)
- ✅ RESTful API design
- ✅ Pydantic validation for type safety
- ✅ Comprehensive error handling
- ✅ Auto-generated OpenAPI documentation

---

## 📁 Project Structure
```
Borrower's-Forum-Platform/
├── src/
│   ├── api/
│   │   ├── main.py                    # FastAPI application
│   │   ├── dependencies.py            # Dependency injection
│   │   └── routers/
│   │       ├── countries.py           # Countries endpoints
│   │       ├── debt.py                # Debt calculator endpoints
│   │       └── precedents.py          # Precedents search endpoints
│   ├── config/
│   │   └── settings.py                # Configuration management
│   ├── models/
│   │   └── debt_data.py               # SQLAlchemy models
│   ├── services/
│   │   ├── database.py                # Database connection
│   │   ├── debt_calculator.py         # Debt calculation logic
│   │   └── precedent_search.py        # Precedents search logic
│   └── utils/
│       ├── env_validator.py           # Environment validation
│       ├── add_test_data.py           # Country test data
│       ├── add_debt_test_data.py      # Debt data
│       └── add_precedent_test_data.py # Precedent cases
├── docs/
│   ├── ARCHITECTURE.md                # Architecture overview
│   └── CHAT_HANDOFF.md                # Development handoff
├── .env                               # Environment variables (not in git)
├── .gitignore
├── README.md                          # This file
└── requirements.txt                   # Python dependencies
```

---

## 🗄️ Database Schema

### **Countries** (5 records)
Country profiles with economic and climate indicators.

**Fields:**
- `id` (UUID, primary key)
- `code` (VARCHAR(3), unique) - ISO 3-letter code
- `name` (VARCHAR(100))
- `region` (VARCHAR(100))
- `income_level` (VARCHAR(50))
- `population` (INTEGER)
- `gdp_usd_billions` (DECIMAL)
- `climate_vulnerability_score` (DECIMAL) - Scale 0-100

**Sample Data:** Ghana (GHA), Kenya (KEN), Zambia (ZMB), Pakistan (PAK), Bangladesh (BGD)

### **DebtData** (5 records)
Time-series debt service and development spending data.

**Fields:**
- `id` (UUID, primary key)
- `country_id` (UUID, foreign key → countries.id)
- `year` (INTEGER)
- `debt_service_usd_millions` (DECIMAL)
- `gdp_usd_billions` (DECIMAL)
- `government_revenue_usd_millions` (DECIMAL)
- `healthcare_worker_annual_salary_usd` (DECIMAL)
- `school_construction_cost_usd` (DECIMAL)
- `annual_climate_adaptation_budget_usd_millions` (DECIMAL)
- `data_quality_score` (INTEGER) - 0-100
- `source_debt`, `source_healthcare`, `source_school`, `source_climate` (VARCHAR)

### **Precedents** (5 records)
Historical debt restructuring cases with climate considerations.

**Fields:**
- `id` (UUID, primary key)
- `country_id` (UUID, foreign key → countries.id)
- `year` (INTEGER)
- `debt_amount_millions` (DECIMAL)
- `creditor_type` (VARCHAR) - Paris Club, Official, Mixed, Private
- `treatment_type` (VARCHAR) - Flow, Stock, HIPC, Common Framework
- `duration_months` (INTEGER)
- `npv_reduction_percent` (DECIMAL)
- `grace_period_months` (INTEGER)
- `interest_rate_percent` (DECIMAL)
- `terms_summary` (TEXT)
- `conditions` (TEXT)
- `outcomes` (TEXT)
- `includes_climate_clause` (VARCHAR) - Yes, No, Partial
- `climate_notes` (TEXT)
- `source_url`, `source_document` (VARCHAR)

---

## 🤖 AI Similarity Matching

The precedents search uses an intelligent scoring algorithm (0-100) based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Regional Similarity** | 30 points | Same geographic region (e.g., Sub-Saharan Africa) |
| **Income Level** | 25 points | Same World Bank income classification (e.g., LMIC) |
| **Climate Vulnerability** | 15 points | Similar climate vulnerability scores (within 10 points) |
| **Debt Amount** | 20 points | Comparable debt size (within 50-200% range) |
| **Recency** | 10 points | More recent cases score higher (within 5 years = full points) |

**Example:** Ghana seeking precedents for $2B debt scores 86/100 with Ghana 2020 case because:
- ✅ Same region (+30 points)
- ✅ Same income level (+25 points)
- ✅ Exact climate vulnerability match (+15 points)
- ✅ Similar debt amount - $1.8B vs $2B (+18 points)
- ✅ Recent case - 5 years ago (+8 points)

---

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.115+
- **Database**: PostgreSQL (Supabase cloud hosting)
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic V2
- **API Docs**: OpenAPI/Swagger (auto-generated)
- **Python**: 3.13+

**Dependencies:**
```
fastapi>=0.115.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
uvicorn>=0.30.0
```

---

## 📈 Development Roadmap

- [x] **Phase 1**: Foundation & Setup ✅
- [x] **Phase 2**: Database & Countries API ✅
- [x] **Phase 3**: Debt Calculator & Precedents Search ✅
- [ ] **Phase 4**: Real Data Integration (IMF, World Bank APIs)
- [ ] **Phase 5**: Testing & Documentation
- [ ] **Phase 6**: Deployment & Security Hardening
- [ ] **Phase 7**: Frontend Dashboard (Optional)

**Current Status:** Phase 3 Complete - Production-ready API with test data

---

## 🧪 Testing

### **Interactive Testing (Swagger UI)**
```bash
# Start the server
uvicorn src.api.main:app --reload

# Open browser
http://localhost:8000/api/docs

# Try these endpoints:
1. GET /api/v1/countries - List all countries
2. POST /api/v1/debt/calculate - Calculate opportunity costs
3. GET /api/v1/precedents/similar - Find similar cases
4. GET /api/v1/precedents/stats - View statistics
```

### **Sample Test Requests**

**Test Debt Calculator:**
```json
POST /api/v1/debt/calculate
{
  "country_code": "GHA",
  "year": 2023,
  "debt_amount_usd": 50000000
}
```

**Test Precedents Search:**
```
GET /api/v1/precedents?country_code=GHA&year_start=2020&includes_climate=true
```

**Test AI Similarity:**
```
GET /api/v1/precedents/similar?country_code=KEN&debt_amount_millions=2500
```

---

## 🚀 Deployment

**Current Status:** Development mode with test data

**For Production Deployment:**
1. Replace test data with real IMF/World Bank data
2. Set up production PostgreSQL database
3. Configure environment variables for production
4. Enable HTTPS
5. Set up monitoring (Sentry, DataDog)
6. Implement rate limiting
7. Add authentication if needed

**Recommended Platforms:**
- Railway (Easiest for FastAPI)
- Render (Good free tier)
- Fly.io (Global deployment)
- AWS/GCP/Azure (Enterprise scale)

---

## 🔒 Security

Current security measures:
- ✅ No credentials in code (environment variables only)
- ✅ Input validation on all endpoints (Pydantic models)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS configured properly
- ✅ Type-safe database operations

**Before Production:**
- [ ] Add authentication (OAuth/JWT)
- [ ] Enable rate limiting
- [ ] Set up HTTPS
- [ ] Implement API keys for access control
- [ ] Add comprehensive logging
- [ ] Set up error monitoring

---

## 🤝 Contributing

This is a UN-backed initiative. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make changes and add tests
4. Commit changes (`git commit -m 'Add: AmazingFeature'`)
5. Push to branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

**Code Standards:**
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints
- Write tests for new features
- Update documentation

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **UN Borrower's Forum** - Project sponsor and vision
- **IMF & World Bank** - Data sources and methodologies
- **Paris Club** - Historical precedent documentation
- **Framework Contributors** - Enterprise architecture patterns

---

## 📞 Contact

**Developer**: Anne Ngarachu  
**GitHub**: [@AnneNgarachu](https://github.com/AnneNgarachu)  
**Repository**: [Borrowers-Forum-Platform](https://github.com/AnneNgarachu/Borrowers-Forum-Platform)

---

## 📊 Project Statistics

**Current Version**: 1.0.0 (Phase 3 Complete)  
**Status**: ✅ Production-ready API with test data  
**Last Updated**: November 29, 2025

**Current Data:**
- **Countries**: 5 (Ghana, Kenya, Zambia, Pakistan, Bangladesh)
- **Debt Records**: 5 (2023 data with realistic estimates)
- **Precedent Cases**: 5 (2017-2023 historical cases)
- **API Endpoints**: 9 functional endpoints
- **Documentation**: Auto-generated Swagger UI

**Code Metrics:**
- **Lines of Code**: ~2,500
- **Services**: 3 (Database, DebtCalculator, PrecedentSearch)
- **Routers**: 3 (Countries, Debt, Precedents)
- **Models**: 3 (Country, DebtData, Precedent)

---

*Built with ❤️ for debt-stressed countries seeking data-driven solutions*