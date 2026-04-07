"""Upload document use case."""

import os
from typing import Optional
from src.application.services import DocumentService
from src.application.dto import DocumentDTO


class UploadDocumentUseCase:
    """Use case for uploading a PDF document."""

    def __init__(self, document_service: DocumentService):
        self.document_service = document_service

    async def execute(
        self,
        filename: str,
        original_filename: str,
        file_size: int,
        file_path: str,
        uploaded_by: Optional[str] = None,
    ) -> DocumentDTO:
        """Execute the upload document use case."""
        # Validate file
        if not self._validate_file(file_path, file_size):
            raise ValueError("Invalid file")

        # Create document entry
        document = await self.document_service.create_document(
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
            file_path=file_path,
            uploaded_by=uploaded_by,
        )

        return document

    @staticmethod
    def _validate_file(file_path: str, file_size: int) -> bool:
        """Validate if file is valid."""
        # Check if file exists
        if not os.path.exists(file_path):
            return False

        # Check if PDF (could add more validations)
        if not file_path.lower().endswith(".pdf"):
            return False

        return True
