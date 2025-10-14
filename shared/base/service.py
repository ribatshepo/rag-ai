"""Base service class with lifecycle and dependency injection."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio


class BaseService(ABC):
    """Abstract base service class.
    
    Provides service lifecycle management, dependency injection,
    and common service patterns.
    """
    
    __slots__ = (
        '_name', '_dependencies', '_is_running', '_created_at',
        '_start_time', '_config', '_health_status'
    )
    
    def __init__(
        self, 
        name: str,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the service.
        
        Args:
            name: Service name
            config: Optional service configuration
        """
        self._name = name
        self._dependencies: Dict[str, Any] = {}
        self._is_running = False
        self._created_at = datetime.utcnow()
        self._start_time: Optional[datetime] = None
        self._config = config or {}
        self._health_status = "stopped"
    
    async def start(self) -> None:
        """Start the service."""
        if self._is_running:
            return
        
        try:
            self._health_status = "starting"
            await self._validate_dependencies()
            await self._on_start()
            self._is_running = True
            self._start_time = datetime.utcnow()
            self._health_status = "running"
        except Exception as e:
            self._health_status = "error"
            raise RuntimeError(f"Failed to start service {self._name}: {e}")
    
    async def stop(self) -> None:
        """Stop the service."""
        if not self._is_running:
            return
        
        try:
            self._health_status = "stopping"
            await self._on_stop()
            self._is_running = False
            self._start_time = None
            self._health_status = "stopped"
        except Exception as e:
            self._health_status = "error"
            raise RuntimeError(f"Failed to stop service {self._name}: {e}")
    
    def add_dependency(self, name: str, dependency: Any) -> None:
        """Add a service dependency.
        
        Args:
            name: Dependency name
            dependency: Dependency instance
        """
        self._dependencies[name] = dependency
    
    def get_dependency(self, name: str) -> Any:
        """Get a service dependency.
        
        Args:
            name: Dependency name
            
        Returns:
            Any: Dependency instance
            
        Raises:
            KeyError: If dependency not found
        """
        if name not in self._dependencies:
            raise KeyError(f"Dependency '{name}' not found in service '{self._name}'")
        return self._dependencies[name]
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        uptime = None
        if self._start_time:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()
        
        return {
            "name": self._name,
            "status": self._health_status,
            "is_running": self._is_running,
            "uptime_seconds": uptime,
            "dependencies": list(self._dependencies.keys()),
            **await self._custom_health_check()
        }
    
    @abstractmethod
    async def _on_start(self) -> None:
        """Service start hook. Override in subclasses."""
        pass
    
    @abstractmethod
    async def _on_stop(self) -> None:
        """Service stop hook. Override in subclasses."""
        pass
    
    async def _validate_dependencies(self) -> None:
        """Validate service dependencies. Override in subclasses."""
        pass
    
    async def _custom_health_check(self) -> Dict[str, Any]:
        """Custom health check. Override in subclasses."""
        return {}
    
    @property
    def name(self) -> str:
        """Get service name."""
        return self._name
    
    @property
    def is_running(self) -> bool:
        """Check if service is running."""
        return self._is_running