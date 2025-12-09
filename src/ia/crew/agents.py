from crewai import Agent
from langchain_groq import ChatGroq
from src.services.config import settings

class CVAnalysisAgents:
    def __init__(self):
        # Conectamos el cerebro (Groq - Llama3)
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0  # Cero creatividad, máxima precisión
        )

    def extractor_agent(self):
        return Agent(
            role='Extractor de Perfiles Técnicos',
            goal='Extraer habilidades técnicas, experiencia y resumen de textos crudos.',
            backstory="""Eres un experto reclutador técnico con ojo de águila. 
            Tu trabajo es leer hojas de vida (CVs) y descripciones de trabajo sucias 
            y extraer listas limpias y estructuradas de tecnologías y habilidades.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def processor_agent(self):
        return Agent(
            role='Analista de Datos de RRHH',
            goal='Comparar objetivamente listas de habilidades y calcular coincidencias.',
            backstory="""Eres un analista frío y calculador. Tu única misión es tomar 
            las habilidades del candidato y las de la oferta, cruzarlas matemáticamente 
            y reportar cuáles coinciden y cuáles faltan.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def scorer_agent(self):
        return Agent(
            role='Juez de Afinidad Laboral',
            goal='Determinar el puntaje final de afinidad (0-100) y justificarlo.',
            backstory="""Eres el juez final en el proceso de contratación. 
            Basado en el análisis técnico, decides si el candidato es apto. 
            Siempre das un puntaje numérico y una explicación honesta y directa.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )