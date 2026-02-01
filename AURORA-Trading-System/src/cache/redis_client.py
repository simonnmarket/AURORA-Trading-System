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
    """
    
    def __init__(self, host: str = None, port: int = None, db: int = 0):
        """Initialize Redis connection."""
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db
        
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True,
            socket_connect_timeout=5,
            health_check_interval=30
        )
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test Redis connection with PING."""
        try:
            self.client.ping()
            print(f"✅ Redis connection successful! ({self.host}:{self.port})")
            return True
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"❌ Error getting cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL."""
        try:
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"❌ Error setting cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete cache key."""
        try:
            return self.client.delete(key) > 0
        except Exception as e:
            print(f"❌ Error deleting cache: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            return False
    
    def ttl(self, key: str) -> int:
        """Get TTL for cache key."""
        try:
            return self.client.ttl(key)
        except Exception as e:
            return -2
    
    def flush(self) -> bool:
        """Clear all cache."""
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            return False
    
    def close(self):
        """Close Redis connection."""
        try:
            self.client.close()
        except Exception as e:
            pass


# Global instance for application use
try:
    redis_client = RedisClient()
except Exception as e:
    print(f"⚠️  Redis initialization: {e}")
    redis_client = None
