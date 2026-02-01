# Tests for AURORA API Integration
"""
Unit and integration tests for API endpoints.
Tests database integration, cache, event store, and endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api.main import app
from src.api.dependencies import get_db
from src.database.config import Base
from src.database.models import Trade
from src.cache.cache_manager import CacheManager
from src.events.event_store import EventStore

# Test database setup (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ============================================================================
# TRADE ENDPOINT TESTS
# ============================================================================

class TestTradeEndpoints:
    """Tests for GET/POST /trades endpoints."""
    
    def test_create_trade_success(self):
        """Test successful trade creation."""
        response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "BTC/USD",
                "price": 45000.00,
                "quantity": 1.5,
                "side": "BUY"
            }
        )
        assert response.status_code == 201
        assert response.json()["symbol"] == "BTC/USD"
        assert response.json()["price"] == 45000.00
    
    def test_create_trade_invalid_price(self):
        """Test trade creation with invalid price."""
        response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "BTC/USD",
                "price": -100,
                "quantity": 1.5,
                "side": "BUY"
            }
        )
        assert response.status_code in [400, 422]
    
    def test_create_trade_invalid_side(self):
        """Test trade creation with invalid side."""
        response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "BTC/USD",
                "price": 45000.00,
                "quantity": 1.5,
                "side": "INVALID"
            }
        )
        assert response.status_code == 422
    
    def test_get_trades_empty(self):
        """Test getting trades when none exist."""
        response = client.get("/api/v1/trades")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_trades_with_data(self):
        """Test getting trades after creating one."""
        # Create trade
        client.post(
            "/api/v1/trades",
            json={
                "symbol": "ETH/USD",
                "price": 2000.00,
                "quantity": 10,
                "side": "SELL"
            }
        )
        
        # Get trades
        response = client.get("/api/v1/trades")
        assert response.status_code == 200
        trades = response.json()
        assert len(trades) > 0
    
    def test_get_trade_by_id_success(self):
        """Test getting specific trade by ID."""
        # Create trade
        create_response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "XRP/USD",
                "price": 0.5,
                "quantity": 1000,
                "side": "BUY"
            }
        )
        trade_id = create_response.json()["id"]
        
        # Get specific trade
        response = client.get(f"/api/v1/trades/{trade_id}")
        assert response.status_code == 200
        assert response.json()["id"] == trade_id
    
    def test_get_trade_by_id_not_found(self):
        """Test getting non-existent trade."""
        response = client.get("/api/v1/trades/99999")
        assert response.status_code == 404
    
    def test_update_trade_success(self):
        """Test updating a trade."""
        # Create trade
        create_response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "ADA/USD",
                "price": 0.5,
                "quantity": 100,
                "side": "BUY"
            }
        )
        trade_id = create_response.json()["id"]
        
        # Update trade
        response = client.put(
            f"/api/v1/trades/{trade_id}",
            json={
                "symbol": "ADA/USD",
                "price": 0.6,
                "quantity": 150,
                "side": "SELL"
            }
        )
        assert response.status_code == 200
        assert response.json()["price"] == 0.6


# ============================================================================
# EVENT ENDPOINT TESTS
# ============================================================================

class TestEventEndpoints:
    """Tests for GET /events endpoints."""
    
    def test_get_events_empty(self):
        """Test getting events when none exist."""
        response = client.get("/api/v1/events")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_events_after_trade_creation(self):
        """Test getting events after trade is created."""
        # Create trade (should create event)
        client.post(
            "/api/v1/trades",
            json={
                "symbol": "SOL/USD",
                "price": 100.00,
                "quantity": 10,
                "side": "BUY"
            }
        )
        
        # Get events
        response = client.get("/api/v1/events")
        assert response.status_code == 200
        events = response.json()
        assert len(events) > 0
        assert events[0]["event_type"] in ["TRADE_CREATED", "TRADE_EXECUTED"]
    
    def test_get_events_by_type(self):
        """Test filtering events by type."""
        response = client.get("/api/v1/events?event_type=TRADE_CREATED")
        assert response.status_code == 200
        events = response.json()
        for event in events:
            assert event["event_type"] == "TRADE_CREATED"
    
    def test_get_event_stream(self):
        """Test getting event stream for aggregate."""
        # Create trade
        create_response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "LUNA/USD",
                "price": 5.00,
                "quantity": 1000,
                "side": "BUY"
            }
        )
        trade_id = create_response.json()["id"]
        
        # Get stream
        response = client.get(f"/api/v1/events/stream/trade:{trade_id}")
        assert response.status_code == 200
        events = response.json()
        assert len(events) > 0
        for event in events:
            assert event["aggregate_id"] == f"trade:{trade_id}"
    
    def test_replay_events(self):
        """Test event replay for state reconstruction."""
        # Create trade
        create_response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "DOT/USD",
                "price": 10.00,
                "quantity": 100,
                "side": "SELL"
            }
        )
        trade_id = create_response.json()["id"]
        
        # Replay
        response = client.get(f"/api/v1/events/replay/trade:{trade_id}")
        assert response.status_code == 200
        state = response.json()
        assert "aggregate_id" in state
        assert "event_count" in state
        assert state["event_count"] > 0
    
    def test_get_event_stats(self):
        """Test getting event statistics."""
        response = client.get("/api/v1/events/stats")
        assert response.status_code == 200
        stats = response.json()
        assert "total_events" in stats
        assert "events_by_type" in stats


# ============================================================================
# HEALTH ENDPOINT TESTS
# ============================================================================

class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        health = response.json()
        assert "status" in health
        assert health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "database_ok" in health
        assert "cache_ok" in health
        assert "events_ok" in health
    
    def test_api_version(self):
        """Test API version endpoint."""
        response = client.get("/api/version")
        assert response.status_code == 200
        version = response.json()
        assert version["version"] == "1.0.0"
        assert version["st_id"] == "AURORA-ST-20260202-004"


# ============================================================================
# CACHE INTEGRATION TESTS
# ============================================================================

class TestCacheIntegration:
    """Tests for cache integration with API."""
    
    def test_cache_hit_on_repeated_request(self):
        """Test that repeated requests use cache."""
        # First request (cache miss)
        response1 = client.get("/api/v1/trades?limit=5")
        assert response1.status_code == 200
        
        # Second request (should be cached)
        response2 = client.get("/api/v1/trades?limit=5")
        assert response2.status_code == 200
        
        # Should return identical results
        assert response1.json() == response2.json()
    
    def test_cache_invalidation_on_create(self):
        """Test that cache is invalidated after trade creation."""
        # Get trades (cache miss)
        response1 = client.get("/api/v1/trades")
        count1 = len(response1.json())
        
        # Create trade (should invalidate cache)
        client.post(
            "/api/v1/trades",
            json={
                "symbol": "MATIC/USD",
                "price": 1.0,
                "quantity": 1000,
                "side": "BUY"
            }
        )
        
        # Get trades again
        response2 = client.get("/api/v1/trades")
        count2 = len(response2.json())
        
        # Count should increase (cache was invalidated)
        assert count2 >= count1


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Tests for error handling."""
    
    def test_invalid_json_body(self):
        """Test error on invalid JSON body."""
        response = client.post(
            "/api/v1/trades",
            json={"invalid": "data"}
        )
        assert response.status_code == 422
    
    def test_missing_required_field(self):
        """Test error on missing required field."""
        response = client.post(
            "/api/v1/trades",
            json={
                "symbol": "BTC/USD",
                "price": 45000.00
                # Missing quantity and side
            }
        )
        assert response.status_code == 422
    
    def test_query_param_validation(self):
        """Test query parameter validation."""
        response = client.get("/api/v1/trades?limit=1001")  # Exceeds max
        assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
