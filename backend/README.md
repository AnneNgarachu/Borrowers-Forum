# 🌍 Borrower's Forum Platform

**Open-source debt intelligence platform helping debt-stressed countries make informed restructuring decisions.**

Creditors coordinate. Debtors don't. Since 1956, creditor nations have organized through the Paris Club, while debtor nations negotiate individually. This platform gives debtor nations shared intelligence to help close that gap, through data-driven debt analysis and historical precedent matching.

[![Live Status](https://img.shields.io/badge/Status-🟢%20LIVE-success)](https://borrowers-forum.onrender.com)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/tests-38%20passed-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌐 Live Platform

**The platform is LIVE and operational.**

| Resource | URL |
|----------|-----|
| **🌍 Live API** | https://borrowers-forum.onrender.com |
| **📖 API Documentation** | https://borrowers-forum.onrender.com/api/docs |
| **❤️ Health Check** | https://borrowers-forum.onrender.com/health |
| **📘 ReDoc** | https://borrowers-forum.onrender.com/api/redoc |

**⚠️ Note:** Data endpoints are protected by API key authentication. The public web frontend at [borrowersforum.org](https://www.borrowersforum.org) accesses these endpoints through a server-side key, so visitors can use the site anonymously without registering. Direct API access requires a key; contact the maintainer to request one.

---

## ✨ Features

### 🤖 **AI Strategy Tools** (Claude integration)
Generative AI features powered by the Anthropic Claude API:
- **Strategy Brief Generator**: Produces a tailored debt-strategy brief from country, precedent, and debt-data context
- **Advisory Chat**: Conversational endpoint for debt-restructuring questions, grounded in platform data
- **Model**: `claude-haiku-4-5`

### 🔐 **API Key Authentication**
Secure access control for all data endpoints:
- **Permission Levels**: read, read_write, admin
- **Rate Limiting**: 100 requests/minute (standard), 1000/minute (admin)
- **Secure Storage**: SHA-256 hashed keys

### 🧮 **Debt Calculator**
Convert abstract debt service payments into tangible opportunity costs:
- **Healthcare**: How many doctors could be employed for 1 or 5 years?
- **Education**: How many schools could be built?
- **Climate**: What percentage of annual climate adaptation budget?
- **Live Data Mode**: Calculate using real-time World Bank data for 190+ countries, with a graceful fallback to stored estimates if live data is unavailable

### 🔍 **Precedents Search**
Find historical debt restructuring cases with weighted similarity matching:
- **Advanced Filtering**: By country, year range, creditor type, treatment type, climate clauses
- **Similarity Scoring**: Deterministic 0-100 scoring across 5 weighted factors (regional, income level, climate vulnerability, debt amount, recency)
- **Statistics Dashboard**: Aggregated insights by creditor type, treatment type, climate clauses
- **Climate Tracking**: Identify cases with climate adaptation clauses

### 🌍 **Live World Bank Data**
Real-time economic data integration:
- **190+ Countries**: Any country with World Bank data
- **Live Indicators**: GDP, population, external debt, debt service, government revenue
- **Automatic Caching**: 1-hour TTL for performance

### 🗂️ **Country & Precedent Data**
- Comprehensive country profiles with economic and climate indicators
- **20 countries** seeded with detailed profiles and climate vulnerability scoring
- **23 historical precedent cases** (2017-2023) drawn from official IMF, Paris Club, and World Bank documentation

---

## 🚀 Quick Start

### **Option 1: Use the Live API (Recommended)**

The API is already deployed and ready to use:

```bash
# Test the API (public endpoint)
curl https://borrowers-forum.onrender.com

# Check health status (public endpoint)
curl https://borrowers-forum.onrender.com/health

# Access protected endpoints (requires API key)
curl -H "X-API-Key: your_api_key_here" \
  https://borrowers-forum.onrender.com/api/v1/countries
```

**Interactive Documentation:** https://borrowers-forum.onrender.com/api/docs

### **Option 2: Run Locally**

#### Prerequisites
- Python 3.11.x (NOT 3.13 - see note below)
- PostgreSQL database (or Supabase account)
- Git

#### Installation

```bash
# Clone the repository
git clone https://github.com/AnneNgarachu/Borrowers-Forum.git
cd Borrowers-Forum/backend

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
# Create .env file with your credentials
echo "DATABASE_URL=postgresql://..." > .env
echo "BOOTSTRAP_SECRET=your_secret_here" >> .env
echo "ANTHROPIC_API_KEY=your_anthropic_key_here" >> .env

# Run the server
uvicorn src.api.main:app --reload
```

#### Access Local API

- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000

---

## 📊 API Endpoints (26 Total)

### **Public Endpoints** (2)
```
GET    /                              # API information
GET    /health                        # Health check with database status
```

### **Countries** (6) - 🔐 Protected
```
GET    /api/v1/countries              # List all countries
POST   /api/v1/countries              # Create new country
GET    /api/v1/countries/{code}       # Get specific country by ISO code
PUT    /api/v1/countries/{code}       # Update a country
DELETE /api/v1/countries/{code}       # Delete a country
```

### **Debt Calculator** (4) - 🔐 Protected
```
POST   /api/v1/debt/calculate         # Calculate opportunity costs
POST   /api/v1/debt/calculate-live    # Calculate with live World Bank data
POST   /api/v1/debt/compare           # Compare multiple scenarios
GET    /api/v1/debt/info              # Get calculator methodology
```

### **Precedents Search** (3) - 🔐 Protected
```
GET    /api/v1/precedents             # Search with filters
GET    /api/v1/precedents/similar     # Weighted similarity matching
GET    /api/v1/precedents/stats       # Get statistics
```

### **Live Data** (3) - 🔐 Protected
```
GET    /api/v1/live/economic/{code}   # Live economic data from World Bank
GET    /api/v1/live/debt/{code}       # Live debt data for calculator
GET    /api/v1/live/countries         # List supported countries
```

### **AI Strategy Tools** (2) - 🔐 Protected
```
POST   /api/v1/ai/strategy-brief      # Generate a debt-strategy brief (Claude)
POST   /api/v1/ai/chat                # Advisory chat (Claude)
```

### **Admin** (6) - 🔐 Admin Only
```
POST   /api/v1/admin/keys/bootstrap   # Create first admin key (one-time)
POST   /api/v1/admin/keys             # Generate new API key
GET    /api/v1/admin/keys             # List all API keys
GET    /api/v1/admin/keys/{key_id}    # Get key details
DELETE /api/v1/admin/keys/{key_id}    # Deactivate key
POST   /api/v1/admin/keys/{key_id}/reactivate  # Reactivate key
```

---

## 💡 Example Usage

### **Calculate Debt Opportunity Costs**

**Request:**
```bash
curl -X POST "https://borrowers-forum.onrender.com/api/v1/debt/calculate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "country_code": "GHA",
    "year": 2023,
    "debt_amount_usd": 50000000
  }'
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
  }
}
```

### **Find Similar Precedents**

**Request:**
```bash
curl -H "X-API-Key: your_api_key_here" \
  "https://borrowers-forum.onrender.com/api/v1/precedents/similar?country_code=GHA&debt_amount_millions=2000"
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
        "name": "Ghana"
      },
      "year": 2020,
      "debt_amount_millions": 1800.0,
      "creditor_type": "Paris Club",
      "treatment_type": "Flow",
      "includes_climate_clause": "Partial"
    }
  ],
  "total_found": 5
}
```

---

## 🧪 Automated Testing

Run the full test suite:

```bash
# Activate virtual environment first
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Run all tests
pytest tests/ -v
```

**Test Coverage:**

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `test_health.py` | 4 | Health & root endpoints |
| `test_countries.py` | 6 | Countries API & auth |
| `test_debt.py` | 10 | Debt calculator & validation |
| `test_precedents.py` | 9 | Precedents search & filters |
| `test_auth.py` | 9 | API key authentication |
| **Total** | **38** | ✅ All passing |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           FastAPI Application               │
│  ┌───────────────────────────────────────┐  │
│  │         API Routers                   │  │
│  │  Countries | Debt | Precedents        │  │
│  │  Live Data | AI | Admin               │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │      Authentication Layer             │  │
│  │  - API Key Validation                 │  │
│  │  - Rate Limiting                      │  │
│  │  - Permission Checks                  │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │       Service Layer                   │  │
│  │  - Business Logic                     │  │
│  │  - Calculations                       │  │
│  │  - Weighted Similarity Scoring        │  │
│  │  - Claude AI Service                  │  │
│  │  - External API Clients               │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │       Database Layer                  │  │
│  │  - SQLAlchemy Models                  │  │
│  │  - Session Management                 │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
        ↓              ↓               ↓
┌─────────────┐ ┌──────────────┐ ┌──────────────┐
│ Supabase    │ │ World Bank   │ │ Anthropic    │
│ PostgreSQL  │ │ API (Live)   │ │ Claude API   │
└─────────────┘ └──────────────┘ └──────────────┘
```

**Key Design Principles:**
- ✅ Service layer separation (business logic isolated from API routes)
- ✅ RESTful API design
- ✅ Pydantic validation for type safety
- ✅ Comprehensive error handling
- ✅ Auto-generated OpenAPI documentation
- ✅ API key authentication with rate limiting

---

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11.10 | Runtime |
| **FastAPI** | 0.104.1 | Web framework |
| **Pydantic** | 1.10.13 | Data validation |
| **SQLAlchemy** | 2.0.23 | ORM |
| **anthropic** | >=0.39.0 | Claude API client |
| **PostgreSQL** | 15+ | Database |
| **Supabase** | Cloud | Database hosting |
| **Render** | Cloud | Application hosting |
| **Uvicorn** | 0.24.0 | ASGI server |
| **pytest** | >=7.4.0 | Testing framework |
| **httpx** | 0.27.0 | HTTP client for tests |

---

## 📁 Project Structure

```
Borrowers-Forum/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── main.py                # FastAPI application
│   │   │   ├── dependencies.py        # Dependency injection
│   │   │   ├── auth.py                # Authentication & rate limiting
│   │   │   └── routers/
│   │   │       ├── countries.py       # Countries endpoints
│   │   │       ├── debt.py            # Debt calculator endpoints
│   │   │       ├── precedents.py      # Precedents search endpoints
│   │   │       ├── live_data.py       # Live World Bank data endpoints
│   │   │       ├── ai.py              # Claude AI endpoints
│   │   │       └── admin.py           # Admin key management
│   │   ├── config/
│   │   │   └── settings.py            # Configuration management
│   │   ├── models/
│   │   │   └── debt_data.py           # SQLAlchemy models
│   │   ├── services/
│   │   │   ├── database.py            # Database connection
│   │   │   ├── debt_calculator.py     # Debt calculation logic
│   │   │   ├── precedent_search.py    # Precedents search logic
│   │   │   ├── auth_service.py        # API key management
│   │   │   ├── ai_service.py          # Claude AI service
│   │   │   └── external_data.py       # World Bank API client
│   │   └── utils/
│   │       ├── env_validator.py       # Environment validation
│   │       └── add_api_keys_table.py  # API keys table setup
│   ├── tests/
│   │   ├── conftest.py                # Test fixtures
│   │   ├── test_health.py             # Health endpoint tests
│   │   ├── test_countries.py          # Countries API tests
│   │   ├── test_debt.py               # Debt calculator tests
│   │   ├── test_precedents.py         # Precedents search tests
│   │   └── test_auth.py               # Authentication tests
│   ├── seed_production.sql            # Production data seed
│   ├── Procfile                       # Render start command
│   ├── runtime.txt                    # Python version
│   ├── requirements.txt               # Python dependencies
│   └── README.md                      # This file
├── frontend/                          # Next.js web application
└── README.md
```

---

## 🗄️ Database Schema

### **Countries** (20 seeded)
Country profiles with economic and climate indicators.

### **DebtData**
Time-series debt service and development spending data.

### **Precedents** (23 seeded)
Historical debt restructuring cases (2017-2023) with climate considerations.

### **APIKeys**
API key storage with permissions and rate limits.

---

## 🎯 Weighted Similarity Scoring

The precedents search uses a deterministic, rule-based scoring algorithm (0-100). This is a transparent weighted formula, not a machine-learning model:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Regional Similarity** | 30 points | Same geographic region |
| **Income Level** | 25 points | Same World Bank income classification |
| **Climate Vulnerability** | 15 points | Similar climate vulnerability scores |
| **Debt Amount** | 20 points | Comparable debt size (within 50-200%) |
| **Recency** | 10 points | More recent cases score higher |

> Generative AI (the Claude integration) powers the separate Strategy Brief and Advisory Chat features. Precedent similarity is intentionally rule-based for transparency and reproducibility.

---

## 📈 Development Roadmap

- [x] **Phase 1**: Foundation & Setup ✅
- [x] **Phase 2**: Database & Countries API ✅
- [x] **Phase 3**: Debt Calculator & Precedents Search ✅
- [x] **Phase 4**: Live World Bank Data Integration ✅
- [x] **Phase 5**: Testing (38 pytest tests) ✅
- [x] **Phase 6**: Deployment to Render ✅
- [x] **Phase 7**: Security & Authentication ✅
- [x] **Phase 8**: AI Strategy Tools (Claude) ✅
- [x] **Phase 9**: Web Frontend (Next.js) ✅

**Current Status:** 🟢 LIVE - production API with authentication, AI features, and a live web frontend

---

## 🚀 Deployment

### **Current Production Setup**

| Component | Service | Plan |
|-----------|---------|------|
| **API Hosting** | Render | Starter ($7/mo) |
| **Database** | Supabase | Cloud |
| **Frontend** | Vercel | - |

### **Environment Variables Required**

| Variable | Description |
|----------|-------------|
| `PYTHON_VERSION` | `3.11.10` (set on Render; takes precedence over runtime.txt) |
| `DATABASE_URL` | PostgreSQL connection string |
| `BOOTSTRAP_SECRET` | Secret for initial admin key creation |
| `ANTHROPIC_API_KEY` | Required for the AI endpoints (return 503 if unset) |

### **Deploy Your Own**

See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## ⚠️ Important Notes

### **Python Version**
This project requires **Python 3.11.x**. Python 3.13 is NOT compatible due to Pydantic V1 limitations. On Render, the `PYTHON_VERSION=3.11.10` environment variable takes precedence over `runtime.txt`. Keep both aligned to avoid confusion.

---

## 🔒 Security

**Implemented:**
- ✅ API key authentication enforced on all data endpoints
- ✅ Rate limiting (100 req/min standard, 1000/min admin)
- ✅ Permission levels (read, read_write, admin)
- ✅ SHA-256 key hashing (secure storage)
- ✅ Bootstrap secret in environment variable
- ✅ No credentials in code (environment variables only)
- ✅ Input validation on all endpoints (Pydantic models)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS configured properly
- ✅ HTTPS enabled (automatic on Render)

> **Note on access model:** Permissions are role-based (read / read_write / admin). The platform does not currently implement identity verification or a "verified government official" tier; the public frontend uses a single server-side key so visitors can browse anonymously. Per-user vetting is a possible future addition, not a current feature.

---

## 🤝 Contributing

This is an independent open-source project. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make changes and add tests
4. Run tests (`pytest tests/ -v`)
5. Commit changes (`git commit -m 'Add: AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. Copyright (c) 2025-2026 Anne Wanjiru Ngarachu / SAGE Platform LLC. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IMF, World Bank & Paris Club** - Data sources and methodologies for the seeded precedent and economic data
- The platform concept is aligned with the agenda of the UN Expert Group on Debt and was developed through the COP30 Simulation Programme at the British University in Egypt

---

## 📞 Contact

**Developer**: Anne Wanjiru Ngarachu
**Portfolio**: [annengarachu.com](https://annengarachu.com)
**LinkedIn**: [anne-wanjiru-ngarachu](https://www.linkedin.com/in/anne-wanjiru-ngarachu/)
**GitHub**: [@AnneNgarachu](https://github.com/AnneNgarachu)
**Repository**: [Borrowers-Forum](https://github.com/AnneNgarachu/Borrowers-Forum)

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Version** | 1.0.0 |
| **Status** | 🟢 LIVE |
| **API Endpoints** | 26 |
| **Automated Tests** | 38 |
| **Database Tables** | 4 |
| **Countries (seeded)** | 20 |
| **Precedents (seeded)** | 23 |
| **Countries (live via World Bank)** | 190+ |

---

*Built for debt-stressed countries seeking data-driven solutions*
