"""Rate limiting utilities using asyncio."""

import asyncio
from typing import Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class RateLimitBucket:
    """Token bucket for rate limiting."""
    max_tokens: int
    refill_rate: float  # tokens per second
    current_tokens: float
    last_refill: datetime = field(default_factory=datetime.utcnow)
    
    def refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = datetime.utcnow()
        elapsed = (now - self.last_refill).total_seconds()
        
        # Add tokens based on elapsed time
        tokens_to_add = elapsed * self.refill_rate
        self.current_tokens = min(self.max_tokens, self.current_tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from bucket.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            bool: True if tokens were consumed
        """
        self.refill()
        
        if self.current_tokens >= tokens:
            self.current_tokens -= tokens
            return True
        return False
    
    def time_until_tokens(self, tokens: int = 1) -> float:
        """Calculate time until tokens are available.
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            float: Time in seconds until tokens available
        """
        self.refill()
        
        if self.current_tokens >= tokens:
            return 0.0
        
        tokens_needed = tokens - self.current_tokens
        return tokens_needed / self.refill_rate


class RateLimiter:
    """Request rate limiting using token bucket algorithm.
    
    Provides per-key rate limiting with configurable limits
    and asynchronous waiting for token availability.
    """
    
    __slots__ = ('_buckets', '_default_max_tokens', '_default_refill_rate', '_cleanup_interval')
    
    def __init__(
        self,
        max_tokens: int = 10,
        refill_rate: float = 1.0,
        cleanup_interval: int = 300  # 5 minutes
    ):
        """Initialize rate limiter.
        
        Args:
            max_tokens: Maximum tokens per bucket
            refill_rate: Token refill rate per second
            cleanup_interval: Cleanup interval in seconds
        """
        self._buckets: Dict[str, RateLimitBucket] = {}
        self._default_max_tokens = max_tokens
        self._default_refill_rate = refill_rate
        self._cleanup_interval = cleanup_interval
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_old_buckets())
    
    def _get_bucket(self, key: str) -> RateLimitBucket:
        """Get or create rate limit bucket for key.
        
        Args:
            key: Rate limit key (e.g., domain, user_id)
            
        Returns:
            RateLimitBucket: Token bucket for the key
        """
        if key not in self._buckets:
            self._buckets[key] = RateLimitBucket(
                max_tokens=self._default_max_tokens,
                refill_rate=self._default_refill_rate,
                current_tokens=self._default_max_tokens
            )
        
        return self._buckets[key]
    
    async def acquire(
        self,
        key: str,
        tokens: int = 1,
        timeout: Optional[float] = None
    ) -> bool:
        """Acquire tokens from rate limiter.
        
        Args:
            key: Rate limit key
            tokens: Number of tokens to acquire
            timeout: Maximum wait time in seconds
            
        Returns:
            bool: True if tokens were acquired
        """
        bucket = self._get_bucket(key)
        
        # Try immediate acquisition
        if bucket.consume(tokens):
            return True
        
        # Calculate wait time
        wait_time = bucket.time_until_tokens(tokens)
        
        # Check timeout
        if timeout is not None and wait_time > timeout:
            return False
        
        # Wait for tokens
        await asyncio.sleep(wait_time)
        
        # Try acquisition again
        return bucket.consume(tokens)
    
    async def wait_for_tokens(self, key: str, tokens: int = 1) -> None:
        """Wait until tokens are available.
        
        Args:
            key: Rate limit key
            tokens: Number of tokens needed
        """
        bucket = self._get_bucket(key)
        
        while not bucket.consume(tokens):
            wait_time = bucket.time_until_tokens(tokens)
            await asyncio.sleep(wait_time)
    
    def get_remaining_tokens(self, key: str) -> float:
        """Get remaining tokens for a key.
        
        Args:
            key: Rate limit key
            
        Returns:
            float: Number of remaining tokens
        """
        bucket = self._get_bucket(key)
        bucket.refill()
        return bucket.current_tokens
    
    def reset_bucket(self, key: str) -> None:
        """Reset rate limit bucket for a key.
        
        Args:
            key: Rate limit key to reset
        """
        if key in self._buckets:
            bucket = self._buckets[key]
            bucket.current_tokens = bucket.max_tokens
            bucket.last_refill = datetime.utcnow()
    
    async def _cleanup_old_buckets(self) -> None:
        """Cleanup old unused buckets periodically."""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                
                current_time = datetime.utcnow()
                cutoff_time = current_time - timedelta(seconds=self._cleanup_interval * 2)
                
                # Remove buckets that haven't been used recently
                keys_to_remove = [
                    key for key, bucket in self._buckets.items()
                    if bucket.last_refill < cutoff_time
                ]
                
                for key in keys_to_remove:
                    del self._buckets[key]
                    
            except Exception:
                # Continue cleanup on error
                pass