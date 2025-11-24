from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.jobs import JobCreate, JobResponse
from src.services.database import get_database
from uuid import uuid4

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate, db = Depends(get_database)):
    job_dict = job.model_dump()
    job_dict["_id"] = str(uuid4())
    
    await db["jobs"].insert_one(job_dict)
    
    created_job = await db["jobs"].find_one({"_id": job_dict["_id"]})
    return created_job

@router.get("/{id}", response_model=JobResponse)
async def get_job(id: str, db = Depends(get_database)):
    job = await db["jobs"].find_one({"_id": id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job