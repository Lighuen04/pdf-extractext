"""Extract text from PDF use case."""

from typing import Optional
from src.application.services import DocumentService, ExtractionService
from src.application.dto import ExtractionResultDTO


class ExtractTextUseCase:
    """Use case for extracting text from a PDF document."""

    def __init__(
        self,
        document_service: DocumentService,
        extraction_service: ExtractionService,
    ):
        self.document_service = document_service
        self.extraction_service = extraction_service

    async def execute(self, document_id: str) -> Optional[ExtractionResultDTO]:
        """Execute the extract text use case."""
        # Retrieve document
        document = await self.document_service.get_document(document_id)
        if not document:
            return None

        # Update status to processing
        await self.document_service.update_document_status(document_id, "processing")

        try:
            # Extract text
            result = await self.extraction_service.extract_text_from_pdf(
                document_id, document.filename
            )

            if result:
                # Update status to completed
                await self.document_service.update_document_status(document_id, "completed")
                return result
            else:
                # Update status to failed
                await self.document_service.update_document_status(
                    document_id, "failed", "Text extraction failed"
                )
                return None
        except Exception as e:
            # Update status to failed with error message
            await self.document_service.update_document_status(
                document_id, "failed", str(e)
            )
            return None
