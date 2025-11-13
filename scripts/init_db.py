#!/usr/bin/env python3
"""
Database initialization script.
Run this script to create all database tables.
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.database import DatabaseService
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Initialize the database"""
    try:
        logger.info("Initializing database...")
        DatabaseService.init_db()
        logger.info("Database initialized successfully!")
        return 0
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

