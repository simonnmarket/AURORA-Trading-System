# API Decorators for AURORA
"""
Decorators for request validation, logging, performance timing.
Applied to route handlers for cross-cutting concerns.
"""

from functools import wraps
from typing import Callable, Any
import time
import logging
from datetime import datetime

logger = logging.getLogger("AURORA.API")


def validate_trade(func: Callable) -> Callable:
    """
    Decorator to validate trade data before processing.
    
    Validates:
    - Price > 0
    - Quantity > 0
    - Symbol not empty
    - Side in ["BUY", "SELL"]
    
    Usage:
        @router.post("/trades")
        @validate_trade
        async def create_trade(trade: TradeCreate):
            ...
    
    Raises:
        ValueError: If validation fails
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract trade from kwargs (named parameter)
        trade = kwargs.get('trade') or (args[0] if args else None)
        
        if trade:
            # Validate price
            if not hasattr(trade, 'price') or trade.price <= 0:
                logger.warning(f"Invalid price: {trade.price}")
                raise ValueError("Price must be greater than 0")
            
            # Validate quantity
            if not hasattr(trade, 'quantity') or trade.quantity <= 0:
                logger.warning(f"Invalid quantity: {trade.quantity}")
                raise ValueError("Quantity must be greater than 0")
            
            # Validate symbol
            if not hasattr(trade, 'symbol') or not trade.symbol:
                logger.warning("Symbol is empty")
                raise ValueError("Symbol is required")
            
            # Validate side
            if hasattr(trade, 'side') and trade.side not in ["BUY", "SELL"]:
                logger.warning(f"Invalid side: {trade.side}")
                raise ValueError("Side must be BUY or SELL")
            
            logger.info(f"✅ Trade validation passed: {trade.symbol} {trade.side} {trade.quantity}")
        
        return await func(*args, **kwargs)
    
    return wrapper


def log_event(func: Callable) -> Callable:
    """
    Decorator to log event creation.
    
    Logs:
    - Event type
    - Aggregate ID
    - Timestamp
    - User who triggered it
    
    Usage:
        @router.post("/trades")
        @log_event
        async def create_trade(trade: TradeCreate):
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        logger.info(f"📝 Event starting: {func.__name__}")
        
        try:
            result = await func(*args, **kwargs)
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ Event completed: {func.__name__} ({elapsed:.2f}s)")
            return result
        except Exception as e:
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"❌ Event failed: {func.__name__} - {str(e)} ({elapsed:.2f}s)")
            raise
    
    return wrapper


def cache_invalidate(pattern: str) -> Callable:
    """
    Decorator to invalidate cache patterns after function execution.
    
    Usage:
        @router.post("/trades")
        @cache_invalidate("cache:*trade*")
        async def create_trade(trade: TradeCreate):
            ...
    
    Args:
        pattern: Cache key pattern to invalidate (e.g., "cache:get_trades:*")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidate cache
            from src.cache.cache_manager import CacheManager
            invalidated = CacheManager.invalidate_pattern(pattern)
            logger.info(f"🔄 Invalidated {invalidated} keys matching: {pattern}")
            
            return result
        
        return wrapper
    return decorator


def timing(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.
    
    Useful for performance monitoring and profiling.
    
    Usage:
        @router.get("/trades")
        @timing
        async def get_trades():
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        start_datetime = datetime.utcnow()
        
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            logger.info(
                f"⏱️  {func.__name__} executed in {elapsed:.3f}s "
                f"(started: {start_datetime.isoformat()})"
            )
            
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"⏱️  {func.__name__} FAILED in {elapsed:.3f}s - {str(e)}"
            )
            raise
    
    return wrapper


def audit_log(func: Callable) -> Callable:
    """
    Decorator to create audit trail for sensitive operations.
    
    Logs:
    - User (from token)
    - Operation
    - Timestamp
    - Status (success/failure)
    
    Usage:
        @router.post("/trades")
        @audit_log
        async def create_trade(trade: TradeCreate):
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        timestamp = datetime.utcnow().isoformat()
        operation = func.__name__
        
        # Extract request context if available
        user_id = kwargs.get('user_id', 'SYSTEM')
        
        audit_entry = {
            'timestamp': timestamp,
            'operation': operation,
            'user_id': user_id,
            'status': 'STARTED'
        }
        
        logger.info(f"🔐 AUDIT: {audit_entry}")
        
        try:
            result = await func(*args, **kwargs)
            audit_entry['status'] = 'SUCCESS'
            logger.info(f"🔐 AUDIT RESULT: {audit_entry}")
            return result
        except Exception as e:
            audit_entry['status'] = 'FAILED'
            audit_entry['error'] = str(e)
            logger.error(f"🔐 AUDIT FAILED: {audit_entry}")
            raise
    
    return wrapper
