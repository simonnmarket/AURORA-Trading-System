# Dependencies for AURORA API
"""
Dependency injection for database, cache, and event store.
FastAPI dependency functions for request handlers.
"""

from sqlalchemy.orm import Session
from src.database.config import SessionLocal
from src.cache.redis_client import redis_client
from src.events.event_store import event_store, EventStore
from src.events.event_processor import EventProcessor


def get_db() -> Session:
    """
    Get database session for request.
    
    Yields:
        SQLAlchemy Session connected to PostgreSQL
    
    Usage:
        @router.get("/trades")
        async def get_trades(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    """
    Get Redis cache client for request.
    
    Returns:
        RedisClient instance or None if unavailable
    
    Usage:
        @router.post("/trades")
        async def create_trade(cache = Depends(get_cache)):
            cache.set("key", value)
    """
    return redis_client


def get_event_store() -> EventStore:
    """
    Get event store instance for request.
    
    Returns:
        EventStore instance connected to PostgreSQL
    
    Usage:
        @router.get("/events")
        async def get_events(event_store = Depends(get_event_store)):
            events = event_store.get_all_events()
    """
    return event_store


def get_processor() -> EventProcessor:
    """
    Get event processor for state reconstruction.
    
    Returns:
        EventProcessor instance
    
    Usage:
        @router.get("/events/replay/{aggregate_id}")
        async def replay(processor = Depends(get_processor)):
            state = processor.replay_events(aggregate_id)
    """
    return EventProcessor(event_store)
