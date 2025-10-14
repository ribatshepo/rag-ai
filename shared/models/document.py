"""Document and crawl result data models."""

from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(BaseModel):
    """Crawled document with metadata.
    
    Represents a document that has been crawled and is ready
    for processing or has been processed.
    """
    
    id: str = Field(..., description="Unique document identifier")
    url: HttpUrl = Field(..., description="Source URL of the document")
    title: Optional[str] = Field(None, description="Document title")
    content: str = Field(..., description="Raw document content")
    content_type: str = Field("text/plain", description="MIME type of content")
    language: Optional[str] = Field(None, description="Detected language")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    status: DocumentStatus = Field(
        DocumentStatus.PENDING, 
        description="Processing status"
    )
    crawled_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when document was crawled"
    )
    processed_at: Optional[datetime] = Field(
        None, 
        description="Timestamp when document was processed"
    )
    file_size: Optional[int] = Field(None, description="Document size in bytes")
    checksum: Optional[str] = Field(None, description="Content checksum")
    
    class Config:
        """Pydantic model configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def mark_processing(self) -> None:
        """Mark document as being processed."""
        self.status = DocumentStatus.PROCESSING
    
    def mark_completed(self) -> None:
        """Mark document as successfully processed."""
        self.status = DocumentStatus.COMPLETED
        self.processed_at = datetime.utcnow()
    
    def mark_failed(self) -> None:
        """Mark document processing as failed."""
        self.status = DocumentStatus.FAILED


class CrawlResult(BaseModel):
    """Results from a crawling operation.
    
    Contains information about the crawling process and
    any documents that were successfully crawled.
    """
    
    url: HttpUrl = Field(..., description="URL that was crawled")
    success: bool = Field(..., description="Whether crawl was successful")
    document: Optional[Document] = Field(None, description="Crawled document if successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    crawled_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when crawl was performed"
    )
    redirect_chain: List[str] = Field(
        default_factory=list,
        description="Chain of redirects followed"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }