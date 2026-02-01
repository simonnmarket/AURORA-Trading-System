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
    
    Example:
        @cache(ttl=3600)
        def get_user_profile(user_id: int):
            return db.get_user(user_id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate cache key from function name and arguments
            key_data = _generate_cache_key(func, args, kwargs, key_prefix)
            
            # Try to get from cache first
            cached_result = CacheManager.get(key_data)
            if cached_result is not None:
                print(f"✅ Cache HIT: {key_data}")
                return cached_result
            
            # Cache miss: compute result
            print(f"⚙️  Computing: {func.__name__}")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_ttl = ttl or CacheManager.DEFAULT_TTL
            CacheManager.set(key_data, result, cache_ttl)
            
            return result
        
        def clear_cache(*args, **kwargs):
            """Clear cache for this function with given arguments."""
            key_data = _generate_cache_key(func, args, kwargs, key_prefix)
            CacheManager.delete(key_data)
        
        wrapper.clear_cache = clear_cache
        wrapper.cache_key_prefix = key_prefix or func.__name__
        
        return wrapper
    
    return decorator


def cache_invalidate(pattern: str):
    """Decorator to invalidate cache patterns after function execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            invalidated = CacheManager.invalidate_pattern(pattern)
            print(f"🔄 Invalidated {invalidated} cache keys matching: {pattern}")
            return result
        return wrapper
    return decorator


def _generate_cache_key(func: Callable, args: tuple, kwargs: dict, prefix: str = "") -> str:
    """Generate cache key from function and arguments."""
    func_name = prefix or func.__name__
    
    try:
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        if params and params[0] == 'self':
            key_parts = [str(arg) for arg in args[1:]]
        else:
            key_parts = [str(arg) for arg in args]
        
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        
        key_data = f"{func_name}:{':'.join(key_parts)}"
    except Exception:
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
    
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    return f"cache:{func_name}:{key_hash}"


def _format_args(args: tuple, kwargs: dict) -> str:
    """Format arguments for display in logs."""
    arg_strs = [str(arg)[:50] for arg in args]
    for k, v in kwargs.items():
        arg_strs.append(f"{k}={str(v)[:50]}")
    return ", ".join(arg_strs)
