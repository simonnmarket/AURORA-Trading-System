# PostgreSQL Configuration for AURORA Trading System
"""
Database configuration module for AURORA Trading System.
Manages PostgreSQL connection pooling and ORM setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL - PostgreSQL local connection
# Format: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://aurora:aurora_secure_password@localhost:5432/aurora_db"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL statements for debugging
    future=True,  # Use new 2.0 style API
    pool_pre_ping=True,  # Test connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20  # Max overflow connections
)

# Session factory for ORM operations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base for declarative models
Base = declarative_base()

# Test connection function
def test_connection():
    """Test PostgreSQL connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            print("✅ PostgreSQL connection successful!")
            return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False


# Dependency function for FastAPI
def get_db():
    """Get database session dependency for FastAPI.
    
    Yields:
        SessionLocal: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
