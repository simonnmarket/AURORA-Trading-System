# Pydantic Schemas for AURORA API
"""
Request/Response DTOs with validation.
Uses Pydantic for automatic validation and OpenAPI documentation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime


# ============================================================================
# TRADE SCHEMAS
# ============================================================================

class TradeCreate(BaseModel):
    """Request body for creating a new trade."""
    
    symbol: str = Field(..., min_length=1, max_length=20, description="Trading pair (e.g., BTC/USD)")
    price: float = Field(..., gt=0, description="Trade price")
    quantity: float = Field(..., gt=0, description="Trade quantity")
    side: str = Field(..., regex="^(BUY|SELL)$", description="BUY or SELL")
    
    @validator('symbol')
    def symbol_uppercase(cls, v):
        """Convert symbol to uppercase."""
        return v.upper()
    
    class Config:
        example = {
            "symbol": "BTC/USD",
            "price": 45000.00,
            "quantity": 1.5,
            "side": "BUY"
        }


class TradeResponse(BaseModel):
    """Response for trade operations."""
    
    id: int
    symbol: str
    price: float
    quantity: float
    side: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "symbol": "BTC/USD",
            "price": 45000.00,
            "quantity": 1.5,
            "side": "BUY",
            "created_at": "2025-02-02T14:30:00Z",
            "updated_at": None
        }


# ============================================================================
# EVENT SCHEMAS
# ============================================================================

class EventResponse(BaseModel):
    """Response for event queries."""
    
    event_id: str
    event_type: str
    aggregate_id: str
    timestamp: datetime
    data: Dict[str, Any]
    version: int
    user_id: Optional[str] = None
    
    @classmethod
    def from_event(cls, event):
        """Convert Event model to Response."""
        return cls(
            event_id=event.event_id,
            event_type=event.event_type,
            aggregate_id=event.aggregate_id,
            timestamp=event.timestamp,
            data=event.data,
            version=event.version,
            user_id=event.user_id
        )
    
    class Config:
        example = {
            "event_id": "550e8400-e29b-41d4-a716-446655440000",
            "event_type": "TRADE_CREATED",
            "aggregate_id": "trade:1",
            "timestamp": "2025-02-02T14:30:00Z",
            "data": {
                "symbol": "BTC/USD",
                "price": 45000.00,
                "quantity": 1.5,
                "side": "BUY",
                "status": "created"
            },
            "version": 1,
            "user_id": None
        }


# ============================================================================
# HEALTH SCHEMAS
# ============================================================================

class HealthResponse(BaseModel):
    """Response for health check endpoint."""
    
    status: str = Field(..., regex="^(healthy|degraded|unhealthy)$")
    database_ok: bool
    cache_ok: bool
    events_ok: bool
    event_count: int
    timestamp: datetime
    
    class Config:
        example = {
            "status": "healthy",
            "database_ok": True,
            "cache_ok": True,
            "events_ok": True,
            "event_count": 42,
            "timestamp": "2025-02-02T14:30:00Z"
        }


# ============================================================================
# ERROR SCHEMAS
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    timestamp: datetime
    request_id: Optional[str] = None
    
    class Config:
        example = {
            "error": "Validation Error",
            "detail": "Price must be greater than 0",
            "timestamp": "2025-02-02T14:30:00Z",
            "request_id": "req-12345"
        }
