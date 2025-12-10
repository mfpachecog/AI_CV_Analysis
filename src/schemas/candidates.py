from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    raw_profile: str = Field(..., description="Texto completo del CV")

class CandidateResponse(CandidateCreate):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True