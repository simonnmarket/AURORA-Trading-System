# Event Store for AURORA Trading System
"""
Event Store implementation using PostgreSQL for persistence.
Stores all domain events with immutability and append-only semantics.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime, Integer, Index
from sqlalchemy.exc import IntegrityError

from src.database.config import Base, SessionLocal
from .event_models import Event, EventType
import json


class EventRecord(Base):
    """SQLAlchemy model for storing events in PostgreSQL.
    
    Represents a single event persisted in the database.
    This is the append-only log of all events in the system.
    """
    __tablename__ = "events"
    
    # Primary key
    event_id = Column(String(36), primary_key=True, unique=True, nullable=False)
    
    # Event metadata
    event_type = Column(String(100), nullable=False, index=True)
    aggregate_id = Column(String(100), nullable=False, index=True)
    
    # Temporal
    timestamp = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    
    # Event data
    data = Column(JSON, nullable=False)
    
    # Versioning
    version = Column(Integer, nullable=False, default=1)
    
    # User tracking
    user_id = Column(String(100), nullable=True)
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_aggregate_timestamp', 'aggregate_id', 'timestamp'),
        Index('idx_event_type_timestamp', 'event_type', 'timestamp'),
    )
    
    def to_event(self) -> Event:
        """Convert database record to Event object.
        
        Returns:
            Event instance with all data from record
        """
        return Event(
            event_id=self.event_id,
            event_type=self.event_type,
            aggregate_id=self.aggregate_id,
            timestamp=self.timestamp,
            data=self.data,
            version=self.version,
            user_id=self.user_id
        )


class EventStore:
    """Event Store for persisting and retrieving events.
    
    Implements append-only event store pattern with PostgreSQL backend.
    All events are immutable once appended.
    """
    
    def __init__(self):
        """Initialize EventStore."""
        # Create tables if they don't exist
        Base.metadata.create_all(bind=SessionLocal().get_bind())
    
    def append(self, event: Event) -> bool:
        """Append a single event to the store.
        
        Args:
            event: Event to append
        
        Returns:
            bool: True if successful, False otherwise
        
        Raises:
            IntegrityError: If event_id already exists
        """
        try:
            session = SessionLocal()
            
            record = EventRecord(
                event_id=event.event_id,
                event_type=event.event_type,
                aggregate_id=event.aggregate_id,
                timestamp=event.timestamp,
                data=event.data,
                version=event.version,
                user_id=event.user_id
            )
            
            session.add(record)
            session.commit()
            session.close()
            
            print(f"✅ Event appended: {event.event_type} (ID: {event.event_id})")
            return True
            
        except IntegrityError as e:
            print(f"❌ Event already exists: {event.event_id}")
            session.rollback()
            session.close()
            return False
        except Exception as e:
            print(f"❌ Error appending event: {e}")
            session.rollback()
            session.close()
            return False
    
    def append_many(self, events: List[Event]) -> int:
        """Append multiple events to the store.
        
        Args:
            events: List of events to append
        
        Returns:
            int: Number of successfully appended events
        """
        appended = 0
        for event in events:
            if self.append(event):
                appended += 1
        return appended
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Retrieve a single event by ID.
        
        Args:
            event_id: ID of event to retrieve
        
        Returns:
            Event if found, None otherwise
        """
        try:
            session = SessionLocal()
            
            record = session.query(EventRecord)\
                .filter(EventRecord.event_id == event_id)\
                .first()
            
            session.close()
            
            return record.to_event() if record else None
            
        except Exception as e:
            print(f"❌ Error retrieving event: {e}")
            return None
    
    def get_events_by_aggregate(
        self,
        aggregate_id: str,
        since: Optional[datetime] = None
    ) -> List[Event]:
        """Retrieve all events for an aggregate (stream).
        
        Args:
            aggregate_id: Aggregate ID to retrieve events for
            since: Optional start datetime (events after this time)
        
        Returns:
            List of events in chronological order
        """
        try:
            session = SessionLocal()
            
            query = session.query(EventRecord)\
                .filter(EventRecord.aggregate_id == aggregate_id)
            
            if since:
                query = query.filter(EventRecord.timestamp >= since)
            
            records = query.order_by(EventRecord.timestamp).all()
            session.close()
            
            return [record.to_event() for record in records]
            
        except Exception as e:
            print(f"❌ Error retrieving events: {e}")
            return []
    
    def get_events_by_type(self, event_type: str) -> List[Event]:
        """Retrieve all events of a specific type.
        
        Args:
            event_type: Type of events to retrieve
        
        Returns:
            List of events of the specified type
        """
        try:
            session = SessionLocal()
            
            records = session.query(EventRecord)\
                .filter(EventRecord.event_type == event_type)\
                .order_by(EventRecord.timestamp)\
                .all()
            
            session.close()
            
            return [record.to_event() for record in records]
            
        except Exception as e:
            print(f"❌ Error retrieving events by type: {e}")
            return []
    
    def get_all_events(self, limit: Optional[int] = None) -> List[Event]:
        """Retrieve all events in the store.
        
        Args:
            limit: Optional limit on number of events to return
        
        Returns:
            List of all events in chronological order
        """
        try:
            session = SessionLocal()
            
            query = session.query(EventRecord)\
                .order_by(EventRecord.timestamp)
            
            if limit:
                query = query.limit(limit)
            
            records = query.all()
            session.close()
            
            return [record.to_event() for record in records]
            
        except Exception as e:
            print(f"❌ Error retrieving all events: {e}")
            return []
    
    def get_event_count(self) -> int:
        """Get total number of events in store.
        
        Returns:
            int: Total event count
        """
        try:
            session = SessionLocal()
            count = session.query(EventRecord).count()
            session.close()
            return count
        except Exception as e:
            print(f"❌ Error counting events: {e}")
            return 0
    
    def clear(self) -> bool:
        """Clear all events from the store (DANGEROUS).
        
        WARNING: This deletes all events. Use only for testing!
        
        Returns:
            bool: True if successful
        """
        try:
            session = SessionLocal()
            session.query(EventRecord).delete()
            session.commit()
            session.close()
            print("⚠️  All events cleared!")
            return True
        except Exception as e:
            print(f"❌ Error clearing events: {e}")
            return False


# Global instance
event_store = EventStore()
