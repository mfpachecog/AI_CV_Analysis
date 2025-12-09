from typing import List, Set
import re
from src.services.config import settings
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class ExtractorAgent:
    """
    US-05: Extrae skills desde textos de candidatos y ofertas.
    Versión V1: Búsqueda de palabras clave (Rule-Based).
    """
    
    # Lista básica de skills para probar el flujo
    KNOWN_SKILLS = {
        "python", "fastapi", "azure", "mongodb", "sql", "java", 
        "docker", "kubernetes", "react", "scrum", "git", "linux"
    }

    def __init__(self):
        # Inicializamos el cliente de Azure solo si las claves existen
        try:
            self.doc_client = DocumentAnalysisClient(
                endpoint=settings.AZURE_DOC_ENDPOINT,
                credential=AzureKeyCredential(settings.AZURE_DOC_KEY)
            )
            print("✅ ExtractorAgent conectado a Azure AI.")
        except Exception as e:
            print(f"⚠️ Azure AI no configurado: {e}")
            self.doc_client = None

    def extract_from_text(self, text: str) -> Set[str]:
        """Modo 1: Recibe texto plano (ej: desde n8n)"""
        found_skills = set()
        text_lower = text.lower()
        for skill in self.KNOWN_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.add(skill)
        return found_skills