"""Document management router."""

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase as AsyncDatabase

from src.api.schemas import (
    DocumentCreateRequest,
    DocumentResponse,
    DocumentListResponse,
)
from src.api.dependencies import DIContainer
from src.infrastructure import get_database


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    request: DocumentCreateRequest,
    database: AsyncDatabase = Depends(get_database),
) -> DocumentResponse:
    """Upload a new PDF document.
    
    Args:
        request: Document creation request
        database: MongoDB database instance
        
    Returns:
        Created document information
    """
    di_container = DIContainer()
    use_case = di_container.get_upload_document_use_case(database)
    
    try:
        document = await use_case.execute(
            filename=request.filename,
            original_filename=request.original_filename,
            file_size=request.file_size,
            file_path=request.file_path,
        )
        return DocumentResponse(
            id=document.id,
            filename=document.filename,
            original_filename=document.original_filename,
            file_size=document.file_size,
            status=document.status,
            created_at=document.created_at,
            updated_at=document.updated_at,
            error_message=document.error_message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    database: AsyncDatabase = Depends(get_database),
) -> DocumentResponse:
    """Retrieve a document by ID.
    
    Args:
        document_id: ID of the document
        database: MongoDB database instance
        
    Returns:
        Document information
    """
    di_container = DIContainer()
    document_service = di_container.get_document_service(database)
    
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        original_filename=document.original_filename,
        file_size=document.file_size,
        status=document.status,
        created_at=document.created_at,
        updated_at=document.updated_at,
        error_message=document.error_message,
    )


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    database: AsyncDatabase = Depends(get_database),
) -> DocumentListResponse:
    """List all documents with pagination.
    
    Args:
        skip: Number of documents to skip
        limit: Maximum number of documents to return
        database: MongoDB database instance
        
    Returns:
        List of documents
    """
    di_container = DIContainer()
    document_service = di_container.get_document_service(database)
    
    documents = await document_service.list_documents(skip=skip, limit=limit)
    
    return DocumentListResponse(
        total=len(documents),
        skip=skip,
        limit=limit,
        documents=[
            DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                original_filename=doc.original_filename,
                file_size=doc.file_size,
                status=doc.status,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
                error_message=doc.error_message,
            )
            for doc in documents
        ],
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    database: AsyncDatabase = Depends(get_database),
):
    """Delete a document.
    
    Args:
        document_id: ID of the document to delete
        database: MongoDB database instance
    """
    di_container = DIContainer()
    document_service = di_container.get_document_service(database)
    
    result = await document_service.delete_document(document_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
