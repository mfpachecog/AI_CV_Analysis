from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
from src.services.database import get_database

router = APIRouter()

# Schema interno (podría ir en src/schemas/jobs.py, pero lo dejo aquí para rapidez)
class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None

class JobResponse(JobCreate):
    id: str
    created_at: datetime

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate, db = Depends(get_database)):
    job_id = str(uuid4())
    job_doc = job.dict()
    job_doc["_id"] = job_id
    job_doc["created_at"] = datetime.utcnow()

    await db["jobs"].insert_one(job_doc)
    
    # Adaptamos para la respuesta (MongoDB usa _id, Pydantic usa id)
    job_doc["id"] = job_id
    return job_doc

@router.get("/", response_model=List[JobResponse])
async def list_jobs(db = Depends(get_database)):
    jobs = []
    cursor = db["jobs"].find()
    async for doc in cursor:
        doc["id"] = doc["_id"]
        jobs.append(doc)
    return jobs

@router.get("/{id}", response_model=JobResponse)
async def get_job(id: str, db = Depends(get_database)):
    doc = await db["jobs"].find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    doc["id"] = doc["_id"]
    return doc