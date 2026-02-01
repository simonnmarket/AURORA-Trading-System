"""
Unit tests for AURORA cache layer.
Tests Redis connection, cache manager operations, and decorator functionality.
"""

import pytest
from src.cache.cache_manager import CacheManager
from src.cache.decorators import cache, cache_invalidate


# ============================================================================
# Cache Manager Tests
# ============================================================================

def test_cache_set_get():
    """Test basic cache set and get operations."""
    CacheManager.set("test_key_1", "test_value", ttl=60)
    result = CacheManager.get("test_key_1")
    assert result == "test_value"


def test_cache_set_get_dict():
    """Test caching complex data types (dict)."""
    test_data = {
        "user_id": 123,
        "name": "Alice",
        "email": "alice@example.com"
    }
    CacheManager.set("user:123", test_data, ttl=60)
    result = CacheManager.get("user:123")
    assert result == test_data
    assert result["user_id"] == 123


def test_cache_get_nonexistent():
    """Test getting non-existent key returns None."""
    result = CacheManager.get("nonexistent_key_xyz")
    assert result is None


def test_cache_delete():
    """Test cache delete operation."""
    CacheManager.set("delete_key", "value", ttl=60)
    assert CacheManager.exists("delete_key") is True
    
    deleted = CacheManager.delete("delete_key")
    assert deleted is True
    
    result = CacheManager.get("delete_key")
    assert result is None


def test_cache_delete_nonexistent():
    """Test deleting non-existent key returns False."""
    result = CacheManager.delete("nonexistent_delete_key")
    assert result is False


def test_cache_exists():
    """Test key existence check."""
    CacheManager.set("exists_test", "value", ttl=60)
    assert CacheManager.exists("exists_test") is True
    assert CacheManager.exists("nonexistent_exists") is False


def test_cache_delete_many():
    """Test deleting multiple keys."""
    keys = ["key_1", "key_2", "key_3"]
    for key in keys:
        CacheManager.set(key, f"value_{key}", ttl=60)
    
    deleted = CacheManager.delete_many(keys)
    assert deleted == 3


def test_cache_invalidate_pattern():
    """Test pattern-based cache invalidation."""
    # Set multiple keys with pattern
    for i in range(5):
        CacheManager.set(f"user:100:cache_{i}", f"value_{i}", ttl=60)
    
    # Invalidate pattern
    invalidated = CacheManager.invalidate_pattern("user:100:*")
    assert invalidated == 5


# ============================================================================
# Cache Decorator Tests
# ============================================================================

def test_cache_decorator_basic():
    """Test @cache decorator basic functionality."""
    call_count = 0
    
    @cache(ttl=60)
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call: compute
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call: from cache (no additional compute)
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 1  # NOT incremented


def test_cache_decorator_different_args():
    """Test @cache with different arguments computes separately."""
    call_count = 0
    
    @cache(ttl=60)
    def multiply(a, b):
        nonlocal call_count
        call_count += 1
        return a * b
    
    # Different arguments should NOT share cache
    result1 = multiply(2, 3)
    assert result1 == 6
    assert call_count == 1
    
    result2 = multiply(2, 4)
    assert result2 == 8
    assert call_count == 2  # Different args, new computation


def test_cache_decorator_kwargs():
    """Test @cache with keyword arguments."""
    call_count = 0
    
    @cache(ttl=60)
    def create_user(name, age=0):
        nonlocal call_count
        call_count += 1
        return {"name": name, "age": age}
    
    # Call with kwargs
    result1 = create_user("Alice", age=30)
    assert result1 == {"name": "Alice", "age": 30}
    assert call_count == 1
    
    # Same call: from cache
    result2 = create_user("Alice", age=30)
    assert result2 == {"name": "Alice", "age": 30}
    assert call_count == 1  # NOT incremented


def test_cache_decorator_clear_cache():
    """Test clear_cache method on decorated function."""
    call_count = 0
    
    @cache(ttl=60)
    def get_value(key):
        nonlocal call_count
        call_count += 1
        return f"value_{key}"
    
    # Cache a value
    result1 = get_value("test")
    assert call_count == 1
    
    # Clear cache for this specific call
    get_value.clear_cache("test")
    
    # Next call recomputes
    result2 = get_value("test")
    assert call_count == 2


def test_cache_decorator_with_prefix():
    """Test @cache with custom key prefix."""
    call_count = 0
    
    @cache(ttl=60, key_prefix="user_profile")
    def get_profile(user_id):
        nonlocal call_count
        call_count += 1
        return {"id": user_id, "name": f"User{user_id}"}
    
    result1 = get_profile(123)
    assert result1["id"] == 123
    assert call_count == 1
    
    result2 = get_profile(123)
    assert call_count == 1  # From cache


def test_cache_decorator_complex_return():
    """Test @cache with complex data structures."""
    @cache(ttl=60)
    def get_report():
        return {
            "trades": [
                {"id": 1, "symbol": "BTC/USD", "price": 45000},
                {"id": 2, "symbol": "ETH/USD", "price": 2500}
            ],
            "stats": {
                "total": 2,
                "value": 47500
            }
        }
    
    result1 = get_report()
    result2 = get_report()
    
    assert result1 == result2
    assert len(result1["trades"]) == 2
    assert result1["stats"]["value"] == 47500


# ============================================================================
# Cache Invalidation Tests
# ============================================================================

def test_cache_invalidate_decorator():
    """Test @cache_invalidate decorator for cache coherence."""
    call_count = 0
    
    @cache_invalidate(pattern="data:*")
    def update_data(key, value):
        nonlocal call_count
        call_count += 1
        return {"key": key, "value": value}
    
    # Execution invalidates matching cache patterns
    result = update_data("test", "value")
    assert result == {"key": "test", "value": "value"}


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_cache_ttl_validation():
    """Test cache with custom TTL."""
    CacheManager.set("ttl_test", "value", ttl=1)
    
    # Should exist immediately
    assert CacheManager.exists("ttl_test") is True


def test_cache_multiple_types():
    """Test caching different data types."""
    # String
    CacheManager.set("str_key", "string_value", ttl=60)
    assert CacheManager.get("str_key") == "string_value"
    
    # Integer
    CacheManager.set("int_key", 42, ttl=60)
    assert CacheManager.get("int_key") == 42
    
    # List
    CacheManager.set("list_key", [1, 2, 3], ttl=60)
    assert CacheManager.get("list_key") == [1, 2, 3]
    
    # Dict
    CacheManager.set("dict_key", {"a": 1, "b": 2}, ttl=60)
    assert CacheManager.get("dict_key") == {"a": 1, "b": 2}
    
    # Boolean
    CacheManager.set("bool_key", True, ttl=60)
    assert CacheManager.get("bool_key") is True


# ============================================================================
# Integration Tests
# ============================================================================

def test_cache_decorator_integration_with_manager():
    """Test decorator works well with CacheManager."""
    call_count = 0
    
    @cache(ttl=60, key_prefix="integration")
    def compute_total(a, b):
        nonlocal call_count
        call_count += 1
        return a + b
    
    # Use decorator
    result1 = compute_total(10, 20)
    assert result1 == 30
    
    # Can also clear via manager using pattern
    invalidated = CacheManager.invalidate_pattern("cache:integration:*")
    assert invalidated == 1
    
    # Next call recomputes
    result2 = compute_total(10, 20)
    assert call_count == 2


if __name__ == "__main__":
    # Run: pytest tests/test_cache.py -v
    pytest.main([__file__, "-v"])
