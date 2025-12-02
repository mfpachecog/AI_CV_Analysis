from typing import Set, Dict

class ProcessorAgent:
    """
    US-06: Calcula indicadores numéricos (Jaccard, Overlap).
    """

    def calculate_similarity(self, candidate_skills: Set[str], job_skills: Set[str]) -> Dict[str, float]:
        if not candidate_skills or not job_skills:
            return {"jaccard_index": 0.0, "overlap_count": 0}

        # Intersección: Skills que tienen AMBOS
        intersection = candidate_skills.intersection(job_skills)
        
        # Unión: Todas las skills mencionadas (sin repetir)
        union = candidate_skills.union(job_skills)
        
        # Índice de Jaccard
        jaccard = len(intersection) / len(union)
        
        return {
            "jaccard_index": round(jaccard, 2),
            "overlap_count": len(intersection),
            "total_union": len(union),
            "common_skills": list(intersection)
        }