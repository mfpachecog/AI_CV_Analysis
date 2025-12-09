from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from typing import List, Dict, Any

class CandidateClusterer:
    """
    Implementación de K-Means para agrupar candidatos según su perfil.
    Cumple con el requisito US-14 de IA Clásica.
    """
    
    def __init__(self, n_clusters: int = 3):
        """
        Args:
            n_clusters: Número de grupos a formar (ej: 3 para Junior, Mid, Senior)
        """
        self.n_clusters = n_clusters
        # Vectorizador: Convierte texto a matriz numérica, eliminando palabras comunes (stop words)
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    def train_and_predict(self, candidates_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Entrena el modelo con los perfiles actuales y asigna un grupo a cada candidato.
        
        Args:
            candidates_data: Lista de dicts con al menos 'id' y 'raw_profile'
            
        Returns:
            La misma lista pero enriquecida con el campo 'cluster_id'
        """
        if len(candidates_data) < self.n_clusters:
            print(f"⚠️ Advertencia: Hay menos candidatos ({len(candidates_data)}) que clusters ({self.n_clusters}).")
            # Si hay pocos datos, ajustamos dinámicamente o retornamos grupo 0
            current_k = len(candidates_data) if len(candidates_data) > 0 else 1
            self.model = KMeans(n_clusters=current_k, random_state=42, n_init=10)

        # 1. Extraer solo los textos de los perfiles
        corpus = [c.get("raw_profile", "") for c in candidates_data]
        
        # 2. Convertir Texto -> Vectores Numéricos
        # (La IA no lee letras, lee matemáticas)
        vectors = self.vectorizer.fit_transform(corpus)
        
        # 3. Entrenar K-Means (Encontrar los centroides)
        self.model.fit(vectors)
        
        # 4. Obtener las etiquetas (0, 1, 2...)
        labels = self.model.labels_
        
        # 5. Pegar la etiqueta de vuelta al candidato
        results = []
        for i, candidate in enumerate(candidates_data):
            candidate_copy = candidate.copy()
            candidate_copy["cluster_id"] = int(labels[i])
            results.append(candidate_copy)
            
        return results

    def get_cluster_terms(self, top_n: int = 5) -> Dict[int, List[str]]:
        """
        Intenta explicar qué significa cada cluster extrayendo sus palabras clave.
        Útil para la documentación del algoritmo.
        """
        if not hasattr(self.model, 'cluster_centers_'):
            return {}
            
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names_out()
        
        cluster_keywords = {}
        for i in range(self.n_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :top_n]]
            cluster_keywords[i] = top_terms
            
        return cluster_keywords