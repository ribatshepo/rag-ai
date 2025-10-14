"""URL validation and sanitization utilities."""

import re
from urllib.parse import urlparse, urlunparse, quote, unquote
from typing import Optional, List, Set
from dataclasses import dataclass


@dataclass
class URLInfo:
    """URL information structure."""
    original: str
    normalized: str
    scheme: str
    domain: str
    path: str
    is_valid: bool
    error_message: Optional[str] = None


class URLValidator:
    """URL validation and sanitization utilities.
    
    Provides methods for validating, normalizing, and sanitizing
    URLs for crawling and processing operations.
    """
    
    __slots__ = ('_allowed_schemes', '_blocked_domains', '_max_url_length')
    
    # Common URL patterns
    URL_PATTERN = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    DOMAIN_PATTERN = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    
    def __init__(
        self,
        allowed_schemes: Optional[Set[str]] = None,
        blocked_domains: Optional[Set[str]] = None,
        max_url_length: int = 2048
    ):
        """Initialize URL validator.
        
        Args:
            allowed_schemes: Set of allowed URL schemes
            blocked_domains: Set of blocked domains
            max_url_length: Maximum allowed URL length
        """
        self._allowed_schemes = allowed_schemes or {'http', 'https'}
        self._blocked_domains = blocked_domains or set()
        self._max_url_length = max_url_length
    
    def validate_url(self, url: str) -> URLInfo:
        """Validate and analyze a URL.
        
        Args:
            url: URL to validate
            
        Returns:
            URLInfo: URL validation results
        """
        original_url = url
        
        try:
            # Basic length check
            if len(url) > self._max_url_length:
                return URLInfo(
                    original=original_url,
                    normalized="",
                    scheme="",
                    domain="",
                    path="",
                    is_valid=False,
                    error_message=f"URL exceeds maximum length of {self._max_url_length}"
                )
            
            # Normalize the URL
            normalized_url = self.normalize_url(url)
            parsed = urlparse(normalized_url)
            
            # Validate scheme
            if parsed.scheme not in self._allowed_schemes:
                return URLInfo(
                    original=original_url,
                    normalized=normalized_url,
                    scheme=parsed.scheme,
                    domain=parsed.netloc,
                    path=parsed.path,
                    is_valid=False,
                    error_message=f"Scheme '{parsed.scheme}' not allowed"
                )
            
            # Validate domain
            if not parsed.netloc:
                return URLInfo(
                    original=original_url,
                    normalized=normalized_url,
                    scheme=parsed.scheme,
                    domain="",
                    path=parsed.path,
                    is_valid=False,
                    error_message="Missing domain"
                )
            
            # Check if domain is blocked
            domain = parsed.netloc.lower()
            if domain in self._blocked_domains:
                return URLInfo(
                    original=original_url,
                    normalized=normalized_url,
                    scheme=parsed.scheme,
                    domain=domain,
                    path=parsed.path,
                    is_valid=False,
                    error_message=f"Domain '{domain}' is blocked"
                )
            
            # Validate domain format
            if not self.DOMAIN_PATTERN.match(domain):
                return URLInfo(
                    original=original_url,
                    normalized=normalized_url,
                    scheme=parsed.scheme,
                    domain=domain,
                    path=parsed.path,
                    is_valid=False,
                    error_message=f"Invalid domain format: '{domain}'"
                )
            
            return URLInfo(
                original=original_url,
                normalized=normalized_url,
                scheme=parsed.scheme,
                domain=domain,
                path=parsed.path,
                is_valid=True
            )
        
        except Exception as e:
            return URLInfo(
                original=original_url,
                normalized="",
                scheme="",
                domain="",
                path="",
                is_valid=False,
                error_message=f"URL parsing error: {str(e)}"
            )
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL for consistent processing.
        
        Args:
            url: URL to normalize
            
        Returns:
            str: Normalized URL
        """
        # Remove leading/trailing whitespace
        url = url.strip()
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Parse and reconstruct URL
        parsed = urlparse(url)
        
        # Normalize components
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = quote(unquote(parsed.path), safe='/')
        query = parsed.query
        fragment = parsed.fragment
        
        # Remove default ports
        if ':80' in netloc and scheme == 'http':
            netloc = netloc.replace(':80', '')
        elif ':443' in netloc and scheme == 'https':
            netloc = netloc.replace(':443', '')
        
        # Remove trailing slash from path if it's just '/'
        if path == '/':
            path = ''
        
        # Reconstruct URL
        normalized = urlunparse((scheme, netloc, path, '', query, fragment))
        
        return normalized
    
    def extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text content.
        
        Args:
            text: Text content to search
            
        Returns:
            List[str]: Extracted URLs
        """
        urls = self.URL_PATTERN.findall(text)
        return [self.normalize_url(url) for url in urls]
    
    def is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain.
        
        Args:
            url1: First URL
            url2: Second URL
            
        Returns:
            bool: True if same domain
        """
        try:
            domain1 = urlparse(url1).netloc.lower()
            domain2 = urlparse(url2).netloc.lower()
            return domain1 == domain2
        except:
            return False