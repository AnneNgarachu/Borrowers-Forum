"""
Borrower's Forum Platform - Precedents Search Tests
====================================================

Tests for precedents search endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


class TestPrecedentsAuth:
    """Tests for precedents endpoint authentication."""
    
    def test_search_without_auth_fails(self):
        """Precedents search should require auth."""
        response = client.get("/api/v1/precedents")
        assert response.status_code in [401, 403]
    
    def test_similar_without_auth_fails(self):
        """Similar precedents should require auth."""
        response = client.get("/api/v1/precedents/similar")
        assert response.status_code in [401, 403]
    
    def test_stats_without_auth_fails(self):
        """Precedents stats should require auth."""
        response = client.get("/api/v1/precedents/stats")
        assert response.status_code in [401, 403]


class TestPrecedentsEndpoints:
    """Tests for precedents endpoint structure."""
    
    def test_precedents_endpoint_exists(self):
        """Precedents endpoint should exist."""
        response = client.get("/api/v1/precedents")
        assert response.status_code != 404
    
    def test_similar_endpoint_exists(self):
        """Similar endpoint should exist."""
        response = client.get("/api/v1/precedents/similar")
        assert response.status_code != 404
    
    def test_stats_endpoint_exists(self):
        """Stats endpoint should exist."""
        response = client.get("/api/v1/precedents/stats")
        assert response.status_code != 404


class TestPrecedentsQueryParams:
    """Tests for precedents query parameters."""
    
    def test_search_with_country_filter(self):
        """Should accept country_code filter."""
        response = client.get(
            "/api/v1/precedents?country_code=GHA",
            headers={"X-API-Key": "bf_invalid_key"}
        )
        # Should fail auth, not validation
        assert response.status_code in [401, 403]
    
    def test_search_with_year_range(self):
        """Should accept year range filters."""
        response = client.get(
            "/api/v1/precedents?year_start=2015&year_end=2023",
            headers={"X-API-Key": "bf_invalid_key"}
        )
        assert response.status_code in [401, 403]
    
    def test_similar_with_params(self):
        """Similar endpoint should accept query params."""
        response = client.get(
            "/api/v1/precedents/similar?country_code=GHA&debt_amount_millions=2000",
            headers={"X-API-Key": "bf_invalid_key"}
        )
        assert response.status_code in [401, 403]