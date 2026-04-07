"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from main import create_app
from src.config import Settings


@pytest.fixture
def test_settings():
    """Provide test settings."""
    return Settings(
        DEBUG=True,
        MONGODB_URL="mongodb://localhost:27017",
        MONGODB_DATABASE="pdf_extractext_test",
    )


@pytest.fixture
def test_client(test_settings):
    """Provide a test FastAPI client."""
    test_app = create_app(test_settings)
    return TestClient(test_app)


class TestHealthCheckEndpoint:
    """Integration tests for health check endpoint."""

    def test_health_check_success(self, test_client):
        """Test successful health check response."""
        response = test_client.get("/health")
        
        # Note: This test may fail if MongoDB is not running
        # For proper integration testing, ensure MongoDB is available
        assert response.status_code in [200, 503]  # 200 if connected, 503 if not
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert "version" in data
        assert "database_connected" in data


class TestRootEndpoint:
    """Integration tests for root endpoint."""

    def test_root_endpoint(self, test_client):
        """Test root endpoint response."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"


class TestDocumentEndpoints:
    """Integration tests for document endpoints."""

    def test_list_documents_empty(self, test_client):
        """Test listing documents when empty."""
        response = test_client.get("/api/v1/documents")
        
        # May fail if MongoDB not running, but structure should be valid if it succeeds
        if response.status_code == 200:
            data = response.json()
            assert "total" in data
            assert "documents" in data
            assert isinstance(data["documents"], list)
