"""
Shared module for RAG AI system.

This module provides the foundational components including interfaces,
base classes, data models, utilities, and configuration management.
"""

__version__ = "0.1.0"

# Export main interfaces
from .interfaces import (
    ICrawlingStrategy,
    IContentProcessor,
    IVectorStore,
    IEmbeddingGenerator,
    IRetrievalStrategy,
    IGenerationStrategy,
    ILogger,
    IConfiguration,
)

# Export base classes
from .base import BaseStrategy, BaseService, BaseRepository, BaseException

# Export data models
from .models import Document, TextChunk, Embedding, Query, Response, CrawlResult

# Export utilities
from .utils import TextProcessor, URLValidator, RateLimiter, RetryHandler

# Export configuration
from .config import BaseConfig, LoggingConfig

__all__ = [
    # Interfaces
    "ICrawlingStrategy",
    "IContentProcessor",
    "IVectorStore",
    "IEmbeddingGenerator",
    "IRetrievalStrategy",
    "IGenerationStrategy",
    "ILogger",
    "IConfiguration",
    # Base classes
    "BaseStrategy",
    "BaseService",
    "BaseRepository",
    "BaseException",
    # Models
    "Document",
    "TextChunk",
    "Embedding",
    "Query",
    "Response",
    "CrawlResult",
    # Utils
    "TextProcessor",
    "URLValidator",
    "RateLimiter",
    "RetryHandler",
    # Config
    "BaseConfig",
    "LoggingConfig",
]