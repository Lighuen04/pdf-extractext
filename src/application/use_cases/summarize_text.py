"""Summarize text use case."""

from typing import Optional
from src.application.services import DocumentService, SummarizationService
from src.application.dto import SummarizationResultDTO


class SummarizeTextUseCase:
    """Use case for summarizing extracted text."""

    def __init__(
        self,
        document_service: DocumentService,
        summarization_service: SummarizationService,
    ):
        self.document_service = document_service
        self.summarization_service = summarization_service

    async def execute(
        self, document_id: str, text: str, max_length: Optional[int] = None
    ) -> Optional[SummarizationResultDTO]:
        """Execute the summarize text use case."""
        # Retrieve document
        document = await self.document_service.get_document(document_id)
        if not document:
            return None

        # Update status to processing
        await self.document_service.update_document_status(document_id, "processing")

        try:
            # Summarize text
            result = await self.summarization_service.summarize_text(
                document_id, text, max_length
            )

            if result:
                # Update status to completed
                await self.document_service.update_document_status(document_id, "completed")
                return result
            else:
                # Update status to failed
                await self.document_service.update_document_status(
                    document_id, "failed", "Text summarization failed"
                )
                return None
        except Exception as e:
            # Update status to failed with error message
            await self.document_service.update_document_status(
                document_id, "failed", str(e)
            )
            return None
