from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.analysis import AnalysisRequest, AnalysisResult
from src.services.database import get_database
from src.ia.orchestrator import CrewOrchestrator
from uuid import uuid4
from datetime import datetime

router = APIRouter()
orchestrator = CrewOrchestrator()

@router.post("/", response_model=AnalysisResult, status_code=status.HTTP_201_CREATED)
async def perform_analysis(request: AnalysisRequest, db = Depends(get_database)):
    # 1. Validar que el Candidato exista
    candidate = await db["candidates"].find_one({"_id": request.candidate_id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    # 2. Validar que la Oferta exista
    job = await db["jobs"].find_one({"_id": request.job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")

    # 3. Ejecutar el Pipeline de IA (Tu Orchestrator)
    #    (Usamos los textos reales guardados en la BD)
    analysis_result = orchestrator.run_analysis(
        candidate_profile=candidate["raw_profile"],
        job_description=job["description"]
    )

    # 4. Preparar el objeto para guardar (Persistencia US-09)
    doc_to_save = {
        "_id": str(uuid4()),
        "candidate_id": request.candidate_id,
        "job_id": request.job_id,
        "created_at": datetime.utcnow(),
        "result": analysis_result # Guardamos todo el JSON que genera el orquestador
    }

    # 5. Guardar en Azure Cosmos DB
    # 5. Guardar en Azure Cosmos DB
    try:
        await db["analysis_results"].insert_one(doc_to_save)
    except Exception as e:
        print(f"WARNING: Failed to save analysis result to DB: {e}")
        # Add warning to features so client knows
        if "features" not in analysis_result:
            analysis_result["features"] = {}
        analysis_result["features"]["db_save_error"] = str(e)

    # 6. Retornar el resultado al usuario
    #    (Aplanamos la respuesta para que coincida con AnalysisResult)
    return {
        "affinity_score": analysis_result["affinity_score"],
        "match_reason": analysis_result["match_reason"],
        "features": analysis_result["features"]
    }

@router.get("/{id}")
async def get_analysis(id: str, db = Depends(get_database)):
    # US-10: Consultar un análisis pasado
    result = await db["analysis_results"].find_one({"_id": id})
    if not result:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    return result