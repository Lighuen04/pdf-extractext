"""Document service for business logic."""

from datetime import datetime
from typing import Optional
from src.infrastructure.repositories import DocumentRepository
from src.application.dto import DocumentDTO


class DocumentService:
    """Service for document operations."""

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def create_document(
        self,
        filename: str,
        original_filename: str,
        file_size: int,
        file_path: str,
        uploaded_by: Optional[str] = None,
    ) -> DocumentDTO:
        """Create a new document entry."""
        doc_id = await self.document_repository.create_document(
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
            file_path=file_path,
            uploaded_by=uploaded_by,
        )
        
        # Retrieve the created document
        doc = await self.document_repository.get_document_by_id(doc_id)
        return self._to_dto(doc)

    async def get_document(self, document_id: str) -> Optional[DocumentDTO]:
        """Retrieve a document by ID."""
        doc = await self.document_repository.get_document_by_id(document_id)
        return self._to_dto(doc) if doc else None

    async def list_documents(self, skip: int = 0, limit: int = 10) -> list[DocumentDTO]:
        """List all documents with pagination."""
        docs = await self.document_repository.read_all(skip=skip, limit=limit)
        return [self._to_dto(doc) for doc in docs]

    async def update_document_status(
        self,
        document_id: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> bool:
        """Update document status."""
        return await self.document_repository.update_document_status(
            document_id=document_id,
            status=status,
            error_message=error_message,
        )

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document."""
        return await self.document_repository.delete(document_id)

    @staticmethod
    def _to_dto(doc: dict) -> DocumentDTO:
        """Convert database document to DTO."""
        return DocumentDTO(
            id=str(doc.get("_id", "")),
            filename=doc.get("filename", ""),
            original_filename=doc.get("original_filename", ""),
            file_size=doc.get("file_size", 0),
            status=doc.get("status", ""),
            created_at=doc.get("created_at", datetime.utcnow()),
            updated_at=doc.get("updated_at", datetime.utcnow()),
            error_message=doc.get("error_message"),
        )
