# Cache Decorators for AURORA Trading System
"""
Function decorators for automatic caching.
Provides @cache decorator for transparent memoization of function results.
"""

from functools import wraps
from typing import Callable, Any, Optional
from .cache_manager import CacheManager
import hashlib
import inspect


def cache(ttl: Optional[int] = None, key_prefix: str = ""):
    """Decorator to cache function results.
    
    Automatically caches function results based on arguments.
<<<<
    
    Example:
        @cache(ttl=3600)
        def get_user_profile(user_id: int):
<<<<<<
