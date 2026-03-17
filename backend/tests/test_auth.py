"""
Borrower's Forum Platform - Authentication Tests
=================================================

Tests for API key authentication system.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


class TestAPIKeyValidation:
    """Tests for API key format validation."""
    
    def test_missing_api_key_returns_401(self):
        """Missing API key should return 401."""
        response = client.get("/api/v1/countries")
        assert response.status_code == 401
        assert "detail" in response.json()
    
    def test_invalid_format_returns_401(self):
        """Invalid API key format should return 401."""
        response = client.get(
            "/api/v1/countries",
            headers={"X-API-Key": "not_a_valid_key"}
        )
        assert response.status_code == 401
    
    def test_key_without_bf_prefix_fails(self):
        """API key without 'bf_' prefix should fail."""
        response = client.get(
            "/api/v1/countries",
            headers={"X-API-Key": "invalid_key_format"}
        )
        assert response.status_code == 401
    
    def test_malformed_key_fails(self):
        """Malformed API key should fail."""
        response = client.get(
            "/api/v1/countries",
            headers={"X-API-Key": "bf_"}
        )
        assert response.status_code == 401


class TestAdminEndpoints:
    """Tests for admin endpoints."""
    
    def test_admin_keys_list_requires_auth(self):
        """Admin keys list should require auth."""
        response = client.get("/api/v1/admin/keys")
        assert response.status_code in [401, 403]
    
    def test_admin_create_key_requires_auth(self):
        """Creating keys should require admin auth."""
        response = client.post(
            "/api/v1/admin/keys",
            json={"name": "Test", "owner": "Test"}
        )
        assert response.status_code in [401, 403]
    
    def test_bootstrap_endpoint_exists(self):
        """Bootstrap endpoint should exist."""
        response = client.post(
            "/api/v1/admin/keys/bootstrap",
            json={"admin_secret": "wrong", "name": "Test", "owner": "Test"}
        )
        # Should fail but not 404
        assert response.status_code != 404


class TestErrorResponses:
    """Tests for error response format."""
    
    def test_401_has_detail_field(self):
        """401 errors should have detail field."""
        response = client.get("/api/v1/countries")
        data = response.json()
        assert "detail" in data
    
    def test_401_detail_has_error_info(self):
        """401 detail should include error information."""
        response = client.get("/api/v1/countries")
        data = response.json()
        detail = data.get("detail", {})
        # Should have either 'error' or 'message'
        assert "error" in detail or "message" in detail or isinstance(detail, str)