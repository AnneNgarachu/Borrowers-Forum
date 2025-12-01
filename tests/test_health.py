"""
Borrower's Forum Platform - Health Endpoint Tests
==================================================

Tests for root and health check endpoints.
These are public endpoints (no auth required).
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint (/)."""
    
    def test_root_returns_200(self):
        """Root endpoint should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_api_info(self):
        """Root endpoint should return API information."""
        response = client.get("/")
        data = response.json()
        
        assert "name" in data or "message" in data
        assert "version" in data or "status" in data


class TestHealthEndpoint:
    """Tests for the health check endpoint (/health)."""
    
    def test_health_returns_200(self):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_status(self):
        """Health endpoint should return health status."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert data["status"] in ["healthy", "ok", "up"]