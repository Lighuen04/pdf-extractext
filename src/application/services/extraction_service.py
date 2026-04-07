"""PDF extraction service for business logic."""

import time
from typing import Optional
from src.infrastructure.adapters import PDFExtractorAdapter
from src.application.dto import ExtractionResultDTO


class ExtractionService:
    """Service for PDF text extraction operations."""

    def __init__(self, pdf_extractor: PDFExtractorAdapter):
        self.pdf_extractor = pdf_extractor

    async def extract_text_from_pdf(
        self, document_id: str, file_path: str
    ) -> Optional[ExtractionResultDTO]:
        """Extract text from a PDF file.
        
        Args:
            document_id: ID of the document
            file_path: Path to the PDF file
            
        Returns:
            ExtractionResultDTO or None if extraction fails
        """
        start_time = time.time()
        
        try:
            # Extract text using adapter
            extracted_text = await self.pdf_extractor.extract_text(file_path)
            
            if not extracted_text:
                return None

            extraction_time_ms = (time.time() - start_time) * 1000
            
            return ExtractionResultDTO(
                document_id=document_id,
                extracted_text=extracted_text,
                page_count=1,  # TODO: Extract actual page count
                extraction_time_ms=extraction_time_ms,
            )
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None

    async def get_pdf_metadata(self, file_path: str) -> dict:
        """Get metadata from a PDF file."""
        try:
            metadata = await self.pdf_extractor.extract_metadata(file_path)
            return metadata
        except Exception as e:
            print(f"Error extracting PDF metadata: {str(e)}")
            return {}
