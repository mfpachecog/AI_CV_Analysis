from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# 1. Cargar variables de entorno
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("MODEL_NAME")

print(f"🔑 Verificando llave: {api_key[:5]}... (Oculto)")
print(f"🤖 Verificando modelo: {model_name}")

if not api_key:
    print("❌ ERROR: No se encontró GROQ_API_KEY en .env")
    exit()

try:
    # 2. Intentar conexión directa
    print("\n📞 Llamando a Groq...")
    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name=model_name,
        temperature=0
    )
    
    # 3. Pregunta simple
    response = llm.invoke("Di 'Hola, la conexión funciona' si me escuchas.")
    
    print("\n✅ ¡ÉXITO! Respuesta de Groq:")
    print(response.content)

except Exception as e:
    print("\n❌ FALLÓ LA CONEXIÓN:")
    print(str(e))
