# AI CV Analyzer 

Backend API construido con FastAPI y Azure Cosmos DB (MongoDB) para el análisis de afinidad entre hojas de vida y ofertas laborales usando Inteligencia Artificial.

## Sprint 1: Fundaciones

Este sprint establece la arquitectura base, la conexión a la nube y el CRUD principal.

### Características Implementadas
- **API REST:** FastAPI con arquitectura limpia (Clean Architecture).
- **Base de Datos:** Azure Cosmos DB for MongoDB (Capa gratuita).
- **Gestión de Candidatos:** Endpoint `POST /candidates` y `GET /candidates/{id}`.
- **Gestión de Ofertas:** Endpoint `POST /jobs` y `GET /jobs/{id}`.

###  Configuración e Instalación

#### 1. Prerrequisitos
- Python 3.10+
- Cuenta de Azure con Cosmos DB configurado.

#### 2. Instalación de Dependencias
Se recomienda usar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
pip install -r requirements.txt
