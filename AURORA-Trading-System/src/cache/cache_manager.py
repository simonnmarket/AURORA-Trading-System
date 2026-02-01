# Cache Manager for AURORA Trading System
"""
High-level cache operations manager.
Provides consistent interface for cache operations across AURORA system.
"""

from typing import Any, Optional, List
from .redis_client import redis_client


class CacheManager:
    """Unified cache operations interface.
    
    Provides high-level methods for cache operations with sensible defaults.
    All operations are thread-safe through Redis itself.
    """
    
    DEFAULT_TTL = 3600  # 1 hour default
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Value from cache or None if not found
        
        Example:
            value = CacheManager.get("user:123:profile")
        """
        if redis_client is None:
            return None
        return redis_client.get(key)
    
    @staticmethod
    def set(
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (default: DEFAULT_TTL)
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            CacheManager.set("user:123:profile", user_data, ttl=7200)
        """
        if redis_client is None:
            return False
        
        ttl = ttl or CacheManager.DEFAULT_TTL
        return redis_client.set(key, value, ttl)
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete cache key.
        
        Args:
            key: Cache key
        
        Returns:
            bool: True if deleted, False if not found
        
        Example:
            CacheManager.delete("user:123:profile")
        """
        if redis_client is None:
            return False
        return redis_client.delete(key)
    
    @staticmethod
    def delete_many(keys: List[str]) -> int:
        """Delete multiple cache keys.
        
        Args:
            keys: List of cache keys
        
        Returns:
            int: Number of keys deleted
        
        Example:
            deleted = CacheManager.delete_many(["key1", "key2", "key3"])
        """
        if redis_client is None or not keys:
            return 0
        
        try:
            return redis_client.client.delete(*keys)
        except Exception as e:
            print(f"❌ Error deleting multiple keys: {e}")
            return 0
    
    @staticmethod
    def exists(key: str) -> bool:
        """Check if key exists in cache.
        
        Args:
            key: Cache key
        
        Returns:
            bool: True if key exists, False otherwise
        
        Example:
            if CacheManager.exists("user:123:profile"):
                ...
        """
        if redis_client is None:
            return False
        return redis_client.exists(key)
    
    @staticmethod
    def invalidate_pattern(pattern: str) -> int:
        """Invalidate cache keys matching pattern.
        
        Useful for cache coherence when data changes.
        WARNING: Pattern matching is expensive on large datasets.
        
        Args:
            pattern: Redis pattern (e.g., "user:123:*")
        
        Returns:
            int: Number of keys deleted
        
        Example:
            CacheManager.invalidate_pattern("user:123:*")
        """
        if redis_client is None:
            return 0
        
        try:
            keys = redis_client.client.keys(pattern)
            if not keys:
                return 0
            return redis_client.client.delete(*keys)
        except Exception as e:
            print(f"❌ Error invalidating pattern '{pattern}': {e}")
            return 0
    
    @staticmethod
    def flush() -> bool:
        """Clear all cache.
        
        WARNING: This deletes ALL keys in the current Redis database.
        Use with caution in production.
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            CacheManager.flush()
        """
        if redis_client is None:
            return False
        return redis_client.flush()
    
    @staticmethod
    def get_ttl(key: str) -> int:
        """Get remaining TTL for key.
        
        Args:
            key: Cache key
        
        Returns:
            int: TTL in seconds (-1 if no expiry, -2 if key not found)
        
        Example:
            ttl = CacheManager.get_ttl("user:123:profile")
        """
        if redis_client is None:
            return -2
        return redis_client.ttl(key)
