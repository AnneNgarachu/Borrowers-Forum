"""
Borrower's Forum Platform - Countries API Tests
================================================

Tests for country endpoints.
These endpoints require authentication.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


class TestCountriesAuthentication:
    """Tests for countries endpoint authentication."""
    
    def test_list_countries_without_auth_fails(self):
        """Countries endpoint should reject requests without API key."""
        response = client.get("/api/v1/countries")
        assert response.status_code in [401, 403]
        assert "detail" in response.json()
    
    def test_list_countries_with_invalid_key_fails(self):
        """Countries endpoint should reject invalid API keys."""
        response = client.get(
            "/api/v1/countries",
            headers={"X-API-Key": "invalid_key_12345"}
        )
        assert response.status_code in [401, 403]


class TestCountryByCode:
    """Tests for GET /api/v1/countries/{code}."""
    
    def test_country_without_auth_fails(self):
        """Single country endpoint should require auth."""
        response = client.get("/api/v1/countries/GHA")
        assert response.status_code in [401, 403]
    
    def test_country_with_invalid_key_fails(self):
        """Single country endpoint should reject invalid keys."""
        response = client.get(
            "/api/v1/countries/GHA",
            headers={"X-API-Key": "invalid_key_12345"}
        )
        assert response.status_code in [401, 403]


class TestCountryEndpointStructure:
    """Tests for API structure and error responses."""
    
    def test_error_response_has_detail(self):
        """Error responses should include detail field."""
        response = client.get("/api/v1/countries")
        data = response.json()
        assert "detail" in data
    
    def test_nonexistent_endpoint_returns_404(self):
        """Non-existent endpoints should return 404."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404