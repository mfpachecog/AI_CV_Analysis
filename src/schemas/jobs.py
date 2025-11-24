from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., description="Descripción de la oferta")

class JobResponse(JobCreate):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True