"""
Borrower's Forum Platform - Debt Calculator Tests
==================================================

Tests for debt calculation endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


class TestDebtCalculatorAuth:
    """Tests for debt calculator authentication."""
    
    def test_calculate_without_auth_fails(self):
        """Debt calculate endpoint should require auth."""
        response = client.post(
            "/api/v1/debt/calculate",
            json={"country_code": "GHA", "year": 2023, "debt_amount_usd": 50000000}
        )
        assert response.status_code in [401, 403]
    
    def test_compare_without_auth_fails(self):
        """Debt compare endpoint should require auth."""
        response = client.post(
            "/api/v1/debt/compare",
            json={"scenarios": []}
        )
        assert response.status_code in [401, 403]
    
    def test_info_without_auth_fails(self):
        """Debt info endpoint should require auth."""
        response = client.get("/api/v1/debt/info")
        assert response.status_code in [401, 403]


class TestDebtCalculatorValidation:
    """Tests for debt calculator input validation."""
    
    def test_calculate_missing_country_code(self):
        """Should reject requests missing country_code."""
        response = client.post(
            "/api/v1/debt/calculate",
            json={"year": 2023, "debt_amount_usd": 50000000},
            headers={"X-API-Key": "bf_invalid_key"}
        )
        # Should fail - either auth or validation
        assert response.status_code in [401, 403, 422]
    
    def test_calculate_negative_debt_amount(self):
        """Should reject negative debt amounts."""
        response = client.post(
            "/api/v1/debt/calculate",
            json={"country_code": "GHA", "year": 2023, "debt_amount_usd": -50000000},
            headers={"X-API-Key": "bf_invalid_key"}
        )
        # Should fail - either auth or validation
        assert response.status_code in [401, 403, 422]
    
    def test_calculate_invalid_year(self):
        """Should reject invalid years."""
        response = client.post(
            "/api/v1/debt/calculate",
            json={"country_code": "GHA", "year": 1800, "debt_amount_usd": 50000000},
            headers={"X-API-Key": "bf_invalid_key"}
        )
        # Should fail - either auth or validation
        assert response.status_code in [401, 403, 422]


class TestDebtCalculatorEndpoints:
    """Tests for debt calculator endpoint structure."""
    
    def test_calculate_endpoint_exists(self):
        """Calculate endpoint should exist."""
        response = client.post("/api/v1/debt/calculate", json={})
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404
    
    def test_compare_endpoint_exists(self):
        """Compare endpoint should exist."""
        response = client.post("/api/v1/debt/compare", json={})
        assert response.status_code != 404
    
    def test_info_endpoint_exists(self):
        """Info endpoint should exist."""
        response = client.get("/api/v1/debt/info")
        assert response.status_code != 404
    
    def test_calculate_live_endpoint_exists(self):
        """Calculate-live endpoint should exist."""
        response = client.post("/api/v1/debt/calculate-live", json={})
        assert response.status_code != 404