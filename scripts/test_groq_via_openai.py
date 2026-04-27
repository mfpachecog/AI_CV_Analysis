import os
try:
    from langchain_openai import ChatOpenAI
    print("Imported ChatOpenAI")
except ImportError:
    print("ChatOpenAI not found")
    exit(1)

os.environ['GROQ_API_KEY'] = 'gsk_dummy_key'

def test_groq_via_openai():
    print("Testing ChatOpenAI pointing to Groq...")
    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key='gsk_dummy_key',
        model='llama3-70b-8192',
        temperature=0
    )
    try:
        llm.invoke("Hello")
    except Exception as e:
        print(f"Caught Exception: {e}")
        if "401" in str(e) and "Invalid API Key" in str(e): # Groq error message
             print("[SUCCESS] Failed with Groq error (expected).")
        elif "openai" in str(e).lower() and "incorrect api key" in str(e).lower():
             print("[FAIL] Failed with OpenAI error (unexpected).")
        else:
             print(f"[UNCERTAIN] {e}")

if __name__ == "__main__":
    test_groq_via_openai()
