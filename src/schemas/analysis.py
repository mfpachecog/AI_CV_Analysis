from pydantic import BaseModel
from typing import List, Dict, Any

class AnalysisRequest(BaseModel):
    candidate_id: str
    job_id: str

class AnalysisResult(BaseModel):
    affinity_score: int
    match_reason: str
    features: Dict[str, Any]  # Aquí guardaremos detalles técnicos como 'jaccard_index'