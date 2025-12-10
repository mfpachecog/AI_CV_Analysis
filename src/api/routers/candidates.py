from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from src.services.database import get_database
from src.schemas.candidates import CandidateResponse
from src.services.ocr import AzureOCRService
from uuid import uuid4
from datetime import datetime

router = APIRouter()
ocr_service = AzureOCRService()

@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    # Recibimos el archivo y los datos del formulario (multipart/form-data)
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    db = Depends(get_database)
):
    # 1. Validar formato del archivo
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")

    # 2. Leer el archivo en memoria (bytes)
    file_content = await file.read()

    # 3. Enviar a Azure Document Intelligence (OCR)
    try:
        extracted_text = ocr_service.extract_text_from_pdf(file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo el PDF: {str(e)}")

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF (¿está vacío o es una imagen sin texto?).")

    # 4. Crear el documento para MongoDB
    candidate_id = str(uuid4())
    candidate_doc = {
        "_id": candidate_id,
        "name": name,
        "email": email,
        "raw_profile": extracted_text,  # Aquí guardamos lo que leyó la IA
        "created_at": datetime.utcnow()
    }

    # 5. Guardar en Base de Datos
    await db["candidates"].insert_one(candidate_doc)

    return candidate_doc

@router.get("/{id}", response_model=CandidateResponse)
async def get_candidate(id: str, db = Depends(get_database)):
    candidate = await db["candidates"].find_one({"_id": id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidate