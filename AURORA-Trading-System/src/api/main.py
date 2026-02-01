# src/api/main.py
# AURORA Trading System - API Entry Point
# Created: 2026-02-01
# Purpose: Initialize and run the API server

from fastapi import FastAPI
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="AURORA Trading API",
    description="API for AURORA Trading System",
    version="2.1"
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "AURORA-API",
        "version": "2.1"
    }

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
