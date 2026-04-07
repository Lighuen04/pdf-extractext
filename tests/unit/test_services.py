"""Unit tests for services."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from src.application.services import DocumentService
from src.application.dto import DocumentDTO


@pytest.mark.asyncio
class TestDocumentService:
    """Test cases for DocumentService."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock document repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create a DocumentService instance with mock repository."""
        return DocumentService(mock_repository)

    @pytest.mark.asyncio
    async def test_create_document(self, service, mock_repository):
        """Test creating a new document."""
        # Mock repository response
        mock_repository.create_document.return_value = "doc_123"
        mock_repository.get_document_by_id.return_value = {
            "_id": "doc_123",
            "filename": "test.pdf",
            "original_filename": "test.pdf",
            "file_size": 1024,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "error_message": None,
        }

        # Execute
        result = await service.create_document(
            filename="test.pdf",
            original_filename="test.pdf",
            file_size=1024,
            file_path="/uploads/test.pdf",
        )

        # Assert
        assert result.id == "doc_123"
        assert result.filename == "test.pdf"
        assert result.status == "pending"
        mock_repository.create_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_document(self, service, mock_repository):
        """Test retrieving a document."""
        # Mock repository response
        mock_repository.get_document_by_id.return_value = {
            "_id": "doc_123",
            "filename": "test.pdf",
            "original_filename": "test.pdf",
            "file_size": 1024,
            "status": "completed",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "error_message": None,
        }

        # Execute
        result = await service.get_document("doc_123")

        # Assert
        assert result is not None
        assert result.id == "doc_123"
        assert result.status == "completed"
        mock_repository.get_document_by_id.assert_called_once_with("doc_123")

    @pytest.mark.asyncio
    async def test_get_nonexistent_document(self, service, mock_repository):
        """Test retrieving a nonexistent document."""
        # Mock repository response
        mock_repository.get_document_by_id.return_value = None

        # Execute
        result = await service.get_document("nonexistent_id")

        # Assert
        assert result is None
        mock_repository.get_document_by_id.assert_called_once_with("nonexistent_id")

    @pytest.mark.asyncio
    async def test_update_document_status(self, service, mock_repository):
        """Test updating document status."""
        # Mock repository response
        mock_repository.update_document_status.return_value = True

        # Execute
        result = await service.update_document_status("doc_123", "processing")

        # Assert
        assert result is True
        mock_repository.update_document_status.assert_called_once_with(
            document_id="doc_123",
            status="processing",
            error_message=None,
        )
