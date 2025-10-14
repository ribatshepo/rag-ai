#!/usr/bin/env python3
"""
Simple example demonstrating the shared module usage.

This script shows how to use the foundational components
of the RAG AI system shared module.
"""

import asyncio
from datetime import datetime
from shared.utils import TextProcessor, URLValidator, RateLimiter
from shared.models.document import Document, DocumentStatus
from shared.models.chunk import TextChunk
from shared.models.query import Query, Response, Embedding
from shared.config.base_config import BaseConfig, LoggingConfig


async def main():
    """Main example function."""
    print("RAG AI Shared Module Example")
    print("=" * 40)
    
    # Configuration example
    print("\n1. Configuration Management:")
    config = BaseConfig()
    print(f"   Environment: {config.environment}")
    print(f"   Debug mode: {config.debug}")
    print(f"   API host: {config.api_host}:{config.api_port}")
    
    # Text processing example
    print("\n2. Text Processing:")
    processor = TextProcessor()
    sample_text = "  <p>This is a <b>sample</b> text with HTML tags!  </p>  "
    cleaned_text = processor.clean_text(sample_text)
    print(f"   Original: {repr(sample_text)}")
    print(f"   Cleaned:  {repr(cleaned_text)}")
    
    # URL validation example
    print("\n3. URL Validation:")
    validator = URLValidator()
    test_urls = [
        "https://example.com/page",
        "invalid-url",
        "http://test.domain.com/path?query=value"
    ]
    
    for url in test_urls:
        info = validator.validate_url(url)
        print(f"   {url:<35} -> Valid: {info.is_valid}")
        if not info.is_valid:
            print(f"   {' ' * 35} -> Error: {info.error_message}")
    
    # Rate limiting example
    print("\n4. Rate Limiting:")
    limiter = RateLimiter(max_tokens=3, refill_rate=1.0)
    
    for i in range(5):
        acquired = await limiter.acquire("test-key", timeout=0.1)
        print(f"   Request {i+1}: {'✓' if acquired else '✗'} (acquired: {acquired})")
        if not acquired:
            remaining = limiter.get_remaining_tokens("test-key")
            print(f"   {' ' * 12} Remaining tokens: {remaining:.2f}")
    
    # Data models example
    print("\n5. Data Models:")
    
    # Create a document
    doc = Document(
        id="doc-123",
        url="https://example.com/article",
        title="Sample Article",
        content="This is the content of the sample article.",
        content_type="text/html"
    )
    print(f"   Document: {doc.title} (Status: {doc.status})")
    doc.mark_completed()
    print(f"   Updated status: {doc.status}")
    
    # Create a text chunk
    chunk = TextChunk(
        id="chunk-456",
        document_id=doc.id,
        content="This is a chunk of text from the document.",
        chunk_index=0,
        start_char=0,
        end_char=42
    )
    print(f"   Chunk: {chunk.length} chars, {chunk.word_count} words")
    
    # Create a query
    query = Query(
        id="query-789",
        text="What is the main topic of the article?",
        max_results=5
    )
    print(f"   Query: {query.text}")
    
    # Create a response
    response = Response(
        id="response-101",
        query_id=query.id,
        text="The main topic of the article is about sample content.",
        confidence=0.85,
        sources=[doc.id]
    )
    print(f"   Response: {response.text[:50]}... (confidence: {response.confidence})")
    
    print("\n All examples completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())