"""AI summarization service for business logic."""

import time
from typing import Optional
from src.infrastructure.adapters import AISummarizerAdapter
from src.application.dto import SummarizationResultDTO


class SummarizationService:
    """Service for text summarization operations."""

    def __init__(self, ai_summarizer: AISummarizerAdapter):
        self.ai_summarizer = ai_summarizer

    async def summarize_text(
        self, document_id: str, text: str, max_length: Optional[int] = None
    ) -> Optional[SummarizationResultDTO]:
        """Summarize extracted text using AI.

        Args:
            document_id: ID of the document
            text: Text to summarize
            max_length: Maximum length of the summary

        Returns:
            SummarizationResultDTO or None if summarization fails
        """
        start_time = time.time()

        try:
            # Summarize using adapter
            summary = await self.ai_summarizer.summarize(text, max_length)

            if not summary:
                return None

            # Extract keywords
            keywords = await self.ai_summarizer.extract_keywords(text, num_keywords=10)

            summarization_time_ms = (time.time() - start_time) * 1000

            return SummarizationResultDTO(
                document_id=document_id,
                original_text=text,
                summary=summary,
                keywords=keywords,
                summarization_time_ms=summarization_time_ms,
            )
        except Exception as e:
            print(f"Error summarizing text: {str(e)}")
            return None
