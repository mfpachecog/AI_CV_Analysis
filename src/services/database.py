"""
Database initialization and management service.
"""
from database.user import engine, Base
from src.models.user import User  # Import all models to register them with Base
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database initialization and management"""
    
    @staticmethod
    def init_db():
        """
        Initialize the database by creating all tables.
        This should be called on application startup.
        """
        try:
            # Import all models here to ensure they're registered with Base
            # This ensures all tables are created
            from src.models.user import User
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    @staticmethod
    def drop_all_tables():
        """
        Drop all database tables.
        WARNING: This will delete all data!
        Use only in development or with extreme caution.
        """
        try:
            Base.metadata.drop_all(bind=engine)
            logger.warning("All database tables dropped")
            return True
        except Exception as e:
            logger.error(f"Error dropping tables: {str(e)}")
            raise
    
    @staticmethod
    def recreate_db():
        """
        Recreate all database tables (drop and create).
        WARNING: This will delete all data!
        Use only in development or with extreme caution.
        """
        try:
            DatabaseService.drop_all_tables()
            DatabaseService.init_db()
            logger.info("Database recreated successfully")
            return True
        except Exception as e:
            logger.error(f"Error recreating database: {str(e)}")
            raise
    
    @staticmethod
    def check_connection():
        """
        Check if database connection is working.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            from sqlalchemy import text
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False

