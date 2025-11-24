from motor.motor_asyncio import AsyncIOMotorClient
from src.services.config import settings

class DatabaseManager:
    client: AsyncIOMotorClient = None

db_manager = DatabaseManager()

async def get_database():
    # Retorna la instancia de la base de datos específica
    return db_manager.client[settings.DB_NAME]