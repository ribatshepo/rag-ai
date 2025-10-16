"""Abstract crawling strategy interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, AsyncIterator
from datetime import datetime

from shared.models.document import CrawlResult


class ICrawlingStrategy(ABC):
    """Abstract base class for crawling strategies.
    
    Defines the interface for different crawling approaches
    such as web scraping, API crawling, file system crawling, etc.
    """
    
    __slots__ = ()
    
    @abstractmethod
    async def crawl(
        self,
        urls: List[str],
        max_depth: int = 1,
        filters: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator["CrawlResult"]:
        """Crawl the specified URLs and yield results.
        
        Args:
            urls: List of URLs to crawl
            max_depth: Maximum crawling depth
            filters: Optional crawling filters
            
        Yields:
            CrawlResult: Results from crawling operation
        """
        pass
    
    @abstractmethod
    async def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid for crawling.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is valid for crawling
        """
        pass
    
    @abstractmethod
    async def get_robots_txt(self, base_url: str) -> Optional[str]:
        """Retrieve robots.txt content for the domain.
        
        Args:
            base_url: Base URL of the domain
            
        Returns:
            Optional[str]: robots.txt content or None
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the strategy name."""
        pass
    
    @property
    @abstractmethod
    def supported_schemes(self) -> List[str]:
        """Get list of supported URL schemes."""
        pass