from fastapi import FastAPI
from src.services.lifecycle import lifespan
from src.api.routers import candidates, jobs # importar jobs tambien


app = FastAPI(
    title="AI CV Analyzer",
    version = "1.0.0",
    lifespan=lifespan
)

app.include_router(candidates.router, prefix="/candidates", tags=["Candidatos"])
app.include_router(jobs.router, prefix="/jobs", tags=["Ofertas"])

@app.get("/")
async def root():
    return {"status": "API Online", "docs": "/docs"}