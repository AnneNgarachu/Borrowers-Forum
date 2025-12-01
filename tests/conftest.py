"""
Borrower's Forum Platform - Test Configuration
==============================================

Shared fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.api.main import app
from src.models.debt_data import Country, DebtData, Precedent, APIKey


# ==========================================
# TEST CLIENT FIXTURE
# ==========================================

@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    
    This client can make requests to the API without running the server.
    """
    return TestClient(app)


# ==========================================
# MOCK DATA FIXTURES
# ==========================================

@pytest.fixture
def mock_country():
    """Sample country data for testing."""
    country = MagicMock(spec=Country)
    country.id = "test-uuid-123"
    country.code = "TST"
    country.name = "Testland"
    country.region = "Test Region"
    country.income_level = "LMIC"
    country.population = 50000000
    country.gdp_usd_billions = 100.0
    country.climate_vulnerability_score = 65.0
    return country


@pytest.fixture
def mock_debt_data():
    """Sample debt data for testing."""
    debt = MagicMock(spec=DebtData)
    debt.id = "test-debt-uuid-123"
    debt.country_id = "test-uuid-123"
    debt.year = 2023
    debt.debt_service_usd_millions = 500.0
    debt.gdp_usd_billions = 100.0
    debt.government_revenue_usd_millions = 20000.0
    debt.healthcare_worker_annual_salary_usd = 15000.0
    debt.school_construction_cost_usd = 350000.0
    debt.annual_climate_adaptation_budget_usd_millions = 1500.0
    return debt


@pytest.fixture
def mock_precedent():
    """Sample precedent data for testing."""
    precedent = MagicMock(spec=Precedent)
    precedent.id = "test-precedent-uuid-123"
    precedent.country_id = "test-uuid-123"
    precedent.year = 2020
    precedent.debt_amount_millions = 2000.0
    precedent.creditor_type = "Paris Club"
    precedent.treatment_type = "Flow"
    precedent.duration_months = 36
    precedent.npv_reduction_percent = 25.0
    precedent.grace_period_months = 12
    precedent.interest_rate_percent = 2.5
    precedent.terms_summary = "Test terms summary"
    precedent.includes_climate_clause = "Yes"
    return precedent


@pytest.fixture
def mock_api_key():
    """Sample API key for testing."""
    api_key = MagicMock(spec=APIKey)
    api_key.id = "test-key-uuid-123"
    api_key.key_id = "testkey123"
    api_key.key_hash = "hashed_secret"
    api_key.name = "Test API Key"
    api_key.owner = "Test Owner"
    api_key.permissions = "admin"
    api_key.is_active = True
    api_key.rate_limit_per_minute = 100
    api_key.usage_count = 0
    return api_key


# ==========================================
# AUTH BYPASS FIXTURE
# ==========================================

@pytest.fixture
def auth_headers():
    """
    Headers with a test API key.
    
    Note: For testing, we'll mock the auth dependency.
    """
    return {"X-API-Key": "bf_testkey123_testsecret123456789"}


@pytest.fixture
def mock_auth(mock_api_key):
    """
    Mock the authentication dependency.
    
    This allows tests to bypass real authentication.
    """
    with patch("src.api.auth.get_api_key") as mock:
        mock.return_value = mock_api_key
        yield mock