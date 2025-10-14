"""Text processing utilities."""

import re
import unicodedata
from typing import List, Dict, Any, Optional
from html import unescape
from urllib.parse import unquote


class TextProcessor:
    """Text cleaning and normalization utilities.
    
    Provides methods for cleaning, normalizing, and processing
    text content for embedding and retrieval operations.
    """
    
    __slots__ = ('_normalize_whitespace', '_remove_html', '_decode_entities')
    
    # Common patterns for text cleaning
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
    WHITESPACE_PATTERN = re.compile(r'\s+')
    URL_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
    
    def __init__(
        self,
        normalize_whitespace: bool = True,
        remove_html: bool = True,
        decode_entities: bool = True
    ):
        """Initialize text processor.
        
        Args:
            normalize_whitespace: Whether to normalize whitespace
            remove_html: Whether to remove HTML tags
            decode_entities: Whether to decode HTML entities
        """
        self._normalize_whitespace = normalize_whitespace
        self._remove_html = remove_html
        self._decode_entities = decode_entities
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content.
        
        Args:
            text: Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Decode URL encoding
        text = unquote(text)
        
        # Decode HTML entities
        if self._decode_entities:
            text = unescape(text)
        
        # Remove HTML tags
        if self._remove_html:
            text = self.HTML_TAG_PATTERN.sub(' ', text)
        
        # Normalize Unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Normalize whitespace
        if self._normalize_whitespace:
            text = self.WHITESPACE_PATTERN.sub(' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text.
        
        Args:
            text: Input text
            
        Returns:
            List[str]: List of sentences
        """
        # Simple sentence splitting on periods, exclamation, question marks
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """Extract metadata from text content.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dict[str, Any]: Extracted metadata
        """
        metadata = {}
        
        # Basic statistics
        metadata['character_count'] = len(text)
        metadata['word_count'] = len(text.split())
        metadata['sentence_count'] = len(self.extract_sentences(text))
        
        # Extract URLs
        urls = self.URL_PATTERN.findall(text)
        metadata['urls'] = urls
        metadata['url_count'] = len(urls)
        
        # Extract emails
        emails = self.EMAIL_PATTERN.findall(text)
        metadata['emails'] = emails
        metadata['email_count'] = len(emails)
        
        # Extract phone numbers
        phones = self.PHONE_PATTERN.findall(text)
        metadata['phone_numbers'] = [f"{p[0]}{p[1]}-{p[2]}-{p[3]}" for p in phones]
        metadata['phone_count'] = len(phones)
        
        # Language detection could be added here with langdetect library
        # metadata['language'] = detect_language(text)
        
        return metadata
    
    def truncate_text(
        self,
        text: str,
        max_length: int,
        preserve_words: bool = True
    ) -> str:
        """Truncate text to maximum length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length in characters
            preserve_words: Whether to preserve word boundaries
            
        Returns:
            str: Truncated text
        """
        if len(text) <= max_length:
            return text
        
        if preserve_words:
            # Find last space before max_length
            truncated = text[:max_length]
            last_space = truncated.rfind(' ')
            if last_space > max_length * 0.8:  # Don't cut too much
                return truncated[:last_space] + "..."
        
        return text[:max_length-3] + "..."