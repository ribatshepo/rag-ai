"""Content processing strategy interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class IContentProcessor(ABC):
    """Abstract base class for content processing strategies.
    
    Defines the interface for processing raw content into
    structured formats suitable for embedding and retrieval.
    """
    
    __slots__ = ()
    
    @abstractmethod
    async def process(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List["TextChunk"]:
        """Process raw content into structured chunks.
        
        Args:
            content: Raw content to process
            metadata: Optional metadata about the content
            
        Returns:
            List[TextChunk]: Processed content chunks
        """
        pass
    
    @abstractmethod
    async def clean_text(self, text: str) -> str:
        """Clean and normalize text content.
        
        Args:
            text: Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        pass
    
    @abstractmethod
    async def extract_metadata(
        self, 
        content: str
    ) -> Dict[str, Any]:
        """Extract metadata from content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dict[str, Any]: Extracted metadata
        """
        pass
    
    @abstractmethod
    async def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum chunk size in characters
            overlap: Overlap between chunks
            
        Returns:
            List[str]: Text chunks
        """
        pass
    
    @property
    @abstractmethod
    def supported_formats(self) -> List[str]:
        """Get list of supported content formats."""
        pass