# Event Processor for AURORA Trading System
"""
Event Processor for replaying events and building materialized views.
Handles event sourcing replay logic and state reconstruction.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from collections import defaultdict

from .event_models import Event, EventType, TradeEvent, CacheEvent, SystemEvent
from .event_store import EventStore


class EventProcessor:
    """Process events for state reconstruction and materialization.
    
    Implements event sourcing pattern with replay capability.
    Can reconstruct state at any point in time by replaying events.
    """
    
    def __init__(self, event_store: EventStore):
        """Initialize EventProcessor with an event store.
        
        Args:
            event_store: EventStore instance for retrieving events
        """
        self.event_store = event_store
        self.event_handlers: Dict[str, Callable] = {
            EventType.TRADE_CREATED: self._handle_trade_created,
            EventType.TRADE_EXECUTED: self._handle_trade_executed,
            EventType.TRADE_CANCELLED: self._handle_trade_cancelled,
            EventType.CACHE_HIT: self._handle_cache_hit,
            EventType.CACHE_MISS: self._handle_cache_miss,
            EventType.CACHE_INVALIDATED: self._handle_cache_invalidated,
        }
    
    def replay_events(self, aggregate_id: str) -> Dict[str, Any]:
        """Replay all events for an aggregate to reconstruct current state.
        
        Args:
            aggregate_id: Aggregate ID to replay events for
        
        Returns:
            Current state after replaying all events
        """
        events = self.event_store.get_events_by_aggregate(aggregate_id)
        
        state = {
            'aggregate_id': aggregate_id,
            'version': 0,
            'status': 'initialized',
            'created_at': datetime.utcnow().isoformat(),
            'event_count': 0,
            'events': []
        }
        
        for event in events:
            state = self._apply_event(state, event)
        
        print(f"✅ Replayed {len(events)} events for {aggregate_id}")
        return state
    
    def replay_events_until(
        self,
        aggregate_id: str,
        until_timestamp: datetime
    ) -> Dict[str, Any]:
        """Replay events up to a specific point in time.
        
        Useful for temporal queries and auditing.
        
        Args:
            aggregate_id: Aggregate ID
            until_timestamp: Timestamp to replay until
        
        Returns:
            State at that point in time
        """
        events = self.event_store.get_events_by_aggregate(
            aggregate_id,
            since=None
        )
        
        # Filter events up to timestamp
        events = [e for e in events if e.timestamp <= until_timestamp]
        
        state = {
            'aggregate_id': aggregate_id,
            'version': 0,
            'status': 'initialized',
            'as_of': until_timestamp.isoformat(),
            'event_count': 0,
            'events': []
        }
        
        for event in events:
            state = self._apply_event(state, event)
        
        return state
    
    def _apply_event(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Apply a single event to state.
        
        Dispatches to specific handlers based on event type.
        
        Args:
            state: Current state
            event: Event to apply
        
        Returns:
            Updated state
        """
        handler = self.event_handlers.get(event.event_type)
        
        if handler:
            state = handler(state, event)
        else:
            # Default handler for unknown event types
            state = self._handle_unknown_event(state, event)
        
        # Update metadata
        state['version'] += 1
        state['event_count'] += 1
        state['events'].append(event.to_dict())
        state['last_updated'] = event.timestamp.isoformat()
        
        return state
    
    # ========================================================================
    # Event Handlers
    # ========================================================================
    
    def _handle_trade_created(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle TRADE_CREATED event."""
        data = event.data
        state['symbol'] = data.get('symbol')
        state['price'] = data.get('price')
        state['quantity'] = data.get('quantity')
        state['side'] = data.get('side')
        state['status'] = 'created'
        return state
    
    def _handle_trade_executed(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle TRADE_EXECUTED event."""
        data = event.data
        state['status'] = 'executed'
        state['executed_price'] = data.get('price', state.get('price'))
        state['executed_quantity'] = data.get('quantity', state.get('quantity'))
        state['executed_at'] = event.timestamp.isoformat()
        return state
    
    def _handle_trade_cancelled(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle TRADE_CANCELLED event."""
        data = event.data
        state['status'] = 'cancelled'
        state['cancelled_reason'] = data.get('reason')
        state['cancelled_at'] = event.timestamp.isoformat()
        return state
    
    def _handle_cache_hit(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle CACHE_HIT event."""
        data = event.data
        if 'cache_stats' not in state:
            state['cache_stats'] = {'hits': 0, 'misses': 0}
        state['cache_stats']['hits'] += 1
        state['last_cache_key'] = data.get('cache_key')
        return state
    
    def _handle_cache_miss(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle CACHE_MISS event."""
        data = event.data
        if 'cache_stats' not in state:
            state['cache_stats'] = {'hits': 0, 'misses': 0}
        state['cache_stats']['misses'] += 1
        state['last_cache_key'] = data.get('cache_key')
        return state
    
    def _handle_cache_invalidated(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle CACHE_INVALIDATED event."""
        data = event.data
        if 'invalidations' not in state:
            state['invalidations'] = []
        state['invalidations'].append({
            'cache_key': data.get('cache_key'),
            'timestamp': event.timestamp.isoformat()
        })
        return state
    
    def _handle_unknown_event(self, state: Dict[str, Any], event: Event) -> Dict[str, Any]:
        """Handle unknown event types (fallback handler)."""
        if 'unknown_events' not in state:
            state['unknown_events'] = []
        state['unknown_events'].append(event.to_dict())
        return state
    
    # ========================================================================
    # Materialized Views / Projections
    # ========================================================================
    
    def get_trade_projection(self, trade_id: str) -> Dict[str, Any]:
        """Get materialized view of a trade's current state.
        
        Args:
            trade_id: Trade ID
        
        Returns:
            Trade state
        """
        return self.replay_events(f"trade:{trade_id}")
    
    def get_cache_projection(self, cache_key: str) -> Dict[str, Any]:
        """Get materialized view of cache activity.
        
        Args:
            cache_key: Cache key
        
        Returns:
            Cache state and statistics
        """
        return self.replay_events(f"cache:{cache_key}")
    
    def get_aggregate_stats(self) -> Dict[str, Any]:
        """Get statistics across all aggregates.
        
        Returns:
            Dictionary with aggregate statistics
        """
        all_events = self.event_store.get_all_events()
        
        stats = {
            'total_events': len(all_events),
            'events_by_type': defaultdict(int),
            'events_by_aggregate': defaultdict(int),
            'first_event_time': None,
            'last_event_time': None,
        }
        
        if all_events:
            stats['first_event_time'] = all_events[0].timestamp.isoformat()
            stats['last_event_time'] = all_events[-1].timestamp.isoformat()
        
        for event in all_events:
            stats['events_by_type'][event.event_type] += 1
            stats['events_by_aggregate'][event.aggregate_id] += 1
        
        # Convert defaultdicts to regular dicts
        stats['events_by_type'] = dict(stats['events_by_type'])
        stats['events_by_aggregate'] = dict(stats['events_by_aggregate'])
        
        return stats
    
    def get_event_timeline(self, aggregate_id: str) -> List[Dict[str, Any]]:
        """Get timeline of all events for an aggregate.
        
        Args:
            aggregate_id: Aggregate ID
        
        Returns:
            List of event metadata in chronological order
        """
        events = self.event_store.get_events_by_aggregate(aggregate_id)
        
        timeline = []
        for event in events:
            timeline.append({
                'event_id': event.event_id,
                'event_type': event.event_type,
                'timestamp': event.timestamp.isoformat(),
                'version': event.version
            })
        
        return timeline
