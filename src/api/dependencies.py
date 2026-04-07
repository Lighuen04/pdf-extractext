"""Dependency injection container."""

from motor.motor_asyncio import AsyncIOMotorDatabase as AsyncDatabase

from src.infrastructure import (
    get_database,
    DocumentRepository,
    PDFExtractorAdapter,
    AISummarizerAdapter,
    MongoDBAdapter,
)
from src.application import (
    DocumentService,
    ExtractionService,
    SummarizationService,
    UploadDocumentUseCase,
    ExtractTextUseCase,
    SummarizeTextUseCase,
)


class DIContainer:
    """Dependency Injection Container for managing service instances."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_database(self) -> AsyncDatabase:
        """Get database instance."""
        return await get_database()

    def get_document_repository(self, database: AsyncDatabase) -> DocumentRepository:
        """Get document repository instance."""
        return DocumentRepository(database)

    def get_mongodb_adapter(self, database: AsyncDatabase) -> MongoDBAdapter:
        """Get MongoDB adapter instance."""
        return MongoDBAdapter(database)

    def get_pdf_extractor_adapter(self) -> PDFExtractorAdapter:
        """Get PDF extractor adapter instance."""
        return PDFExtractorAdapter()

    def get_ai_summarizer_adapter(self) -> AISummarizerAdapter:
        """Get AI summarizer adapter instance."""
        return AISummarizerAdapter()

    def get_document_service(self, database: AsyncDatabase) -> DocumentService:
        """Get document service instance."""
        repository = self.get_document_repository(database)
        return DocumentService(repository)

    def get_extraction_service(self) -> ExtractionService:
        """Get extraction service instance."""
        adapter = self.get_pdf_extractor_adapter()
        return ExtractionService(adapter)

    def get_summarization_service(self) -> SummarizationService:
        """Get summarization service instance."""
        adapter = self.get_ai_summarizer_adapter()
        return SummarizationService(adapter)

    def get_upload_document_use_case(self, database: AsyncDatabase) -> UploadDocumentUseCase:
        """Get upload document use case instance."""
        service = self.get_document_service(database)
        return UploadDocumentUseCase(service)

    def get_extract_text_use_case(self, database: AsyncDatabase) -> ExtractTextUseCase:
        """Get extract text use case instance."""
        doc_service = self.get_document_service(database)
        extraction_service = self.get_extraction_service()
        return ExtractTextUseCase(doc_service, extraction_service)

    def get_summarize_text_use_case(self, database: AsyncDatabase) -> SummarizeTextUseCase:
        """Get summarize text use case instance."""
        doc_service = self.get_document_service(database)
        summarization_service = self.get_summarization_service()
        return SummarizeTextUseCase(doc_service, summarization_service)


# Global DI container instance
_di_container = DIContainer()


async def get_di_container() -> DIContainer:
    """Get the DI container instance."""
    return _di_container
