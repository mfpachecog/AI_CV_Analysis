from typing import List, Set
import re

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

    def extract_skills(self, text: str) -> Set[str]:
        """
        Busca palabras clave en el texto y devuelve un set de skills únicas.
        """
        found_skills = set()
        # Normalizamos a minúsculas para comparar
        text_lower = text.lower()
        
        # Búsqueda simple (en el futuro esto lo hará un LLM)
        for skill in self.KNOWN_SKILLS:
            # Usamos regex para buscar la palabra completa (evitar 'java' en 'javascript')
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.add(skill)
                
        return found_skills