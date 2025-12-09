from src.ia.agents.extractor import ExtractorAgent
from src.ia.agents.processor import ProcessorAgent
from src.ia.agents.scorer import AffinityScorerAgent
from typing import Dict, Any

class CrewOrchestrator:
    """
    Coordina el flujo completo: Texto -> Skills -> Métricas -> Score
    """
    def __init__(self):
        self.extractor = ExtractorAgent()
        self.processor = ProcessorAgent()
        self.scorer = AffinityScorerAgent()

    def run_analysis(self, candidate_profile: str, job_description: str) -> Dict[str, Any]:
        # 1. Extracción
        cand_skills = self.extractor.extract_skills(candidate_profile)
        job_skills = self.extractor.extract_skills(job_description)
        
        # 2. Procesamiento Matemático
        features = self.processor.calculate_similarity(cand_skills, job_skills)
        
        # 3. Puntuación y Razón
        score, reason = self.scorer.score_affinity(features)
        
        # 4. Empaquetar resultado
        return {
            "affinity_score": score,
            "match_reason": reason,
            "features": features,
            "extracted_data": {
                "candidate_skills": list(cand_skills),
                "job_skills": list(job_skills)
            }
        }