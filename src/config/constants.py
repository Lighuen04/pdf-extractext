"""Application constants."""

# HTTP Status Messages
HTTP_OK = "OK"
HTTP_CREATED = "Created"
HTTP_BAD_REQUEST = "Bad Request"
HTTP_NOT_FOUND = "Not Found"
HTTP_INTERNAL_ERROR = "Internal Server Error"

# Document Status
DOCUMENT_STATUS_PENDING = "pending"
DOCUMENT_STATUS_PROCESSING = "processing"
DOCUMENT_STATUS_COMPLETED = "completed"
DOCUMENT_STATUS_FAILED = "failed"

# Error Messages
ERROR_FILE_NOT_FOUND = "File not found"
ERROR_INVALID_FILE_TYPE = "Invalid file type. Only PDF files are supported"
ERROR_FILE_TOO_LARGE = "File size exceeds the maximum allowed size"
ERROR_DOCUMENT_NOT_FOUND = "Document not found"
ERROR_PROCESSING_FAILED = "Failed to process the document"

# Success Messages
SUCCESS_DOCUMENT_UPLOADED = "Document uploaded successfully"
SUCCESS_EXTRACTION_COMPLETED = "Text extraction completed successfully"
SUCCESS_SUMMARIZATION_COMPLETED = "Text summarization completed successfully"

# Database Collections
COLLECTION_DOCUMENTS = "documents"
COLLECTION_EXTRACTIONS = "extractions"
COLLECTION_SUMMARIES = "summaries"

# Timeouts
DATABASE_OPERATION_TIMEOUT = 30  # seconds
PDF_EXTRACTION_TIMEOUT = 60  # seconds
AI_SUMMARIZATION_TIMEOUT = 120  # seconds
