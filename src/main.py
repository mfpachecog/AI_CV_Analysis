from fastapi import FastAPI
from src.api.routers import user

app = FastAPI(
    title="CV Analysis API",
    description="AI application that reads and understands CVs from possible candidates",
    version="1.0.0"
)

# Include routers
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CV Analysis API"}

@app.get("/dev")
def read_dev():
    message = "Hello this is my first app in FastAPI"
    return {"message": message}