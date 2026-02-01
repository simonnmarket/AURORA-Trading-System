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
    Cache key is generated from function name and arguments.
    
    Args:
        ttl: Time-to-live in seconds (default: CacheManager.DEFAULT_TTL)
        key_prefix: Optional prefix for cache keys
    
    Returns:
        Decorator function
    
    Example:
        @cache(ttl=3600)
        def get_user_profile(user_id: int):
            # Expensive database query
            return db.get_user(user_id)
        
        # First call: computes and caches
        profile = get_user_profile(123)
        
        # Second call: returns from cache
        profile = get_user_profile(123)
    
    Example with prefix:
        @cache(ttl=1800, key_prefix="user_profile")
        def get_profile(user_id):
            ...
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
            print(f"⚙️  Computing: {func.__name__}({_format_args(args, kwargs)})")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_ttl = ttl or CacheManager.DEFAULT_TTL
            CacheManager.set(key_data, result, cache_ttl)
            
            return result
        
        # Add cache control methods to wrapped function
        def clear_cache(*args, **kwargs):
            """Clear cache for this function with given arguments."""
            key_data = _generate_cache_key(func, args, kwargs, key_prefix)
            CacheManager.delete(key_data)
        
        wrapper.clear_cache = clear_cache
        wrapper.cache_key_prefix = key_prefix or func.__name__
        
        return wrapper
    
    return decorator


def cache_invalidate(pattern: str):
    """Decorator to invalidate cache patterns after function execution.
    
    Useful for invalidating related cached values after mutations.
    
    Args:
        pattern: Redis pattern for cache invalidation
    
    Example:
        @cache_invalidate(pattern="user:*:profile")
        def update_user(user_id, data):
            # Update database
            db.update_user(user_id, data)
            # Cache invalidation happens automatically
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            # Invalidate cache pattern
            invalidated = CacheManager.invalidate_pattern(pattern)
            print(f"🔄 Invalidated {invalidated} cache keys matching: {pattern}")
            return result
        
        return wrapper
    
    return decorator


def _generate_cache_key(
    func: Callable,
    args: tuple,
    kwargs: dict,
    prefix: str = ""
) -> str:
    """Generate cache key from function and arguments.
    
    Args:
        func: Function being cached
        args: Positional arguments
        kwargs: Keyword arguments
        prefix: Optional cache key prefix
    
    Returns:
        str: Cache key (MD5 hash based)
    """
    # Start with function name
    func_name = prefix or func.__name__
    
    # Serialize arguments (excluding 'self' for methods)
    try:
        # Get function signature to skip 'self' parameter
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        # Build key data from args
        if params and params[0] == 'self':
            # Skip 'self' for methods
            key_parts = [str(arg) for arg in args[1:]]
        else:
            key_parts = [str(arg) for arg in args]
        
        # Add kwargs
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        
        key_data = f"{func_name}:{':'.join(key_parts)}"
    except Exception:
        # Fallback if signature inspection fails
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
    
    # Create MD5 hash of key data
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    
    return f"cache:{func_name}:{key_hash}"


def _format_args(args: tuple, kwargs: dict) -> str:
    """Format arguments for display in logs.
    
    Args:
        args: Positional arguments
        kwargs: Keyword arguments
    
    Returns:
        str: Formatted argument string
    """
    arg_strs = [str(arg)[:50] for arg in args]  # Truncate long args
    for k, v in kwargs.items():
        arg_strs.append(f"{k}={str(v)[:50]}")
    return ", ".join(arg_strs)
