# src/api/main.py
# AURORA Trading System - API Entry Point
# Updated: 2026-02-02 (ST-20260202-004)
# Purpose: Initialize FastAPI with integrated routes (DB + Cache + Events)

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn

# Import integrated routes
from .routes import router

# Initialize FastAPI application with OpenAPI documentation
app = FastAPI(
    title="AURORA Trading API",
    description="Unified API integrating Database, Cache, and Event Store",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Include integrated routes
app.include_router(router)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AURORA Trading API",
        version="1.0.0",
        description="API Integration Layer - Cache + Database + Events",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
