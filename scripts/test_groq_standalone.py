import os
from langchain_groq import ChatGroq

os.environ['GROQ_API_KEY'] = 'gsk_dummy_key'
os.environ['OPENAI_API_KEY'] = 'sk-dummy-openai-key'

def test_groq():
    print("Testing ChatGroq standalone...")
    llm = ChatGroq(
        api_key='gsk_dummy_key',
        model='llama3-70b-8192',
        temperature=0
    )
    try:
        # We expect this to fail with Groq error, NOT OpenAI error
        llm.invoke("Hello")
    except Exception as e:
        print(f"Caught Exception: {e}")
        if "openai" in str(e).lower():
            print("[FAIL] ChatGroq is calling OpenAI!")
        else:
            print("[SUCCESS] ChatGroq failed with non-OpenAI error (likely Groq auth).")

if __name__ == "__main__":
    test_groq()
