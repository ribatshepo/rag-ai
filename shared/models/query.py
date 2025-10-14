"""Query, response, and embedding data models."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np


class Query(BaseModel):
    """User query structure.
    
    Represents a user's query with metadata and processing information.
    """
    
    id: str = Field(..., description="Unique query identifier")
    text: str = Field(..., description="Query text")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    intent: Optional[str] = Field(None, description="Detected query intent")
    language: Optional[str] = Field(None, description="Detected language")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional query metadata"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when query was created"
    )
    
    # Search parameters
    max_results: int = Field(10, description="Maximum results to return")
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Search filters"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Response(BaseModel):
    """Generated response with sources.
    
    Represents a generated response to a user query with
    source attribution and metadata.
    """
    
    id: str = Field(..., description="Unique response identifier")
    query_id: str = Field(..., description="Associated query identifier")
    text: str = Field(..., description="Generated response text")
    confidence: Optional[float] = Field(None, description="Response confidence score")
    sources: List[str] = Field(
        default_factory=list,
        description="Source document IDs used"
    )
    generation_time: Optional[float] = Field(
        None, 
        description="Generation time in seconds"
    )
    token_count: Optional[int] = Field(None, description="Response token count")
    model_name: Optional[str] = Field(None, description="Model used for generation")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional response metadata"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when response was created"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Embedding(BaseModel):
    """Vector embedding with metadata.
    
    Represents a vector embedding of text content with
    associated metadata for storage and retrieval.
    """
    
    id: str = Field(..., description="Unique embedding identifier")
    document_id: Optional[str] = Field(None, description="Source document identifier")
    chunk_id: Optional[str] = Field(None, description="Source chunk identifier")
    text: str = Field(..., description="Original text content")
    vector: List[float] = Field(..., description="Embedding vector")
    model_name: str = Field(..., description="Embedding model used")
    dimension: int = Field(..., description="Vector dimension")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional embedding metadata"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when embedding was created"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @property
    def vector_array(self) -> np.ndarray:
        """Get vector as numpy array."""
        return np.array(self.vector)
    
    @classmethod
    def from_array(
        cls,
        embedding_id: str,
        text: str,
        vector: np.ndarray,
        model_name: str,
        **kwargs
    ) -> "Embedding":
        """Create embedding from numpy array.
        
        Args:
            embedding_id: Unique identifier
            text: Original text
            vector: Embedding vector as numpy array
            model_name: Model used for embedding
            **kwargs: Additional fields
            
        Returns:
            Embedding: Created embedding instance
        """
        return cls(
            id=embedding_id,
            text=text,
            vector=vector.tolist(),
            model_name=model_name,
            dimension=len(vector),
            **kwargs
        )