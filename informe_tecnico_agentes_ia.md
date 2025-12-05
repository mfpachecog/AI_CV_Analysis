# Informe Técnico: Análisis de Agentes de IA

## Resumen General
El sistema utiliza una arquitectura de agentes basada en reglas y lógica matemática determinista para el análisis de compatibilidad entre candidatos y ofertas laborales. Actualmente (V1), no implementa modelos de Deep Learning o LLMs, apoyándose en la librería estándar de Python para eficiencia y control.

## Desglose de Agentes

### 1. Agente Extractor (`src/ia/agents/extractor.py`)
*   **Propósito:** Identificar y extraer habilidades técnicas ("skills") desde textos no estructurados (perfiles y ofertas).
*   **Algoritmo (Rule-Based):**
    *   Utiliza una lista predefinida de habilidades conocidas (`KNOWN_SKILLS`: python, java, docker, etc.).
    *   Realiza normalización de texto (minúsculas) y búsqueda exacta de palabras.
*   **Implementación Técnica:**
    *   Uso de **Expresiones Regulares (`re`)** con delimitadores de palabra (`\b`) para evitar falsos positivos (ej. distinguir "Java" de "JavaScript").

### 2. Agente Procesador (`src/ia/agents/processor.py`)
*   **Propósito:** Calcular métricas objetivas de similitud entre conjuntos de habilidades.
*   **Algoritmo:**
    *   **Intersección:** Identificación de elementos comunes.
    *   **Índice de Jaccard:** Cálculo estadístico de similitud definido como:
      $$ J(A,B) = \frac{|A \cap B|}{|A \cup B|} $$
*   **Implementación Técnica:**
    *   Uso de estructuras de datos nativas de Python: `set` para operaciones de conjuntos (`intersection`, `union`), optimizando la velocidad de cálculo.

### 3. Agente de Puntuación (`src/ia/agents/scorer.py`)
*   **Propósito:** Interpretar las métricas matemáticas para generar una puntuación de negocio y feedback textual.
*   **Algoritmo:**
    *   **Scoring:** Conversión lineal del Índice de Jaccard a una escala porcentual (0-100).
    *   **Feedback Dinámico:** Clasificación basada en umbrales:
        *   Score >= 80: "Excelente Match"
        *   Score >= 50: "Afinidad Media"
        *   Score < 50: "Baja Afinidad"
*   **Implementación Técnica:**
    *   Lógica condicional simple sin dependencias externas.

## Conclusión
Esta arquitectura V1 prioriza la transparencia y la velocidad de ejecución. Es extensible para futuras versiones donde el Agente Extractor podría ser reemplazado por un modelo NLP (BERT/GPT) y el Agente de Puntuación por un modelo de clasificación entrenado, sin alterar la estructura de orquestación.
