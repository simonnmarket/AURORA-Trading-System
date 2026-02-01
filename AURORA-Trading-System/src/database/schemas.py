# Pydantic Schemas for API Validation
"""
Request/response schemas for AURORA Trading API.
Uses Pydantic for automatic validation and OpenAPI documentation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ============================================================================
# Trade Schemas
# ============================================================================

class TradeCreate(BaseModel):
    """Schema for creating a new trade.
    
    Attributes:
        symbol: Trading pair symbol (e.g., BTC/USD)
        price: Trade price in USD
        quantity: Trade quantity
        trade_type: BUY or SELL
    """
    symbol: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    trade_type: str = Field(..., regex="^(BUY|SELL)$")


class Trade(TradeCreate):
    """Complete trade schema with database fields.
    
    Includes all TradeCreate fields plus:
        id: Database primary key
        timestamp: Trade execution time
        status: Trade status
    """
    id: int
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True


# ============================================================================
# Order Schemas
# ============================================================================

class OrderCreate(BaseModel):
    """Schema for creating a new order.
    
    Attributes:
        symbol: Trading pair symbol
        order_type: MARKET or LIMIT
        side: BUY or SELL
        price: Order price (None for MARKET orders)
        quantity: Order quantity
    """
    symbol: str = Field(..., min_length=1, max_length=50)
    order_type: str = Field(..., regex="^(MARKET|LIMIT)$")
    side: str = Field(..., regex="^(BUY|SELL)$")
    price: Optional[float] = Field(None, gt=0)
    quantity: float = Field(..., gt=0)


class Order(OrderCreate):
    """Complete order schema with database fields.
    
    Includes all OrderCreate fields plus:
        id: Database primary key
        status: Order status
        created_at: Order creation timestamp
        updated_at: Order last update timestamp
    """
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# Market Data Schemas
# ============================================================================

class MarketDataCreate(BaseModel):
    """Schema for market data (OHLCV).
    
    Attributes:
        symbol: Trading pair symbol
        open: Opening price
        high: Highest price
        low: Lowest price
        close: Closing price
        volume: Trading volume
        timestamp: Data timestamp
    """
    symbol: str = Field(..., min_length=1, max_length=50)
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)
    timestamp: datetime


class MarketData(MarketDataCreate):
    """Complete market data schema with database fields.
    
    Includes all MarketDataCreate fields plus:
        id: Database primary key
    """
    id: int

    class Config:
        orm_mode = True


# ============================================================================
# Health Check Schemas
# ============================================================================

class HealthCheck(BaseModel):
    """Health check response schema.
    
    Attributes:
        status: Service status (ok, degraded, down)
        service: Service name
        database: Database connection status
        version: API version
    """
    status: str
    service: str
    database: str
    version: str
