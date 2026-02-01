# Redis Client for AURORA Trading System
"""
Redis client wrapper providing connection pooling and basic operations.
Handles JSON serialization for cache values.
"""

import redis
from typing import Any, Optional
import json
import os


class RedisClient:
    """Redis client wrapper for AURORA cache layer.
    
    Provides connection pooling, automatic serialization,
    and high-level cache operations.
    
    Attributes:
        client: Underlying redis.Redis instance
        host: Redis server hostname
        port: Redis server port
        db: Redis database number
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = 0,
        decode_responses: bool = True,
        socket_connect_timeout: int = 5
    ):
        """Initialize Redis connection.
        
        Args:
            host: Redis hostname (default: localhost, can use env var REDIS_HOST)
            port: Redis port (default: 6379, can use env var REDIS_PORT)
            db: Redis database number (default: 0)
            decode_responses: Decode responses as UTF-8 (default: True)
            socket_connect_timeout: Connection timeout in seconds (default: 5)
        
        Raises:
            Exception: If Redis connection fails
        """
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db
        
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=decode_responses,
            socket_connect_timeout=socket_connect_timeout,
            health_check_interval=30
        )
        
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test Redis connection with PING.
        
        Returns:
            bool: True if connection successful, False otherwise
        
        Raises:
            Exception: If connection fails
        """
        try:
            self.client.ping()
            print(f"✅ Redis connection successful! ({self.host}:{self.port})")
            return True
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Deserialized value or None if key not found
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except Exception as e:
            print(f"❌ Error getting cache key '{key}': {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time-to-live in seconds (default: 3600)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"❌ Error setting cache key '{key}': {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete cache key.
        
        Args:
            key: Cache key to delete
        
        Returns:
            bool: True if deleted, False if key not found
        """
        try:
            result = self.client.delete(key)
            return result > 0
        except Exception as e:
            print(f"❌ Error deleting cache key '{key}': {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache.
        
        Args:
            key: Cache key
        
        Returns:
            bool: True if key exists, False otherwise
        """
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            print(f"❌ Error checking cache key '{key}': {e}")
            return False
    
    def ttl(self, key: str) -> int:
        """Get TTL for cache key.
        
        Args:
            key: Cache key
        
        Returns:
            int: TTL in seconds (-1 if no expiry, -2 if key not found)
        """
        try:
            return self.client.ttl(key)
        except Exception as e:
            print(f"❌ Error getting TTL for key '{key}': {e}")
            return -2
    
    def flush(self) -> bool:
        """Clear all cache in current database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.flushdb()
            print("✅ Cache flushed")
            return True
        except Exception as e:
            print(f"❌ Error flushing cache: {e}")
            return False
    
    def close(self):
        """Close Redis connection."""
        try:
            self.client.close()
        except Exception as e:
            print(f"❌ Error closing connection: {e}")


# Global instance for application use
try:
    redis_client = RedisClient()
except Exception as e:
    print(f"⚠️  Redis initialization failed: {e}")
    redis_client = None
