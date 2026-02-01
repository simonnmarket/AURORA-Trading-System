"""
Unit tests for AURORA database layer.
Tests PostgreSQL connection, ORM models, and Pydantic schemas.
"""

import pytest
from src.database.models import Trade, Order, MarketData
from src.database.schemas import (
    TradeCreate, Trade as TradeSchema,
    OrderCreate, Order as OrderSchema,
    MarketDataCreate, MarketData as MarketDataSchema
)
from datetime import datetime


# ============================================================================
# Trade Model Tests
# ============================================================================

def test_trade_model_creation():
    """Test creating Trade model instance."""
    trade = Trade(
        symbol="BTC/USD",
        price=45000.0,
        quantity=1.5,
        trade_type="BUY",
        status="EXECUTED"
    )
    assert trade.symbol == "BTC/USD"
    assert trade.price == 45000.0
    assert trade.quantity == 1.5
    assert trade.trade_type == "BUY"
    assert trade.status == "EXECUTED"


def test_trade_model_repr():
    """Test Trade __repr__ method."""
    trade = Trade(
        symbol="ETH/USD",
        price=2500.0,
        quantity=10.0,
        trade_type="SELL",
        status="EXECUTED"
    )
    repr_str = repr(trade)
    assert "ETH/USD" in repr_str
    assert "2500.0" in repr_str


# ============================================================================
# Order Model Tests
# ============================================================================

def test_order_model_creation_market():
    """Test creating MARKET Order model instance."""
    order = Order(
        symbol="BTC/USD",
        order_type="MARKET",
        side="BUY",
        price=None,
        quantity=0.5,
        status="PENDING"
    )
    assert order.symbol == "BTC/USD"
    assert order.order_type == "MARKET"
    assert order.side == "BUY"
    assert order.price is None
    assert order.quantity == 0.5


def test_order_model_creation_limit():
    """Test creating LIMIT Order model instance."""
    order = Order(
        symbol="ETH/USD",
        order_type="LIMIT",
        side="SELL",
        price=2450.0,
        quantity=5.0,
        status="PENDING"
    )
    assert order.order_type == "LIMIT"
    assert order.price == 2450.0


# ============================================================================
# MarketData Model Tests
# ============================================================================

def test_market_data_model_creation():
    """Test creating MarketData model instance."""
    md = MarketData(
        symbol="BTC/USD",
        open=44000.0,
        high=46000.0,
        low=43500.0,
        close=45500.0,
        volume=1000.0,
        timestamp=datetime.now()
    )
    assert md.symbol == "BTC/USD"
    assert md.open == 44000.0
    assert md.high == 46000.0
    assert md.low == 43500.0
    assert md.close == 45500.0
    assert md.volume == 1000.0


# ============================================================================
# Trade Schema Tests
# ============================================================================

def test_trade_schema_creation():
    """Test creating valid TradeCreate schema."""
    trade_data = {
        "symbol": "BTC/USD",
        "price": 45000.0,
        "quantity": 1.0,
        "trade_type": "BUY"
    }
    trade = TradeCreate(**trade_data)
    assert trade.symbol == "BTC/USD"
    assert trade.price == 45000.0
    assert trade.trade_type == "BUY"


def test_trade_schema_invalid_price():
    """Test TradeCreate rejects negative price."""
    trade_data = {
        "symbol": "BTC/USD",
        "price": -100.0,  # Invalid: negative price
        "quantity": 1.0,
        "trade_type": "BUY"
    }
    with pytest.raises(ValueError):
        TradeCreate(**trade_data)


def test_trade_schema_invalid_type():
    """Test TradeCreate rejects invalid trade_type."""
    trade_data = {
        "symbol": "BTC/USD",
        "price": 45000.0,
        "quantity": 1.0,
        "trade_type": "INVALID"  # Invalid: must be BUY or SELL
    }
    with pytest.raises(ValueError):
        TradeCreate(**trade_data)


# ============================================================================
# Order Schema Tests
# ============================================================================

def test_order_create_market_schema():
    """Test creating MARKET OrderCreate schema."""
    order_data = {
        "symbol": "BTC/USD",
        "order_type": "MARKET",
        "side": "BUY",
        "price": None,
        "quantity": 0.5
    }
    order = OrderCreate(**order_data)
    assert order.order_type == "MARKET"
    assert order.price is None


def test_order_create_limit_schema():
    """Test creating LIMIT OrderCreate schema."""
    order_data = {
        "symbol": "ETH/USD",
        "order_type": "LIMIT",
        "side": "SELL",
        "price": 2450.0,
        "quantity": 5.0
    }
    order = OrderCreate(**order_data)
    assert order.order_type == "LIMIT"
    assert order.price == 2450.0


def test_order_schema_invalid_side():
    """Test OrderCreate rejects invalid side."""
    order_data = {
        "symbol": "BTC/USD",
        "order_type": "MARKET",
        "side": "INVALID",
        "price": None,
        "quantity": 0.5
    }
    with pytest.raises(ValueError):
        OrderCreate(**order_data)


# ============================================================================
# MarketData Schema Tests
# ============================================================================

def test_market_data_schema_creation():
    """Test creating valid MarketDataCreate schema."""
    now = datetime.now()
    data = {
        "symbol": "BTC/USD",
        "open": 44000.0,
        "high": 46000.0,
        "low": 43500.0,
        "close": 45500.0,
        "volume": 1000.0,
        "timestamp": now
    }
    md = MarketDataCreate(**data)
    assert md.symbol == "BTC/USD"
    assert md.close == 45500.0


def test_market_data_schema_invalid_prices():
    """Test MarketDataCreate rejects invalid prices."""
    now = datetime.now()
    data = {
        "symbol": "BTC/USD",
        "open": -1000.0,  # Invalid: negative
        "high": 46000.0,
        "low": 43500.0,
        "close": 45500.0,
        "volume": 1000.0,
        "timestamp": now
    }
    with pytest.raises(ValueError):
        MarketDataCreate(**data)


# ============================================================================
# ORM Mode Tests
# ============================================================================

def test_trade_schema_orm_mode():
    """Test Trade schema can be created from ORM model (orm_mode=True)."""
    trade_orm = Trade(
        id=1,
        symbol="BTC/USD",
        price=45000.0,
        quantity=1.0,
        trade_type="BUY",
        status="EXECUTED",
        timestamp=datetime.now()
    )
    trade_schema = TradeSchema.from_orm(trade_orm)
    assert trade_schema.id == 1
    assert trade_schema.symbol == "BTC/USD"


if __name__ == "__main__":
    # Run tests with pytest: pytest tests/test_database.py -v
    pytest.main([__file__, "-v"])
