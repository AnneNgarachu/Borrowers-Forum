# 🌍 Borrower's Forum Platform

**Debt Intelligence Platform for the UN-backed Borrower's Forum**

A production-ready API that helps debt-stressed countries make informed decisions through data-driven debt analysis and historical precedent matching.

[![Live Status](https://img.shields.io/badge/Status-🟢%20LIVE-success)](https://borrowers-forum.onrender.com)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/tests-38%20passed-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌐 Live Platform

**The platform is LIVE and operational!**

| Resource | URL |
|----------|-----|
| **🌍 Live API** | https://borrowers-forum.onrender.com |
| **📖 API Documentation** | https://borrowers-forum.onrender.com/api/docs |
| **❤️ Health Check** | https://borrowers-forum.onrender.com/health |
| **📘 ReDoc** | https://borrowers-forum.onrender.com/api/redoc |

**⚠️ Note:** All data endpoints require API key authentication. Contact the administrator to obtain an API key.

---

## ✨ Features

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
- **Live Data Mode**: Calculate with real-time World Bank data for 190+ countries

### 🔍 **Precedents Search**
Find historical debt restructuring cases with AI-powered similarity matching:
- **Advanced Filtering**: By country, year range, creditor type, treatment type, climate clauses
- **AI Similarity Scoring**: Intelligent matching based on 5 factors (regional, income level, climate vulnerability, debt amount, recency)
- **Statistics Dashboard**: Aggregated insights by creditor type, treatment type, climate clauses
- **Climate Tracking**: Identify cases with climate adaptation clauses

### 🌍 **Live World Bank Data**
Real-time economic data integration:
- **190+ Countries**: Any country with World Bank data
- **Live Indicators**: GDP, population, external debt, debt service, government revenue
- **Automatic Caching**: 1-hour TTL for performance

### 🌍 **Country Data**
- Comprehensive country profiles with economic and climate indicators
- 5 countries with detailed data: Ghana, Kenya, Zambia, Pakistan, Bangladesh
- Climate vulnerability scoring

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
- Python 3.11+ (NOT 3.13 - see note below)
- PostgreSQL database (or Supabase account)
- Git

#### Installation

```bash
# Clone the repository
git clone https://github.com/AnneNgarachu/Borrowers-Forum.git
cd Borrowers-Forum

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
echo "DATABASE_URL=postgresql://..." > .env
echo "BOOTSTRAP_SECRET=your_secret_here" >> .env

# Run the server
uvicorn src.api.main:app --reload
```

#### Access Local API

- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000

---

## 📊 API Endpoints (19 Total)

### **Public Endpoints** (2)
```
GET    /                              # API information
GET    /health                        # Health check with database status
```

### **Countries** (3) - 🔐 Protected
```
GET    /api/v1/countries              # List all countries
POST   /api/v1/countries              # Create new country
GET    /api/v1/countries/{code}       # Get specific country by ISO code
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
GET    /api/v1/precedents/similar     # AI similarity matching
GET    /api/v1/precedents/stats       # Get statistics
```

### **Live Data** (3) - 🔐 Protected
```
GET    /api/v1/live/economic/{code}   # Live economic data from World Bank
GET    /api/v1/live/debt/{code}       # Live debt data for calculator
GET    /api/v1/live/countries         # List supported countries
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
│  │  Live Data | Admin                    │  │
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
│  │  - AI Similarity Matching             │  │
│  │  - External API Clients               │  │
│  └───────────────────────────────────────┘  │
│                    ↓                         │
│  ┌───────────────────────────────────────┐  │
│  │       Database Layer                  │  │
│  │  - SQLAlchemy Models                  │  │
│  │  - Session Management                 │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
          ↓                    ↓
┌─────────────────┐  ┌─────────────────────┐
│ Supabase        │  │ World Bank API      │
│ PostgreSQL      │  │ (Live Data)         │
└─────────────────┘  └─────────────────────┘
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
| **PostgreSQL** | 15+ | Database |
| **Supabase** | Cloud | Database hosting |
| **Render** | Cloud | Application hosting |
| **Uvicorn** | 0.24.0 | ASGI server |
| **pytest** | 9.0+ | Testing framework |
| **httpx** | 0.27.0 | HTTP client for tests |

---

## 📁 Project Structure

```
Borrowers-Forum/
├── src/
│   ├── api/
│   │   ├── main.py                    # FastAPI application
│   │   ├── dependencies.py            # Dependency injection
│   │   ├── auth.py                    # Authentication & rate limiting
│   │   └── routers/
│   │       ├── countries.py           # Countries endpoints
│   │       ├── debt.py                # Debt calculator endpoints
│   │       ├── precedents.py          # Precedents search endpoints
│   │       ├── live_data.py           # Live World Bank data endpoints
│   │       └── admin.py               # Admin key management
│   ├── config/
│   │   └── settings.py                # Configuration management
│   ├── models/
│   │   └── debt_data.py               # SQLAlchemy models
│   ├── services/
│   │   ├── database.py                # Database connection
│   │   ├── debt_calculator.py         # Debt calculation logic
│   │   ├── precedent_search.py        # Precedents search logic
│   │   ├── auth_service.py            # API key management
│   │   └── external_data.py           # World Bank API client
│   └── utils/
│       ├── env_validator.py           # Environment validation
│       ├── add_test_data.py           # Test data scripts
│       └── add_api_keys_table.py      # API keys table setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Test fixtures
│   ├── test_health.py                 # Health endpoint tests
│   ├── test_countries.py              # Countries API tests
│   ├── test_debt.py                   # Debt calculator tests
│   ├── test_precedents.py             # Precedents search tests
│   └── test_auth.py                   # Authentication tests
├── docs/
│   ├── ARCHITECTURE.md                # Architecture overview
│   ├── CHAT_HANDOFF.md                # Development handoff
│   └── DEPLOYMENT_GUIDE.md            # Deployment configuration
├── Procfile                           # Render start command
├── runtime.txt                        # Python version
├── requirements.txt                   # Python dependencies
├── .env.example                       # Example environment variables
├── .gitignore
└── README.md                          # This file
```

---

## 🗄️ Database Schema

### **Countries** (5 records)
Country profiles with economic and climate indicators.

### **DebtData** (5 records)
Time-series debt service and development spending data.

### **Precedents** (5 records)
Historical debt restructuring cases with climate considerations.

### **APIKeys** (1+ records)
API key storage with permissions and rate limits.

---

## 🤖 AI Similarity Matching

The precedents search uses an intelligent scoring algorithm (0-100) based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Regional Similarity** | 30 points | Same geographic region |
| **Income Level** | 25 points | Same World Bank income classification |
| **Climate Vulnerability** | 15 points | Similar climate vulnerability scores |
| **Debt Amount** | 20 points | Comparable debt size (within 50-200%) |
| **Recency** | 10 points | More recent cases score higher |

---

## 📈 Development Roadmap

- [x] **Phase 1**: Foundation & Setup ✅
- [x] **Phase 2**: Database & Countries API ✅
- [x] **Phase 3**: Debt Calculator & Precedents Search ✅
- [x] **Phase 4**: Live World Bank Data Integration ✅
- [x] **Phase 5**: Testing (38 pytest tests) ✅
- [x] **Phase 6**: Deployment to Render ✅
- [x] **Phase 7**: Security & Authentication ✅
- [ ] **Phase 8**: Frontend Dashboard

**Current Status:** 🟢 LIVE - Production-ready API with authentication and tests

---

## 🚀 Deployment

### **Current Production Setup**

| Component | Service | Plan |
|-----------|---------|------|
| **API Hosting** | Render | Free |
| **Database** | Supabase | Free |
| **Region** | US West / US East | - |

### **Environment Variables Required**

| Variable | Description |
|----------|-------------|
| `PYTHON_VERSION` | `3.11.10` (Critical for Pydantic V1 compatibility) |
| `DATABASE_URL` | PostgreSQL connection string |
| `BOOTSTRAP_SECRET` | Secret for initial admin key creation |

### **Deploy Your Own**

See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## ⚠️ Important Notes

### **Python Version**
This project requires **Python 3.11.x**. Python 3.13 is NOT compatible due to Pydantic V1 limitations. When deploying, always set `PYTHON_VERSION=3.11.10`.

### **Free Tier Limitations**
- Render free instances spin down after 15 minutes of inactivity
- First request after sleep may take ~50 seconds
- For production use, consider upgrading to paid tier ($7/month)

---

## 🔒 Security

**Implemented:**
- ✅ API key authentication on all data endpoints
- ✅ Rate limiting (100 req/min standard, 1000/min admin)
- ✅ Permission levels (read, read_write, admin)
- ✅ SHA-256 key hashing (secure storage)
- ✅ Bootstrap secret in environment variable
- ✅ No credentials in code (environment variables only)
- ✅ Input validation on all endpoints (Pydantic models)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS configured properly
- ✅ HTTPS enabled (automatic on Render)

---

## 🤝 Contributing

This is a UN-backed initiative. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make changes and add tests
4. Run tests (`pytest tests/ -v`)
5. Commit changes (`git commit -m 'Add: AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **UN Borrower's Forum** - Project sponsor and vision
- **IMF & World Bank** - Data sources and methodologies
- **Paris Club** - Historical precedent documentation

---

## 📞 Contact

**Developer**: Anne Ngarachu  
**GitHub**: [@AnneNgarachu](https://github.com/AnneNgarachu)  
**Repository**: [Borrowers-Forum](https://github.com/AnneNgarachu/Borrowers-Forum)

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Version** | 1.0.0 |
| **Status** | 🟢 LIVE |
| **API Endpoints** | 19 |
| **Automated Tests** | 38 |
| **Database Tables** | 4 |
| **Test Records** | 16 |
| **Countries (stored)** | 5 |
| **Countries (live)** | 190+ |

**Last Updated:** December 1, 2025

---

*Built with ❤️ for debt-stressed countries seeking data-driven solutions*