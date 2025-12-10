from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI CV Analyzer"
    
    # Base de Datos (Mongo/Cosmos)
    DATABASE_URL: str
    DB_NAME: str = "cv_affinity_db"
    
    # Inteligencia Artificial (Groq)
    GROQ_API_KEY: str
    MODEL_NAME: str = "groq/llama3-8b-8192"
    
    # Azure Document Intelligence (OCR)
    AZURE_DOC_ENDPOINT: str
    AZURE_DOC_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore" # Ignora variables extra del sistema para evitar errores

settings = Settings()