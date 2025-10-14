"""Base repository class for data access patterns."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository class.
    
    Provides common data access patterns and repository interface
    following the Repository pattern for data abstraction.
    """
    
    __slots__ = ('_connection', '_table_name', '_created_at')
    
    def __init__(
        self, 
        connection: Any,
        table_name: str
    ):
        """Initialize the repository.
        
        Args:
            connection: Database or storage connection
            table_name: Name of the table/collection
        """
        self._connection = connection
        self._table_name = table_name
        self._created_at = datetime.utcnow()
    
    @abstractmethod
    async def create(self, entity: T) -> str:
        """Create a new entity.
        
        Args:
            entity: Entity to create
            
        Returns:
            str: Created entity ID
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID.
        
        Args:
            entity_id: Entity identifier
            
        Returns:
            Optional[T]: Entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> bool:
        """Update entity by ID.
        
        Args:
            entity_id: Entity identifier
            updates: Fields to update
            
        Returns:
            bool: True if update successful
        """
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete entity by ID.
        
        Args:
            entity_id: Entity identifier
            
        Returns:
            bool: True if deletion successful
        """
        pass
    
    @abstractmethod
    async def find(
        self, 
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """Find entities matching filters.
        
        Args:
            filters: Search filters
            limit: Maximum results to return
            offset: Number of results to skip
            
        Returns:
            List[T]: Matching entities
        """
        pass
    
    @abstractmethod
    async def count(
        self, 
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count entities matching filters.
        
        Args:
            filters: Search filters
            
        Returns:
            int: Number of matching entities
        """
        pass
    
    async def exists(self, entity_id: str) -> bool:
        """Check if entity exists.
        
        Args:
            entity_id: Entity identifier
            
        Returns:
            bool: True if entity exists
        """
        entity = await self.get_by_id(entity_id)
        return entity is not None
    
    @property
    def table_name(self) -> str:
        """Get table/collection name."""
        return self._table_name
    
    @property
    def connection(self) -> Any:
        """Get database connection."""
        return self._connection