"""Data models for the RAG AI system."""

from .document import Document, CrawlResult
from .chunk import TextChunk
from .query import Query, Response, Embedding

__all__ = [
    "Document",
    "CrawlResult", 
    "TextChunk",
    "Query",
    "Response",
    "Embedding",
]