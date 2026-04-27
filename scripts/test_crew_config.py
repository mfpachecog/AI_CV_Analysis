import os
import sys

# Add project root to python path
sys.path.append(os.getcwd())

# Mock environment variables BEFORE importing config
os.environ['GROQ_API_KEY'] = 'gsk_dummy_key_for_testing_groq_config'
os.environ['MODEL_NAME'] = 'llama3-70b-8192'
os.environ['DATABASE_URL'] = 'mongodb://localhost:27017'
os.environ['AZURE_DOC_ENDPOINT'] = 'https://dummy.cognitiveservices.azure.com/'
os.environ['AZURE_DOC_KEY'] = 'dummy_key'
os.environ['OPENAI_API_KEY'] = 'gsk_dummy_key_for_testing_groq_config'

try:
    from src.ia.orchestrator import CrewOrchestrator
    print("Successfully imported CrewOrchestrator")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

def test_orchestrator():
    print("Initializing Orchestrator...")
    orchestrator = CrewOrchestrator()
    
    candidate_text = "Experto en Python y FastAPI con 5 años de experiencia."
    job_text = "Buscamos desarrollador Python con conocimientos de FastAPI."
    
    print("Running analysis (expecting failure due to dummy key, but checking WHICH failure)...")
    try:
        result = orchestrator.run_analysis(candidate_text, job_text)
        print("Result:", result)
    except Exception as e:
        print(f"\nCaught Exception: {type(e).__name__}: {e}")
        # Check if it's an OpenAI error or Groq error
        error_str = str(e).lower()
        if "openai" in error_str or "api key" in error_str and "na" in error_str:
            print("\n[FAIL] It seems to be trying to use OpenAI!")
        elif "groq" in error_str or "401" in error_str:
             print("\n[SUCCESS] It failed with Groq error as expected (since key is dummy).")
        else:
            print(f"\n[UNCERTAIN] Unknown error: {e}")

if __name__ == "__main__":
    test_orchestrator()
