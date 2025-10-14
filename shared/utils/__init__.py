"""Utility classes for the RAG AI system."""

from .text_processor import TextProcessor
from .url_validator import URLValidator
from .rate_limiter import RateLimiter
import asyncio
import random
from typing import Callable, Any, Optional, List, Type
from datetime import datetime, timedelta


class RetryHandler:
    """Exponential backoff retry logic utility."""
    
    __slots__ = ('_max_retries', '_base_delay', '_max_delay', '_backoff_factor', '_jitter')
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True
    ):
        """Initialize retry handler.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            backoff_factor: Exponential backoff factor
            jitter: Whether to add random jitter
        """
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._backoff_factor = backoff_factor
        self._jitter = jitter
    
    async def retry_async(
        self,
        func: Callable[..., Any],
        *args,
        exceptions: Optional[List[Type[Exception]]] = None,
        **kwargs
    ) -> Any:
        """Retry an async function with exponential backoff.
        
        Args:
            func: Async function to retry
            *args: Function arguments
            exceptions: Exception types to retry on
            **kwargs: Function keyword arguments
            
        Returns:
            Any: Function result
            
        Raises:
            Exception: Last exception if all retries failed
        """
        exceptions = exceptions or [Exception]
        last_exception = None
        
        for attempt in range(self._max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                # Check if exception type should trigger retry
                if not any(isinstance(e, exc_type) for exc_type in exceptions):
                    raise
                
                # Don't wait after last attempt
                if attempt == self._max_retries:
                    break
                
                # Calculate delay
                delay = min(
                    self._base_delay * (self._backoff_factor ** attempt),
                    self._max_delay
                )
                
                # Add jitter
                if self._jitter:
                    delay *= (0.5 + random.random() * 0.5)
                
                await asyncio.sleep(delay)
        
        # Raise the last exception
        if last_exception:
            raise last_exception


class ConfigValidator:
    """Configuration validation utility."""
    
    @staticmethod
    def validate_required_keys(config: dict, required_keys: List[str]) -> None:
        """Validate that all required keys are present.
        
        Args:
            config: Configuration dictionary
            required_keys: List of required keys
            
        Raises:
            ValueError: If required keys are missing
        """
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")
    
    @staticmethod
    def validate_types(config: dict, type_mapping: dict) -> None:
        """Validate configuration value types.
        
        Args:
            config: Configuration dictionary
            type_mapping: Dictionary mapping keys to expected types
            
        Raises:
            TypeError: If value types don't match
        """
        for key, expected_type in type_mapping.items():
            if key in config and not isinstance(config[key], expected_type):
                raise TypeError(
                    f"Configuration key '{key}' must be of type {expected_type.__name__}, "
                    f"got {type(config[key]).__name__}"
                )


__all__ = [
    "TextProcessor",
    "URLValidator", 
    "RateLimiter",
    "RetryHandler",
    "ConfigValidator",
]