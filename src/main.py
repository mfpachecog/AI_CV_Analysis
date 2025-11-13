import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import user
from src.services.lifecycle import lifespan
from src.services.config import ConfigService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Get settings
settings = ConfigService.get_settings()

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    description="AI application that reads and understands CVs from possible candidates",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to CV Analysis API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }

@app.get("/dev")
def read_dev():
    """Development endpoint"""
    message = "Hello this is my first app in FastAPI"
    return {"message": message}