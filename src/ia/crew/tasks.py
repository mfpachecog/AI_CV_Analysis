from crewai import Task
from textwrap import dedent

class CVAnalysisTasks:
    
    def extraction_task(self, agent, text_type, text_content):
        return Task(
            description=dedent(f"""
                Analiza el siguiente texto de tipo '{text_type}':
                
                '''
                {text_content}
                '''

                Extrae una lista de habilidades técnicas (skills) y un breve resumen profesional.
                Ignora información irrelevante como direcciones o hobbies.
            """),
            expected_output="Una lista de skills (Python, Java, etc.) y un resumen de 2 líneas.",
            agent=agent
        )

    def processing_task(self, agent, candidate_analysis, job_analysis):
        return Task(
            description=dedent(f"""
                Compara las habilidades extraídas del Candidato contra la Oferta.
                
                Datos Candidato: {candidate_analysis}
                Datos Oferta: {job_analysis}
                
                Identifica:
                1. Skills que coinciden (Match).
                2. Skills requeridas por la oferta que el candidato NO tiene (Gap).
            """),
            expected_output="Lista de coincidencias y lista de faltantes.",
            agent=agent
        )

    def scoring_task(self, agent, comparison_result):
        return Task(
            description=dedent(f"""
                Basado en esta comparación:
                {comparison_result}
                
                Asigna un Puntaje de Afinidad (0 a 100).
                - 100: Tiene todo y más.
                - 50: Tiene la mitad.
                - 0: No tiene nada.
                
                Genera un JSON ESTRICTO con este formato (sin texto extra):
                {{
                    "affinity_score": 75,
                    "match_reason": "Breve explicación de por qué..."
                }}
            """),
            expected_output="Un objeto JSON con affinity_score y match_reason.",
            agent=agent
        )