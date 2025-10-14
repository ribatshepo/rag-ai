"""Text chunk data model."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class TextChunk(BaseModel):
    """Processed text chunk with metadata.
    
    Represents a chunk of text that has been extracted and processed
    from a larger document, ready for embedding generation.
    """
    
    id: str = Field(..., description="Unique chunk identifier")
    document_id: str = Field(..., description="Parent document identifier")
    content: str = Field(..., description="Chunk text content")
    chunk_index: int = Field(..., description="Position within parent document")
    start_char: int = Field(..., description="Start character position in original document")
    end_char: int = Field(..., description="End character position in original document")
    token_count: Optional[int] = Field(None, description="Estimated token count")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional chunk metadata"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when chunk was created"
    )
    
    # Contextual information
    previous_chunk_id: Optional[str] = Field(
        None, 
        description="ID of previous chunk for context"
    )
    next_chunk_id: Optional[str] = Field(
        None, 
        description="ID of next chunk for context"
    )
    
    # Processing metadata
    language: Optional[str] = Field(None, description="Detected language")
    section_title: Optional[str] = Field(None, description="Section or heading title")
    
    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @property
    def length(self) -> int:
        """Get content length in characters."""
        return len(self.content)
    
    @property
    def word_count(self) -> int:
        """Get approximate word count."""
        return len(self.content.split())
    
    def get_context_window(self, window_size: int = 100) -> str:
        """Get content with context window indicators.
        
        Args:
            window_size: Number of characters for context window
            
        Returns:
            str: Content with context indicators
        """
        prefix = "..." if self.start_char > 0 else ""
        suffix = "..." if self.next_chunk_id else ""
        
        content = self.content
        if len(content) > window_size * 2:
            mid = len(content) // 2
            start = max(0, mid - window_size)
            end = min(len(content), mid + window_size)
            content = f"{content[:start]}...{content[start:end]}...{content[end:]}"
        
        return f"{prefix}{content}{suffix}"