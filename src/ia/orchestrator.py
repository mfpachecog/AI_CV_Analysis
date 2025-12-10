from crewai import Crew
from src.ia.crew.agents import CVAnalysisAgents
from src.ia.crew.tasks import CVAnalysisTasks
import json

class CrewOrchestrator:
    def run_analysis(self, candidate_input: str, job_description: str):
        # 1. Instanciar Agentes y Tareas
        agents = CVAnalysisAgents()
        tasks = CVAnalysisTasks()

        extractor = agents.extractor_agent()
        processor = agents.processor_agent()
        scorer = agents.scorer_agent()

        # 2. Crear las Tareas encadenadas
        # Tarea A: Leer Candidato
        task_extract_cand = tasks.extraction_task(extractor, "Candidato", candidate_input)
        # Tarea B: Leer Oferta
        task_extract_job = tasks.extraction_task(extractor, "Oferta Laboral", job_description)
        # Tarea C: Comparar (Processor) - Depende de A y B
        task_process = tasks.processing_task(processor, task_extract_cand, task_extract_job) 
        # Tarea D: Puntuar (Scorer) - Depende de C
        task_score = tasks.scoring_task(scorer, task_process)

        # 3. Armar el Equipo (Crew)
        crew = Crew(
            agents=[extractor, processor, scorer],
            tasks=[task_extract_cand, task_extract_job, task_process, task_score],
            verbose=True,
            memory=False  # <--- ¡AGREGA ESTO! (Apaga los embeddings de OpenAI)
        )

        # 4. ¡Acción!
        result = crew.kickoff()

        # 5. Parsear el resultado final (que esperamos sea JSON)
        try:
            # A veces los LLM ponen ```json ... ```, limpiamos eso
            clean_result = str(result).replace("```json", "").replace("```", "")
            return json.loads(clean_result)
        except:
            # Fallback si el LLM no devolvió JSON puro
            return {
                "affinity_score": 0,
                "match_reason": "Error procesando respuesta de IA: " + str(result),
                "features": {}
            }