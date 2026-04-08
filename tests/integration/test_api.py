"""Integration tests for API endpoints."""


class TestHealthCheckEndpoint:
    """Integration tests for health check endpoint."""

    def test_health_check_success(self, test_client):
        """Test successful health check response."""
        response = test_client.get("/health")

        assert response.status_code == 200
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

        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "documents" in data
        assert isinstance(data["documents"], list)
