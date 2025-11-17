"""
Application lifecycle management service.
Handles startup and shutdown events.
"""
import logging
from contextlib import asynccontextmanager
from database.user import engine
from src.services.database import DatabaseService
from src.services.config import ConfigService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    
    Usage in main.py:
        app = FastAPI(lifespan=lifespan)
    """
    # Startup
    logger.info("Starting application...")
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        DatabaseService.init_db()
        
        # Check database connection
        if DatabaseService.check_connection():
            logger.info("Database connection verified")
        else:
            logger.warning("Database connection check failed")
        
        # Log configuration
        config = ConfigService.get_settings()
        logger.info(f"Application: {config.APP_NAME} v{config.APP_VERSION}")
        logger.info(f"Debug mode: {config.DEBUG}")
        logger.info(f"Database: {config.DATABASE_URL.split('@')[-1] if '@' in config.DATABASE_URL else config.DATABASE_URL}")
        
        logger.info("Application startup complete")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    
    try:
        # Close database connections
        engine.dispose()
        logger.info("Database connections closed")
        
        logger.info("Application shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


class LifecycleService:
    """Service for managing application lifecycle"""
    
    @staticmethod
    def on_startup():
        """Actions to perform on application startup"""
        logger.info("Executing startup tasks...")
        
        # Initialize database
        DatabaseService.init_db()
        
        # Verify database connection
        DatabaseService.check_connection()
        
        logger.info("Startup tasks completed")
    
    @staticmethod
    def on_shutdown():
        """Actions to perform on application shutdown"""
        logger.info("Executing shutdown tasks...")
        
        # Close database connections
        engine.dispose()
        
        logger.info("Shutdown tasks completed")

