from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI CV Analyzer"
    # La variable debe llamarse igual que en tu .env
    DATABASE_URL: str 
    DB_NAME: str = "cv_affinity_db"

    AZURE_DOC_ENDPOINT: str
    AZURE_DOC_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()