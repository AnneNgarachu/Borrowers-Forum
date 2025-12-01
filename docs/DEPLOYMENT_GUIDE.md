# 🚀 Deployment Guide - Borrower's Forum Platform

**Last Updated:** December 1, 2025  
**Status:** 🟢 LIVE on Render  
**Live URL:** https://borrowers-forum.onrender.com  
**API Documentation:** https://borrowers-forum.onrender.com/api/docs

---

## 📊 Deployment Overview

The Borrower's Forum Platform is deployed on **Render** (free tier) and connected to **Supabase PostgreSQL** for the database.

### Live Endpoints

| Endpoint | URL |
|----------|-----|
| **Root** | https://borrowers-forum.onrender.com |
| **Health Check** | https://borrowers-forum.onrender.com/health |
| **Swagger UI** | https://borrowers-forum.onrender.com/api/docs |
| **ReDoc** | https://borrowers-forum.onrender.com/api/redoc |
| **OpenAPI JSON** | https://borrowers-forum.onrender.com/api/openapi.json |

**Note:** All data endpoints require API key authentication via the `X-API-Key` header.

---

## ⚙️ Render Configuration

### Service Settings

| Setting | Value |
|---------|-------|
| **Platform** | Render |
| **Service Type** | Web Service |
| **Instance Type** | Free ($0/month) |
| **Region** | Oregon (US West) |
| **Branch** | main |
| **Auto-Deploy** | Enabled |

### Build & Start Commands

| Command | Value |
|---------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT` |

### Environment Variables (Required)

| Variable | Description | Example |
|----------|-------------|---------|
| `PYTHON_VERSION` | **CRITICAL** - Forces Python 3.11 | `3.11.10` |
| `DATABASE_URL` | Supabase PostgreSQL connection string | `postgresql://postgres.xxx:password@aws-0-us-east-1.pooler.supabase.com:6543/postgres` |
| `BOOTSTRAP_SECRET` | Secret for initial admin key creation | `your-generated-secret` |

---

## 📝 Deployment Files

### Procfile
```
web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

### runtime.txt
```
python-3.11.0
```

### requirements.txt (Production)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==1.10.13
python-multipart==0.0.6
python-dotenv==1.0.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
requests>=2.31.0
pytest>=7.4.0
httpx==0.27.0
pytest-asyncio>=0.21.0
```

### settings.py Import (Line 10)
```python
from pydantic import BaseSettings  # Pydantic V1 syntax
```

---

## ⚠️ Critical Deployment Lesson

### The Problem We Encountered

**Error:**
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```

**Root Cause:**
- Render defaults to **Python 3.13** (newest version)
- **Pydantic V1.10.13** is incompatible with Python 3.13
- The error occurs at runtime, not build time

### The Solution

**Add this environment variable in Render Dashboard:**

```
PYTHON_VERSION=3.11.10
```

This single environment variable forces Render to use Python 3.11 instead of 3.13, which is compatible with Pydantic V1.

---

## 🔄 Deployment History & Troubleshooting

### Platforms Attempted

| Platform | Result | Issue |
|----------|--------|-------|
| **Railway** | ❌ Failed | Rust compilation timeout for pydantic-core |
| **Render** | ❌ Initially Failed | Python 3.13 + Pydantic V1 incompatibility |
| **Render** | ✅ Success | After adding `PYTHON_VERSION=3.11.10` |

### Common Errors & Solutions

#### Error: "Failed building wheel for pydantic-core"
**Cause:** Pydantic V2 requires Rust compilation  
**Solution:** Use Pydantic V1 (`pydantic==1.10.13`) OR upgrade to paid tier

#### Error: "ForwardRef._evaluate() missing argument"
**Cause:** Python 3.13 + Pydantic V1 incompatibility  
**Solution:** Add `PYTHON_VERSION=3.11.10` environment variable

#### Error: "SELECT 1 should be explicitly declared as text()"
**Cause:** SQLAlchemy 2.0 requires `text()` wrapper for raw SQL  
**Solution:** Change `db.execute("SELECT 1")` to `db.execute(text("SELECT 1"))`

---

## 🗄️ Database Configuration

### Supabase PostgreSQL

| Setting | Value |
|---------|-------|
| **Provider** | Supabase |
| **Database** | PostgreSQL 15 |
| **Connection Type** | Session Pooler (IPv4 compatible) |
| **Port** | 6543 |
| **Region** | US East 1 |

### Connection String Format
```
postgresql://postgres.[project-ref]:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### Database Tables

| Table | Records | Description |
|-------|---------|-------------|
| `countries` | 5 | Country profiles (Ghana, Kenya, Zambia, Pakistan, Bangladesh) |
| `debt_data` | 5 | Debt service and development cost data (2023) |
| `precedents` | 5 | Historical debt restructuring cases (2017-2023) |
| `api_keys` | 1+ | API keys with permissions and rate limits |

---

## 🔒 Security Configuration

### Implemented Security Measures

- ✅ API key authentication on all data endpoints
- ✅ Rate limiting (100 req/min standard, 1000/min admin)
- ✅ Permission levels (read, read_write, admin)
- ✅ SHA-256 key hashing (secure storage)
- ✅ Bootstrap secret in environment variable
- ✅ No credentials in Git repository
- ✅ DATABASE_URL stored as environment variable
- ✅ Repository is private on GitHub
- ✅ HTTPS enabled (automatic on Render)
- ✅ CORS configured for allowed origins

### API Key Authentication

All data endpoints require the `X-API-Key` header:

```bash
curl -H "X-API-Key: bf_your_key_id_your_secret" \
  https://borrowers-forum.onrender.com/api/v1/countries
```

### Bootstrap Secret

The bootstrap secret is used for initial admin key creation:

1. Generate a secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
2. Add to Render environment variables as `BOOTSTRAP_SECRET`
3. Use `POST /api/v1/admin/keys/bootstrap` to create the first admin key

---

## 📈 Free Tier Limitations

### Render Free Tier Notes

| Limitation | Impact |
|------------|--------|
| **Spin Down** | Instance sleeps after 15 minutes of inactivity |
| **Cold Start** | First request after sleep takes ~50 seconds |
| **RAM** | 512 MB |
| **CPU** | 0.1 CPU |

### Recommendations

- **Development/Demo:** Free tier is sufficient
- **Production:** Consider Starter tier ($7/month) for zero downtime
- **High Traffic:** Consider Standard tier ($25/month)

---

## 🔄 Redeployment Process

### Automatic Deployment

Render automatically deploys when you push to the `main` branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

### Manual Deployment

1. Go to Render Dashboard
2. Click **"Manual Deploy"** dropdown
3. Select **"Deploy latest commit"** or **"Clear build cache & deploy"**

### Clear Cache Deployment

Use "Clear build cache & deploy" when:
- Changing Python version
- Major dependency updates
- Deployment seems stuck on old code

---

## 🧪 Testing Live Deployment

### Quick Health Check

```bash
curl https://borrowers-forum.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "database": {
    "status": "healthy",
    "database_type": "postgresql"
  }
}
```

### Test Protected Endpoints

```bash
# List countries (requires API key)
curl -H "X-API-Key: your_key_here" \
  https://borrowers-forum.onrender.com/api/v1/countries

# Get calculator info (requires API key)
curl -H "X-API-Key: your_key_here" \
  https://borrowers-forum.onrender.com/api/v1/debt/info

# Get precedent statistics (requires API key)
curl -H "X-API-Key: your_key_here" \
  https://borrowers-forum.onrender.com/api/v1/precedents/stats
```

### Swagger UI Testing

Visit: https://borrowers-forum.onrender.com/api/docs

1. Click the **Authorize** button (top right)
2. Enter your API key
3. Use the interactive interface to test all endpoints

---

## 🧪 Running Tests

The project includes 38 automated tests:

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Run all tests
pytest tests/ -v
```

**Test Coverage:**
- test_health.py - 4 tests
- test_countries.py - 6 tests
- test_debt.py - 10 tests
- test_precedents.py - 9 tests
- test_auth.py - 9 tests

---

## 📞 Support & Resources

### Render Documentation
- https://render.com/docs

### Supabase Documentation
- https://supabase.com/docs

### Project Repository
- https://github.com/AnneNgarachu/Borrowers-Forum (Private)

---

## 🎯 Deployment Checklist

### Before First Deployment

- [ ] Procfile created in root directory
- [ ] runtime.txt created with Python version
- [ ] requirements.txt has production dependencies
- [ ] settings.py uses `from pydantic import BaseSettings`
- [ ] .gitignore excludes .env and sensitive files
- [ ] DATABASE_URL works locally

### Render Setup

- [ ] GitHub repository connected
- [ ] Build command set: `pip install -r requirements.txt`
- [ ] Start command set: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
- [ ] `PYTHON_VERSION=3.11.10` environment variable added
- [ ] `DATABASE_URL` environment variable added
- [ ] `BOOTSTRAP_SECRET` environment variable added
- [ ] Free tier selected (or paid for production)

### Post-Deployment Verification

- [ ] Root endpoint responds (/)
- [ ] Health check shows "healthy" (/health)
- [ ] Swagger UI loads (/api/docs)
- [ ] Bootstrap endpoint works (one-time)
- [ ] Admin key created and saved securely
- [ ] Protected endpoints work with API key

### Security Verification

- [ ] API key authentication working
- [ ] Rate limiting working
- [ ] Bootstrap secret not exposed
- [ ] Old API keys rotated if exposed

---

*This guide was created based on real deployment experience and troubleshooting. The `PYTHON_VERSION` environment variable was the critical fix that enabled successful deployment.*