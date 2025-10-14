"""Base strategy class with common functionality."""

from abc import ABC
from typing import Any, Dict, Optional
from datetime import datetime


class BaseStrategy(ABC):
    """Abstract base strategy class with common functionality.
    
    Provides common patterns for strategy implementations including
    configuration management, lifecycle hooks, and error handling.
    """
    
    __slots__ = ('_name', '_config', '_created_at', '_is_initialized')
    
    def __init__(
        self, 
        name: str,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the strategy.
        
        Args:
            name: Strategy name
            config: Optional configuration dictionary
        """
        self._name = name
        self._config = config or {}
        self._created_at = datetime.utcnow()
        self._is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize the strategy asynchronously.
        
        Override this method to perform async initialization.
        """
        if self._is_initialized:
            return
        
        await self._on_initialize()
        self._is_initialized = True
    
    async def cleanup(self) -> None:
        """Cleanup strategy resources.
        
        Override this method to perform cleanup operations.
        """
        if not self._is_initialized:
            return
        
        await self._on_cleanup()
        self._is_initialized = False
    
    async def _on_initialize(self) -> None:
        """Hook for strategy initialization. Override in subclasses."""
        pass
    
    async def _on_cleanup(self) -> None:
        """Hook for strategy cleanup. Override in subclasses."""
        pass
    
    @property
    def name(self) -> str:
        """Get the strategy name."""
        return self._name
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the strategy configuration."""
        return self._config.copy()
    
    @property
    def is_initialized(self) -> bool:
        """Check if strategy is initialized."""
        return self._is_initialized
    
    @property
    def created_at(self) -> datetime:
        """Get strategy creation timestamp."""
        return self._created_at
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        return self._config.get(key, default)
    
    def set_config_value(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def __repr__(self) -> str:
        """String representation of the strategy."""
        return f"{self.__class__.__name__}(name='{self._name}')"