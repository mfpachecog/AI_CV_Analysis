from typing import Dict, Any, Tuple

class AffinityScorerAgent:
    """
    US-07: Produce el affinity_score y match_reason.
    """

    def score_affinity(self, features: Dict[str, Any]) -> Tuple[int, str]:
        jaccard = features.get("jaccard_index", 0.0)
        overlap = features.get("overlap_count", 0)
        
        # Regla de negocio simple: El score es Jaccard * 100
        final_score = int(jaccard * 100)
        
        # Generar explicación dinámica
        if final_score >= 80:
            reason = f"¡Excelente Match! Coinciden en {overlap} habilidades clave."
        elif final_score >= 50:
            reason = f"Afinidad Media. Tienen {overlap} skills en común, pero faltan otras."
        else:
            reason = f"Baja afinidad. Solo coinciden en {overlap} habilidades."
            
        return final_score, reason