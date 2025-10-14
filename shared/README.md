# RAG AI System - Shared Module

A foundational shared module for a Python-based Retrieval-Augmented Generation (RAG) AI system. This module provides the core interfaces, base classes, data models, utilities, and configuration management that serve as the foundation for all other RAG system components.

## Features

### 🏗️ Core Interfaces
- **ICrawlingStrategy** - Abstract crawling behavior
- **IContentProcessor** - Content processing strategy interface
- **IVectorStore** - Vector database operations
- **IEmbeddingGenerator** - Text embedding generation
- **IRetrievalStrategy** - Document retrieval interface
- **IGenerationStrategy** - Text generation interface
- **ILogger** - Logging interface
- **IConfiguration** - Configuration management

### 🔧 Base Classes
- **BaseStrategy** - Abstract strategy with common functionality
- **BaseService** - Service lifecycle and dependency injection
- **BaseRepository** - Data access patterns
- **BaseException** - Custom exception hierarchy

### 📊 Data Models (Pydantic)
- **Document** - Crawled document with metadata
- **TextChunk** - Processed text chunk
- **Embedding** - Vector with metadata
- **Query** - User query structure
- **Response** - Generated response with sources
- **CrawlResult** - Crawling operation results

### 🛠️ Utilities
- **TextProcessor** - Text cleaning and normalization
- **URLValidator** - URL validation and sanitization
- **RateLimiter** - Request rate limiting using asyncio
- **RetryHandler** - Exponential backoff retry logic
- **ConfigValidator** - Configuration validation

### ⚙️ Configuration Management
- **BaseConfig** - Base configuration using Pydantic Settings
- **LoggingConfig** - Structured logging configuration
- Environment variable loading
- Configuration validation

## Installation

```bash
# Install basic dependencies
pip install -r requirements.txt

# Install with development tools
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[full]"
```

## Quick Start

```python
import asyncio
from shared.utils import TextProcessor, URLValidator, RateLimiter
from shared.models.document import Document
from shared.config.base_config import BaseConfig

async def example():
    # Configuration
    config = BaseConfig()
    
    # Text processing
    processor = TextProcessor()
    clean_text = processor.clean_text("<p>Sample HTML content</p>")
    
    # URL validation
    validator = URLValidator()
    url_info = validator.validate_url("https://example.com")
    
    # Rate limiting
    limiter = RateLimiter(max_tokens=10, refill_rate=1.0)
    success = await limiter.acquire("api-key")
    
    # Data models
    doc = Document(
        id="doc-1",
        url="https://example.com/article",
        title="Sample Article",
        content=clean_text
    )
    
    print(f"Document: {doc.title} (Valid URL: {url_info.is_valid})")

# Run the example
asyncio.run(example())
```

## Architecture

### Directory Structure
```
shared/
├── __init__.py
├── interfaces/
│   ├── __init__.py
│   ├── crawling.py
│   ├── processing.py
│   ├── storage.py
│   └── generation.py
├── base/
│   ├── __init__.py
│   ├── strategy.py
│   ├── service.py
│   └── repository.py
├── models/
│   ├── __init__.py
│   ├── document.py
│   ├── chunk.py
│   └── query.py
├── utils/
│   ├── __init__.py
│   ├── text_processor.py
│   ├── url_validator.py
│   └── rate_limiter.py
└── config/
    ├── __init__.py
    └── base_config.py
```

### Design Principles

- **SOLID Principles** - All classes follow SOLID design principles
- **Async-First** - Built with asyncio for asynchronous operations
- **Type Safety** - Comprehensive type hints throughout
- **Memory Efficiency** - Uses `__slots__` where appropriate
- **Configuration-Driven** - Environment-based configuration management
- **Extensible** - Abstract interfaces for easy extension

## Configuration

### Environment Variables

```bash
# Application settings
ENVIRONMENT=development
DEBUG=true
APP_NAME="RAG AI System"

# API settings
API_HOST=127.0.0.1
API_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@localhost/ragdb

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_TO_CONSOLE=true
```

### Configuration Classes

```python
from shared.config import BaseConfig, LoggingConfig

# Application configuration
config = BaseConfig()
print(f"Running in {config.environment} mode")

# Logging configuration
log_config = LoggingConfig()
logging_dict = log_config.get_logging_dict_config()
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=shared
```

### Code Quality

```bash
# Format code
black shared/

# Lint code
flake8 shared/

# Type checking
mypy shared/
```

## Contributing

1. Follow PEP 8 style guidelines
2. Include comprehensive docstrings
3. Add type hints to all functions
4. Keep files under 100 lines when possible
5. Write tests for new functionality

## License

MIT License - see LICENSE file for details.

## Dependencies

- **pydantic** - Data validation and settings management
- **numpy** - Numerical operations for embeddings
- **aiohttp** - Async HTTP client (optional)

See `requirements.txt` for complete dependency list.

## Next Steps

This shared module serves as the foundation for:

1. **Crawling Module** - Web scraping and content extraction
2. **Processing Module** - Text processing and chunking
3. **Embedding Module** - Vector generation and storage
4. **Retrieval Module** - Semantic search and ranking
5. **Generation Module** - Response generation and synthesis
6. **API Module** - REST API and user interface

Each module will implement the interfaces defined in this shared foundation.