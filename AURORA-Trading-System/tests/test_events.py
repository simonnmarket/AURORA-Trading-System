"""
Unit tests for AURORA Event Sourcing implementation.
Tests event models, event store, and event processor functionality.
"""

import pytest
from datetime import datetime, timedelta
from src.events.event_models import (
    Event, EventType, TradeEvent, CacheEvent, SystemEvent,
    create_trade_event, create_cache_event, create_system_event
)
from src.events.event_store import EventStore, EventRecord
from src.events.event_processor import EventProcessor


# ============================================================================
# Event Model Tests
# ============================================================================

def test_event_creation():
    """Test basic event creation."""
    event = Event(
        event_type=EventType.TRADE_CREATED,
        aggregate_id="trade:123",
        data={"symbol": "BTC/USD", "price": 45000}
    )
    
    assert event.event_type == EventType.TRADE_CREATED
    assert event.aggregate_id == "trade:123"
    assert event.data["symbol"] == "BTC/USD"
    assert event.event_id is not None


def test_event_to_dict():
    """Test event serialization to dict."""
    event = Event(
        event_type=EventType.CACHE_HIT,
        aggregate_id="cache:key1",
        data={"hit": True}
    )
    
    event_dict = event.to_dict()
    
    assert event_dict["event_type"] == EventType.CACHE_HIT
    assert event_dict["aggregate_id"] == "cache:key1"
    assert "timestamp" in event_dict
    assert isinstance(event_dict["timestamp"], str)


def test_event_to_json():
    """Test event serialization to JSON."""
    event = Event(
        event_type=EventType.SYSTEM_STARTUP,
        aggregate_id="sys:core",
        data={"message": "System started"}
    )
    
    json_str = event.to_json()
    
    assert isinstance(json_str, str)
    assert "SYSTEM_STARTUP" in json_str
    assert "sys:core" in json_str


def test_trade_event_factory():
    """Test trade event factory function."""
    event = create_trade_event(
        aggregate_id="trade:456",
        event_type=EventType.TRADE_EXECUTED,
        symbol="ETH/USD",
        price=2500,
        quantity=10,
        side="BUY",
        status="EXECUTED"
    )
    
    assert isinstance(event, TradeEvent)
    assert event.data["symbol"] == "ETH/USD"
    assert event.data["price"] == 2500
    assert event.data["side"] == "BUY"


def test_cache_event_factory():
    """Test cache event factory function."""
    event = create_cache_event(
        aggregate_id="cache:userprofile",
        event_type=EventType.CACHE_HIT,
        cache_key="user:123:profile",
        operation="GET",
        hit=True
    )
    
    assert isinstance(event, CacheEvent)
    assert event.data["cache_key"] == "user:123:profile"
    assert event.data["hit"] is True


def test_system_event_factory():
    """Test system event factory function."""
    event = create_system_event(
        event_type=EventType.SYSTEM_STARTUP,
        level="INFO",
        message="Application started",
        component="CORE"
    )
    
    assert isinstance(event, SystemEvent)
    assert event.data["level"] == "INFO"
    assert event.data["component"] == "CORE"
    assert event.aggregate_id == "sys:CORE"


def test_event_hash():
    """Test event hashing for set operations."""
    event1 = Event(event_type=EventType.CACHE_HIT)
    event2 = Event(event_type=EventType.CACHE_MISS, event_id=event1.event_id)
    event3 = Event(event_type=EventType.CACHE_HIT)
    
    # Same event_id should have same hash
    assert hash(event1) == hash(event2)
    # Different event_id should have different hash
    assert hash(event1) != hash(event3)


# ============================================================================
# Event Store Tests
# ============================================================================

def test_event_store_append():
    """Test appending events to store."""
    store = EventStore()
    store.clear()  # Start fresh
    
    event = Event(
        event_type=EventType.TRADE_CREATED,
        aggregate_id="trade:789",
        data={"symbol": "BTC/USD"}
    )
    
    result = store.append(event)
    assert result is True


def test_event_store_get_event():
    """Test retrieving a single event."""
    store = EventStore()
    store.clear()
    
    event = create_trade_event(
        aggregate_id="trade:111",
        event_type=EventType.TRADE_CREATED,
        symbol="BTC/USD",
        price=45000,
        quantity=1,
        side="BUY",
        status="CREATED"
    )
    
    store.append(event)
    retrieved = store.get_event(event.event_id)
    
    assert retrieved is not None
    assert retrieved.event_id == event.event_id
    assert retrieved.data["symbol"] == "BTC/USD"


def test_event_store_get_nonexistent():
    """Test retrieving non-existent event."""
    store = EventStore()
    
    result = store.get_event("nonexistent_id")
    assert result is None


def test_event_store_get_by_aggregate():
    """Test retrieving events for an aggregate."""
    store = EventStore()
    store.clear()
    
    trade_id = "trade:222"
    
    # Create and append multiple events for same aggregate
    event1 = create_trade_event(
        aggregate_id=trade_id,
        event_type=EventType.TRADE_CREATED,
        symbol="BTC/USD",
        price=45000,
        quantity=1,
        side="BUY",
        status="CREATED"
    )
    
    event2 = create_trade_event(
        aggregate_id=trade_id,
        event_type=EventType.TRADE_EXECUTED,
        symbol="BTC/USD",
        price=45100,
        quantity=1,
        side="BUY",
        status="EXECUTED"
    )
    
    store.append(event1)
    store.append(event2)
    
    events = store.get_events_by_aggregate(trade_id)
    
    assert len(events) == 2
    assert events[0].event_type == EventType.TRADE_CREATED
    assert events[1].event_type == EventType.TRADE_EXECUTED


def test_event_store_get_by_type():
    """Test retrieving events by type."""
    store = EventStore()
    store.clear()
    
    # Create events of different types
    trade_event = create_trade_event(
        aggregate_id="trade:333",
        event_type=EventType.TRADE_CREATED,
        symbol="BTC/USD",
        price=45000,
        quantity=1,
        side="BUY",
        status="CREATED"
    )
    
    cache_event = create_cache_event(
        aggregate_id="cache:key1",
        event_type=EventType.CACHE_HIT,
        cache_key="key1",
        operation="GET",
        hit=True
    )
    
    store.append(trade_event)
    store.append(cache_event)
    
    trade_events = store.get_events_by_type(EventType.TRADE_CREATED)
    cache_events = store.get_events_by_type(EventType.CACHE_HIT)
    
    assert len(trade_events) == 1
    assert len(cache_events) == 1


def test_event_store_append_many():
    """Test appending multiple events."""
    store = EventStore()
    store.clear()
    
    events = [
        create_cache_event(
            aggregate_id=f"cache:key{i}",
            event_type=EventType.CACHE_HIT,
            cache_key=f"key{i}",
            operation="GET"
        )
        for i in range(5)
    ]
    
    count = store.append_many(events)
    assert count == 5


def test_event_store_count():
    """Test counting events."""
    store = EventStore()
    store.clear()
    
    initial_count = store.get_event_count()
    
    event = Event(event_type=EventType.CACHE_HIT, aggregate_id="cache:test")
    store.append(event)
    
    new_count = store.get_event_count()
    assert new_count == initial_count + 1


# ============================================================================
# Event Processor Tests
# ============================================================================

def test_event_processor_replay_single():
    """Test replaying a single event."""
    store = EventStore()
    store.clear()
    
    processor = EventProcessor(store)
    
    event = create_trade_event(
        aggregate_id="trade:444",
        event_type=EventType.TRADE_CREATED,
        symbol="BTC/USD",
        price=45000,
        quantity=1,
        side="BUY",
        status="CREATED"
    )
    
    store.append(event)
    state = processor.replay_events("trade:444")
    
    assert state["symbol"] == "BTC/USD"
    assert state["price"] == 45000
    assert state["status"] == "created"
    assert state["event_count"] == 1


def test_event_processor_replay_sequence():
    """Test replaying sequence of events."""
    store = EventStore()
    store.clear()
    
    processor = EventProcessor(store)
    trade_id = "trade:555"
    
    # Create event sequence
    event1 = create_trade_event(
        aggregate_id=trade_id,
        event_type=EventType.TRADE_CREATED,
        symbol="ETH/USD",
        price=2500,
        quantity=10,
        side="BUY",
        status="CREATED"
    )
    
    event2 = create_trade_event(
        aggregate_id=trade_id,
        event_type=EventType.TRADE_EXECUTED,
        symbol="ETH/USD",
        price=2510,
        quantity=10,
        side="BUY",
        status="EXECUTED"
    )
    
    store.append(event1)
    store.append(event2)
    
    state = processor.replay_events(trade_id)
    
    assert state["status"] == "executed"
    assert state["version"] == 2
    assert state["event_count"] == 2


def test_event_processor_cache_stats():
    """Test processor tracking cache statistics."""
    store = EventStore()
    store.clear()
    
    processor = EventProcessor(store)
    cache_id = "cache:profile"
    
    # Create cache hit and miss events
    hit_event = create_cache_event(
        aggregate_id=cache_id,
        event_type=EventType.CACHE_HIT,
        cache_key="user:123:profile",
        operation="GET",
        hit=True
    )
    
    miss_event = create_cache_event(
        aggregate_id=cache_id,
        event_type=EventType.CACHE_MISS,
        cache_key="user:456:profile",
        operation="GET",
        hit=False
    )
    
    store.append(hit_event)
    store.append(miss_event)
    
    state = processor.replay_events(cache_id)
    
    assert state["cache_stats"]["hits"] == 1
    assert state["cache_stats"]["misses"] == 1


def test_event_processor_aggregate_stats():
    """Test aggregating statistics across all events."""
    store = EventStore()
    store.clear()
    
    processor = EventProcessor(store)
    
    # Create different types of events
    events = [
        create_trade_event(
            aggregate_id="trade:1",
            event_type=EventType.TRADE_CREATED,
            symbol="BTC/USD",
            price=45000,
            quantity=1,
            side="BUY",
            status="CREATED"
        ),
        create_cache_event(
            aggregate_id="cache:1",
            event_type=EventType.CACHE_HIT,
            cache_key="key1",
            operation="GET"
        ),
        create_system_event(
            event_type=EventType.SYSTEM_STARTUP,
            level="INFO",
            message="Started",
            component="CORE"
        )
    ]
    
    for event in events:
        store.append(event)
    
    stats = processor.get_aggregate_stats()
    
    assert stats["total_events"] == 3
    assert EventType.TRADE_CREATED in stats["events_by_type"]
    assert EventType.CACHE_HIT in stats["events_by_type"]


def test_event_processor_timeline():
    """Test building event timeline."""
    store = EventStore()
    store.clear()
    
    processor = EventProcessor(store)
    trade_id = "trade:666"
    
    events = [
        create_trade_event(
            aggregate_id=trade_id,
            event_type=EventType.TRADE_CREATED,
            symbol="BTC/USD",
            price=45000,
            quantity=1,
            side="BUY",
            status="CREATED"
        ),
        create_trade_event(
            aggregate_id=trade_id,
            event_type=EventType.TRADE_EXECUTED,
            symbol="BTC/USD",
            price=45100,
            quantity=1,
            side="BUY",
            status="EXECUTED"
        )
    ]
    
    for event in events:
        store.append(event)
    
    timeline = processor.get_event_timeline(trade_id)
    
    assert len(timeline) == 2
    assert timeline[0]["event_type"] == EventType.TRADE_CREATED
    assert timeline[1]["event_type"] == EventType.TRADE_EXECUTED


def test_event_processor_projection():
    """Test getting materialized view of trade."""
    store = EventStore()
    store.clear()
    
    processor = EventProcessor(store)
    
    trade_event = create_trade_event(
        aggregate_id="trade:777",
        event_type=EventType.TRADE_CREATED,
        symbol="BTC/USD",
        price=45000,
        quantity=1,
        side="BUY",
        status="CREATED"
    )
    
    store.append(trade_event)
    projection = processor.get_trade_projection("777")
    
    assert projection["symbol"] == "BTC/USD"
    assert projection["aggregate_id"] == "trade:777"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
