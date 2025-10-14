"""Generation and system interfaces."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum

from ..models.document import Document
from ..models.query import Query, Response


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class IGenerationStrategy(ABC):
    """Abstract base class for text generation strategies.
    
    Defines the interface for generating responses based on
    retrieved context and user queries.
    """
    
    __slots__ = ()
    
    @abstractmethod
    async def generate(
        self,
        query: "Query",
        context: List["Document"],
        max_tokens: int = 1000
    ) -> "Response":
        """Generate a response based on query and context.
        
        Args:
            query: User query
            context: Retrieved context documents
            max_tokens: Maximum tokens in response
            
        Returns:
            Response: Generated response with metadata
        """
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the generation model.
        
        Returns:
            Dict[str, Any]: Model information
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the model name."""
        pass


class ILogger(ABC):
    """Abstract base class for logging interface."""
    
    __slots__ = ()
    
    @abstractmethod
    def log(
        self,
        level: LogLevel,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log a message with specified level.
        
        Args:
            level: Log level
            message: Log message
            metadata: Optional metadata
        """
        pass
    
    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        pass
    
    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        pass
    
    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        pass
    
    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        pass


class IConfiguration(ABC):
    """Abstract base class for configuration management."""
    
    __slots__ = ()
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        pass
    
    @abstractmethod
    def load_from_env(self) -> None:
        """Load configuration from environment variables."""
        pass