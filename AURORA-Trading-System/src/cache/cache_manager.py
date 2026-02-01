# Cache Manager for AURORA Trading System
"""
High-level cache operations manager.
Provides consistent interface for cache operations across AURORA system.
"""

from typing import Any, Optional, List
from .redis_client import redis_client


class CacheManager:
    """Unified cache operations interface."""
    
    DEFAULT_TTL = 3600  # 1 hour default
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache."""
        if redis_client is None:
            return None
        return redis_client.get(key)
    
    @staticmethod
    def set(key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL."""
        if redis_client is None:
            return False
        ttl = ttl or CacheManager.DEFAULT_TTL
        return redis_client.set(key, value, ttl)
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete cache key."""
        if redis_client is None:
            return False
        return redis_client.delete(key)
    
    @staticmethod
    def delete_many(keys: List[str]) -> int:
        """Delete multiple cache keys."""
        if redis_client is None or not keys:
            return 0
        try:
            return redis_client.client.delete(*keys)
        except Exception as e:
            return 0
    
    @staticmethod
    def exists(key: str) -> bool:
        """Check if key exists in cache."""
        if redis_client is None:
            return False
        return redis_client.exists(key)
    
    @staticmethod
    def invalidate_pattern(pattern: str) -> int:
        """Invalidate cache keys matching pattern."""
        if redis_client is None:
            return 0
        try:
            keys = redis_client.client.keys(pattern)
            if not keys:
                return 0
            return redis_client.client.delete(*keys)
        except Exception as e:
            return 0
    
    @staticmethod
    def flush() -> bool:
        """Clear all cache."""
        if redis_client is None:
            return False
        return redis_client.flush()
    
    @staticmethod
    def get_ttl(key: str) -> int:
        """Get remaining TTL for key."""
        if redis_client is None:
            return -2
        return redis_client.ttl(key)
