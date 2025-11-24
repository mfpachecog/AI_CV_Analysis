import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def main():
    print("Waiting 5 seconds for server to start...")
    time.sleep(5)

    url = "/candidates/"
    full_url = f"{BASE_URL}{url}"
    
    payload = {
        "name": "Prueba Azure",
        "email": "test@azure.com",
        "raw_profile": "Perfil de prueba conexión Azure"
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}

    print(f"Sending POST to {full_url} with payload: {payload}")

    req = urllib.request.Request(full_url, data=data_bytes, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"Status Code: {status}")
            print("Response Body:")
            print(response_body)
            
            if status == 201:
                print("\nSUCCESS: Candidate created successfully.")
            else:
                print(f"\nFAILURE: Unexpected status code {status}")

    except urllib.error.HTTPError as e:
        print(f"FAILED (HTTPError: {e.code})")
        print(f"Response: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"FAILED (Exception: {e})")

if __name__ == "__main__":
    main()
