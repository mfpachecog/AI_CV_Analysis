from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from src.services.config import settings
from src.services.database import db_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conectar a Azure Cosmos DB
    print("Conectando a Base de Datos...")
    db_manager.client = AsyncIOMotorClient(settings.DATABASE_URL)
    print("¡Conexión Exitosa!")
    yield
    # Shutdown: Cerrar conexión
    print("Cerrando conexión a Base de Datos...")
    db_manager.client.close()