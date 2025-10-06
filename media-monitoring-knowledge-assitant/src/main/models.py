from pydantic import BaseModel, Field
from typing import List, Optional

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(description="Service status", example="healthy")
    message: str = Field(description="Service message", example="Media monitoring API is running")
    version: str = Field(description="API version", example="1.0.0")

class UploadResponse(BaseModel):
    """Document upload response model"""
    filename: str = Field(description="Name of the uploaded file", example="document.pdf")
    content: dict = Field(description="Processed document content")
    message: str = Field(description="Upload success message", example="Document uploaded and processed successfully")
    file_size: int = Field(description="File size in bytes", example=1024)

class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(description="Search query text", example="media monitoring strategies", min_length=1, max_length=1000)
    top_k: Optional[int] = Field(description="Number of top results to return", default=5, ge=1, le=50)

class SearchResult(BaseModel):
    """Individual search result model"""
    content: str = Field(description="Content of the search result")
    score: float = Field(description="Similarity score", ge=0.0, le=1.0)
    metadata: Optional[dict] = Field(description="Additional metadata about the result", default=None)

class SearchResponse(BaseModel):
    """Search response model"""
    query: str = Field(description="Original search query")
    results: List[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Total number of results found")
    processing_time: float = Field(description="Time taken to process the search in seconds")

class DocumentInfo(BaseModel):
    """Document information model"""
    filename: str = Field(description="Document filename")
    file_size: int = Field(description="File size in bytes")
    upload_date: str = Field(description="Date when document was uploaded")
    processing_status: str = Field(description="Document processing status")
    indexed: bool = Field(description="Whether document is indexed in vector store")

class DocumentsListResponse(BaseModel):
    """Documents list response model"""
    documents: List[DocumentInfo] = Field(description="List of document information")
    total_count: int = Field(description="Total number of documents")
    message: str = Field(description="Response message")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(description="Error type", example="ValidationError")
    message: str = Field(description="Detailed error message")
    details: Optional[dict] = Field(description="Additional error details", default=None)

class BatchUploadRequest(BaseModel):
    """Batch upload request model"""
    files: List[str] = Field(description="List of file paths to upload", min_items=1, max_items=10)

class BatchUploadResponse(BaseModel):
    """Batch upload response model"""
    total_files: int = Field(description="Total number of files processed")
    successful_uploads: int = Field(description="Number of successful uploads")
    failed_uploads: int = Field(description="Number of failed uploads")
    results: List[dict] = Field(description="Results for each file upload")

class IndexingStatusResponse(BaseModel):
    """Indexing status response model"""
    total_documents: int = Field(description="Total number of documents")
    indexed_documents: int = Field(description="Number of indexed documents")
    pending_documents: int = Field(description="Number of documents pending indexing")
    indexing_in_progress: bool = Field(description="Whether indexing is currently in progress")
    last_indexed: Optional[str] = Field(description="Timestamp of last indexing operation", default=None)
