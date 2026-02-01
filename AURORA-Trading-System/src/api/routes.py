# API Routes for AURORA Trading System
"""
REST endpoints integrating Cache, Database, and Event Store.
Provides unified interface for trade operations and event queries.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.config import SessionLocal
from src.database.models import Trade
from src.cache.decorators import cache
from src.events.event_store import event_store
from src.events.event_processor import EventProcessor
from src.events.event_models import create_trade_event, EventType

from .dependencies import get_db, get_cache, get_event_store, get_processor
from .schemas import TradeCreate, TradeResponse, EventResponse, HealthResponse

router = APIRouter(prefix="/api/v1", tags=["AURORA API"])


# ============================================================================
# TRADE ENDPOINTS - Database + Cache Integration
# ============================================================================

@router.get("/trades", response_model=List[TradeResponse])
@cache(ttl=3600)
async def get_trades(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
) -> List[TradeResponse]:
    """
    Get all trades from database with caching.
    
    - **skip**: Skip first N records
    - **limit**: Limit results (max 100)
    - Results cached for 1 hour
    
    Returns:
        List of trades with full details
    """
    trades = db.query(Trade).offset(skip).limit(limit).all()
    return [TradeResponse.from_orm(trade) for trade in trades]


@router.get("/trades/{trade_id}", response_model=TradeResponse)
@cache(ttl=3600)
async def get_trade(
    trade_id: int,
    db: Session = Depends(get_db)
) -> TradeResponse:
    """
    Get specific trade by ID with caching.
    
    - **trade_id**: Trade identifier
    
    Returns:
        Trade details or 404 if not found
    """
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return TradeResponse.from_orm(trade)


@router.post("/trades", response_model=TradeResponse, status_code=201)
async def create_trade(
    trade: TradeCreate,
    db: Session = Depends(get_db),
    event_store_dep = Depends(get_event_store),
    processor: EventProcessor = Depends(get_processor)
) -> TradeResponse:
    """
    Create new trade with database persistence and event logging.
    
    Workflow:
    1. Validate trade data (decorator @validate_trade)
    2. Persist to PostgreSQL database
    3. Create TRADE_CREATED event in Event Store
    4. Invalidate cache pattern for /trades
    5. Return created trade
    
    Request body:
        {
            "symbol": "BTC/USD",
            "price": 45000.00,
            "quantity": 1.5,
            "side": "BUY"
        }
    
    Returns:
        201: Created trade with ID and timestamp
        400: Invalid trade data
    """
    # Create database record
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    
    # Create event
    event = create_trade_event(
        aggregate_id=f"trade:{db_trade.id}",
        event_type=EventType.TRADE_CREATED,
        symbol=trade.symbol,
        price=trade.price,
        quantity=trade.quantity,
        side=trade.side,
        status="created"
    )
    
    # Append to event store
    event_store.append(event)
    
    # Invalidate cache
    from src.cache.cache_manager import CacheManager
    CacheManager.invalidate_pattern("cache:get_trades:*")
    
    return TradeResponse.from_orm(db_trade)


@router.put("/trades/{trade_id}", response_model=TradeResponse)
async def update_trade(
    trade_id: int,
    trade_update: TradeCreate,
    db: Session = Depends(get_db),
    event_store_dep = Depends(get_event_store)
) -> TradeResponse:
    """
    Update trade and log TRADE_UPDATED event.
    
    Returns:
        Updated trade or 404
    """
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    # Update fields
    for key, value in trade_update.dict().items():
        setattr(db_trade, key, value)
    
    db.commit()
    db.refresh(db_trade)
    
    # Log event
    event = create_trade_event(
        aggregate_id=f"trade:{db_trade.id}",
        event_type=EventType.TRADE_EXECUTED,
        symbol=db_trade.symbol,
        price=db_trade.price,
        quantity=db_trade.quantity,
        side=db_trade.side,
        status="updated"
    )
    event_store.append(event)
    
    # Invalidate cache
    from src.cache.cache_manager import CacheManager
    CacheManager.invalidate_pattern("cache:*trade*")
    
    return TradeResponse.from_orm(db_trade)


# ============================================================================
# EVENT ENDPOINTS - Event Store Integration
# ============================================================================

@router.get("/events", response_model=List[EventResponse])
async def get_events(
    event_type: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    event_store_dep = Depends(get_event_store)
) -> List[EventResponse]:
    """
    Query events from Event Store with optional filtering.
    
    - **event_type**: Filter by event type (optional)
    - **limit**: Maximum number of events (default 100, max 1000)
    
    Returns:
        List of events in chronological order
    """
    if event_type:
        events = event_store.get_events_by_type(event_type)
    else:
        events = event_store.get_all_events(limit=limit)
    
    return [EventResponse.from_event(event) for event in events]


@router.get("/events/stream/{aggregate_id}", response_model=List[EventResponse])
async def get_event_stream(
    aggregate_id: str,
    event_store_dep = Depends(get_event_store)
) -> List[EventResponse]:
    """
    Get event stream for specific aggregate (trade, cache, etc).
    
    - **aggregate_id**: Aggregate identifier (e.g., "trade:123")
    
    Returns:
        All events for this aggregate in order
    """
    events = event_store.get_events_by_aggregate(aggregate_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found")
    return [EventResponse.from_event(event) for event in events]


@router.get("/events/replay/{aggregate_id}")
async def replay_events(
    aggregate_id: str,
    processor: EventProcessor = Depends(get_processor)
):
    """
    Replay all events for aggregate to get current state.
    
    - **aggregate_id**: Aggregate to replay
    
    Returns:
        State after replaying all events
    """
    state = processor.replay_events(aggregate_id)
    if not state.get('event_count'):
        raise HTTPException(status_code=404, detail="No events to replay")
    return state


@router.get("/events/stats")
async def get_event_stats(
    processor: EventProcessor = Depends(get_processor)
):
    """
    Get aggregate statistics across all events.
    
    Returns:
        Total count, breakdown by type and aggregate, time range
    """
    return processor.get_aggregate_stats()


# ============================================================================
# HEALTH/STATUS ENDPOINTS
# ============================================================================

@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: Session = Depends(get_db),
    cache = Depends(get_cache),
    event_store_dep = Depends(get_event_store)
) -> HealthResponse:
    """
    Check health of all integrated components.
    
    Returns:
        Status of database, cache, and event store
    """
    try:
        # Check database
        db.execute("SELECT 1")
        db_ok = True
    except:
        db_ok = False
    
    try:
        # Check cache
        cache.ping()
        cache_ok = True
    except:
        cache_ok = False
    
    try:
        # Check event store
        event_count = event_store.get_event_count()
        events_ok = True
    except:
        events_ok = False
    
    status = "healthy" if all([db_ok, cache_ok, events_ok]) else "degraded"
    
    return HealthResponse(
        status=status,
        database_ok=db_ok,
        cache_ok=cache_ok,
        events_ok=events_ok,
        event_count=event_count,
        timestamp=datetime.utcnow()
    )


@router.get("/api/version")
async def version():
    """API version info."""
    return {
        "version": "1.0.0",
        "st_id": "AURORA-ST-20260202-004",
        "components": ["database", "cache", "events"]
    }
