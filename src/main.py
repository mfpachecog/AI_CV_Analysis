from fastapi import FastAPI
from src.services.lifecycle import lifespan
from src.api.routers import candidates # importar jobs tambien
# from src.api.routers import jobs 

app = FastAPI(
    title="AI CV Analyzer",
    lifespan=lifespan
)

app.include_router(candidates.router, prefix="/candidates", tags=["Candidatos"])
# app.include_router(jobs.router, prefix="/jobs", tags=["Ofertas"])

@app.get("/")
async def root():
    return {"status": "API Online", "docs": "/docs"}