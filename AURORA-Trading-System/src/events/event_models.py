# Event Models for AURORA Trading System
"""
Domain events using Event Sourcing pattern.
All events are immutable and represent facts that have happened.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum
import uuid


class EventType(str, Enum):
    """Enumeration of all event types in the system."""
    # Trade events
    TRADE_CREATED = "TRADE_CREATED"
    TRADE_EXECUTED = "TRADE_EXECUTED"
    TRADE_CANCELLED = "TRADE_CANCELLED"
    
    # Cache events
    CACHE_HIT = "CACHE_HIT"
    CACHE_MISS = "CACHE_MISS"
    CACHE_INVALIDATED = "CACHE_INVALIDATED"
    
    # System events
    SYSTEM_STARTUP = "SYSTEM_STARTUP"
    SYSTEM_SHUTDOWN = "SYSTEM_SHUTDOWN"
    SYSTEM_ERROR = "SYSTEM_ERROR"


@dataclass
class Event:
    """Base event class for all domain events.
    
    Represents a fact that has occurred in the system.
    Events are immutable once created and stored.
    
    Attributes:
        event_id: Unique identifier for this event
        event_type: Type of event (EventType enum)
        aggregate_id: Identifier of the aggregate this event belongs to
        timestamp: When the event occurred
        data: Event payload with domain-specific data
        version: Event version for migration purposes
        user_id: Optional user who triggered the event
    """
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = field(default="")
    aggregate_id: str = field(default="")
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    version: int = field(default=1)
    user_id: Optional[str] = field(default=None)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation.
        
        Returns:
            Dictionary with all event fields (ISO format timestamps)
        """
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def to_json(self) -> str:
        """Convert event to JSON string.
        
        Returns:
            JSON representation of the event
        """
        import json
        return json.dumps(self.to_dict())
    
    def __hash__(self):
        """Hash based on event_id for set operations."""
        return hash(self.event_id)
    
    def __repr__(self) -> str:
        """String representation of event."""
        return (
            f"Event(type={self.event_type}, "
            f"aggregate={self.aggregate_id}, "
            f"timestamp={self.timestamp})"
        )


@dataclass
class TradeEvent(Event):
    """Event representing a trade operation.
    
    Examples of trade events:
        - Trade execution
        - Trade cancellation
        - Trade settlement
    """
    
    event_type: str = field(default=EventType.TRADE_CREATED)
    
    # Common trade event data fields (stored in 'data' dict)
    # symbol: str (e.g., "BTC/USD")
    # price: float
    # quantity: float
    # side: str ("BUY" or "SELL")
    # status: str ("PENDING", "EXECUTED", "CANCELLED")


@dataclass
class CacheEvent(Event):
    """Event representing a cache operation.
    
    Examples of cache events:
        - Cache hit
        - Cache miss
        - Cache invalidation
        - Cache eviction
    """
    
    event_type: str = field(default=EventType.CACHE_HIT)
    
    # Common cache event data fields (stored in 'data' dict)
    # cache_key: str
    # operation: str ("GET", "SET", "DELETE", "INVALIDATE")
    # hit: bool (for cache operations)
    # ttl: int (for SET operations)


@dataclass
class SystemEvent(Event):
    """Event representing a system-level event.
    
    Examples of system events:
        - System startup
        - System shutdown
        - System errors
        - Configuration changes
    """
    
    event_type: str = field(default=EventType.SYSTEM_STARTUP)
    
    # Common system event data fields
    # level: str ("INFO", "WARNING", "ERROR", "CRITICAL")
    # message: str
    # component: str (which part of system)
    # error_code: Optional[str]


def create_trade_event(
    aggregate_id: str,
    event_type: str,
    symbol: str,
    price: float,
    quantity: float,
    side: str,
    status: str,
    user_id: Optional[str] = None
) -> TradeEvent:
    """Factory function to create a trade event.
    
    Args:
        aggregate_id: Trade ID
        event_type: Type of trade event
        symbol: Trading pair symbol
        price: Trade price
        quantity: Trade quantity
        side: Buy or sell
        status: Trade status
        user_id: User who initiated trade
    
    Returns:
        TradeEvent instance
    """
    return TradeEvent(
        event_type=event_type,
        aggregate_id=aggregate_id,
        data={
            'symbol': symbol,
            'price': price,
            'quantity': quantity,
            'side': side,
            'status': status
        },
        user_id=user_id
    )


def create_cache_event(
    aggregate_id: str,
    event_type: str,
    cache_key: str,
    operation: str,
    hit: Optional[bool] = None,
    user_id: Optional[str] = None
) -> CacheEvent:
    """Factory function to create a cache event.
    
    Args:
        aggregate_id: Cache aggregate ID
        event_type: Type of cache event
        cache_key: Cache key
        operation: Operation type (GET, SET, DELETE, etc)
        hit: Whether it was a cache hit (for GET operations)
        user_id: Optional user identifier
    
    Returns:
        CacheEvent instance
    """
    data = {
        'cache_key': cache_key,
        'operation': operation
    }
    if hit is not None:
        data['hit'] = hit
    
    return CacheEvent(
        event_type=event_type,
        aggregate_id=aggregate_id,
        data=data,
        user_id=user_id
    )


def create_system_event(
    event_type: str,
    level: str,
    message: str,
    component: str,
    error_code: Optional[str] = None,
    user_id: Optional[str] = None
) -> SystemEvent:
    """Factory function to create a system event.
    
    Args:
        event_type: Type of system event
        level: Event level (INFO, WARNING, ERROR, CRITICAL)
        message: Human-readable message
        component: Component that generated event
        error_code: Optional error code
        user_id: Optional user identifier
    
    Returns:
        SystemEvent instance
    """
    return SystemEvent(
        event_type=event_type,
        aggregate_id=f"sys:{component}",
        data={
            'level': level,
            'message': message,
            'component': component,
            'error_code': error_code
        },
        user_id=user_id
    )
