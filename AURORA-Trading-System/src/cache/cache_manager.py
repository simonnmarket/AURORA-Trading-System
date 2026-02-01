# Cache Manager for AURORA Trading System
"""
High-level cache operations manager.
Provides consistent interface for cache operations across AURORA system.
"""

from typing import Any, Optional, List
from .redis_client import redis_client


class CacheManager:

    
    DEFAULT_TTL = 3600  # 1 hour default
    
    @staticmethod
    def get(key: str) -> Optional[Any]:

        if redis_client is None:
            return None
        return redis_client.get(key)
    
    @staticmethod

        ttl = ttl or CacheManager.DEFAULT_TTL
        return redis_client.set(key, value, ttl)
    
    @staticmethod
    def delete(key: str) -> bool:

        if redis_client is None:
            return False
        return redis_client.delete(key)
    
    @staticmethod
    def delete_many(keys: List[str]) -> int:

            return 0
    
    @staticmethod
    def exists(key: str) -> bool:

        if redis_client is None:
            return False
        return redis_client.exists(key)
    
    @staticmethod
    def invalidate_pattern(pattern: str) -> int:

        try:
            keys = redis_client.client.keys(pattern)
            if not keys:
                return 0
            return redis_client.client.delete(*keys)
        except Exception as e:

            return 0
    
    @staticmethod
    def flush() -> bool: