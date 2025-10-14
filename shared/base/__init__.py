"""Base classes for the RAG AI system."""

from .strategy import BaseStrategy
from .service import BaseService
from .repository import BaseRepository

# Custom exception classes
class BaseException(Exception):
    """Base exception class for RAG AI system."""
    
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

__all__ = [
    "BaseStrategy",
    "BaseService", 
    "BaseRepository",
    "BaseException",
]