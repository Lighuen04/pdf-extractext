"""Unit tests for repositories."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

from src.infrastructure.repositories import DocumentRepository


@pytest.mark.asyncio
class TestDocumentRepository:
    """Test cases for DocumentRepository."""

    @pytest.fixture
    def mock_database(self):
        """Create a mock MongoDB database."""
        mock_db = AsyncMock()
        mock_db.__getitem__ = MagicMock(return_value=AsyncMock())
        return mock_db

    @pytest.fixture
    def repository(self, mock_database):
        """Create a DocumentRepository instance with mock database."""
        return DocumentRepository(mock_database)

    @pytest.mark.asyncio
    async def test_create_document(self, repository):
        """Test creating a new document in the repository."""
        # Mock insert_one response
        mock_insert_result = AsyncMock()
        mock_insert_result.inserted_id = ObjectId()
        repository.collection.insert_one = AsyncMock(return_value=mock_insert_result)

        # Execute
        doc_id = await repository.create_document(
            filename="test.pdf",
            original_filename="test.pdf",
            file_size=1024,
            file_path="/uploads/test.pdf",
        )

        # Assert
        assert doc_id is not None
        repository.collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_document_by_id(self, repository):
        """Test retrieving a document by ID."""
        # Mock find_one response
        test_doc = {
            "_id": ObjectId(),
            "filename": "test.pdf",
            "original_filename": "test.pdf",
            "file_size": 1024,
            "status": "pending",
        }
        repository.collection.find_one = AsyncMock(return_value=test_doc)

        # Execute
        result = await repository.get_document_by_id(str(test_doc["_id"]))

        # Assert
        assert result == test_doc
        repository.collection.find_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_document_status(self, repository):
        """Test updating document status."""
        # Mock update_one response
        mock_update_result = AsyncMock()
        mock_update_result.modified_count = 1
        repository.collection.update_one = AsyncMock(return_value=mock_update_result)

        # Execute
        result = await repository.update_document_status("doc_123", "processing")

        # Assert
        assert result is True
        repository.collection.update_one.assert_called_once()
