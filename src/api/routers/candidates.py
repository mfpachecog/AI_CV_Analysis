from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.candidate import CandidateCreate, CandidateResponse
from src.services.database import get_database
from uuid import uuid4

router = APIRouter()

@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate: CandidateCreate, db = Depends(get_database)):
    # Convertimos Pydantic a Diccionario
    candidate_dict = candidate.model_dump()
    # Generamos ID manual (Cosmos/Mongo lo hace auto, pero así controlamos el formato)
    candidate_dict["_id"] = str(uuid4())
    
    # Insertamos en la colección 'candidates'
    new_candidate = await db["candidates"].insert_one(candidate_dict)
    
    created_candidate = await db["candidates"].find_one({"_id": new_candidate.inserted_id})
    return created_candidate

@router.get("/{id}", response_model=CandidateResponse)
async def get_candidate(id: str, db = Depends(get_database)):
    candidate = await db["candidates"].find_one({"_id": id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidate
