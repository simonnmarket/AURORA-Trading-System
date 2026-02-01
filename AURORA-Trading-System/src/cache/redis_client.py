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