#!/usr/bin/env python3
"""
Script to run the FastAPI development server.
"""
import sys
import os
import uvicorn

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.config import ConfigService

if __name__ == "__main__":
    settings = ConfigService.get_settings()
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

