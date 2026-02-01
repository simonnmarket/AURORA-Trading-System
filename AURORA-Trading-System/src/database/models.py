# SQLAlchemy ORM Models for AURORA Trading System
"""
Database models for AURORA Trading System.
Defines data structures for trades, orders, and market data.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from .config import Base


class Trade(Base):
    """Trade model representing a single trade transaction.
    
    Attributes:
        id: Primary key
        symbol: Trading pair symbol (e.g., BTC/USD)
        price: Trade price in USD
        quantity: Trade quantity in base asset
        trade_type: BUY or SELL
        timestamp: Trade execution timestamp
        status: Trade status (EXECUTED, PENDING, CANCELLED)
    """
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    trade_type = Column(String(10), nullable=False)  # BUY or SELL
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(20), default="EXECUTED", nullable=False)
    
    def __repr__(self):
        """String representation of Trade."""
        return (
            f"<Trade(id={self.id}, symbol={self.symbol}, "
            f"price={self.price}, qty={self.quantity}, "
            f"type={self.trade_type}, status={self.status})>"
        )


class Order(Base):
    """Order model representing a pending or executed order.
    
    Attributes:
        id: Primary key
        symbol: Trading pair symbol
        order_type: MARKET or LIMIT
        side: BUY or SELL
        price: Order price (None for MARKET orders)
        quantity: Order quantity
        status: Order status (PENDING, FILLED, CANCELLED)
        created_at: Order creation timestamp
        updated_at: Order last update timestamp
    """
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False)
    order_type = Column(String(10), nullable=False)  # MARKET or LIMIT
    side = Column(String(10), nullable=False)  # BUY or SELL
    price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        """String representation of Order."""
        return (
            f"<Order(id={self.id}, symbol={self.symbol}, "
            f"type={self.order_type}, side={self.side}, "
            f"status={self.status})>"
        )


class MarketData(Base):
    """Market data model for storing OHLCV data.
    
    Attributes:
        id: Primary key
        symbol: Trading pair symbol
        open: Opening price
        high: Highest price in period
        low: Lowest price in period
        close: Closing price
        volume: Trading volume
        timestamp: Data timestamp
    """
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    
    def __repr__(self):
        """String representation of MarketData."""
        return (
            f"<MarketData(symbol={self.symbol}, "
            f"close={self.close}, volume={self.volume}, "
            f"timestamp={self.timestamp})>"
        )
