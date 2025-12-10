from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from src.services.database import get_database
from src.ia.orchestrator import CrewOrchestrator
from uuid import uuid4
from datetime import datetime

router = APIRouter()
orchestrator = CrewOrchestrator()

class AnalysisRequest(BaseModel):
    candidate_id: str
    job_id: str

@router.post("/")
async def perform_analysis(request: AnalysisRequest, db = Depends(get_database)):
    # 1. Buscar Candidato
    candidate = await db["candidates"].find_one({"_id": request.candidate_id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    
    # 2. Buscar Oferta
    job = await db["jobs"].find_one({"_id": request.job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")

    # 3. Validar que tengamos el texto del perfil (extraído del PDF)
    if "raw_profile" not in candidate or not candidate["raw_profile"]:
        raise HTTPException(status_code=400, detail="El candidato no tiene texto de perfil procesado.")

    # 4. EJECUTAR LA MAGIA (CrewAI)
    # Nota: Pasamos is_pdf=False porque ya tenemos el texto extraído en la BD
    try:
        analysis_result = orchestrator.run_analysis(
            candidate_input=candidate["raw_profile"], 
            job_description=job["description"],
            is_pdf=False 
        )
    except Exception as e:
        print(f"Error en CrewAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno de IA: {str(e)}")

    # 5. Guardar Resultado
    result_doc = {
        "_id": str(uuid4()),
        "candidate_id": request.candidate_id,
        "job_id": request.job_id,
        "created_at": datetime.utcnow(),
        "result": analysis_result
    }
    await db["analysis_results"].insert_one(result_doc)

    return result_doc