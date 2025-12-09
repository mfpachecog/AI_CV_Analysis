import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'} if data else {}
    data_bytes = json.dumps(data).encode('utf-8') if data else None
    
    print(f"[{method}] {url}")
    if data:
        print(f"  Payload: {data}")

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            print(f"  Status: {status}")
            print(f"  Response: {body}")
            return status, json.loads(body)
    except urllib.error.HTTPError as e:
        print(f"  FAILED (HTTPError: {e.code})")
        print(f"  Response: {e.read().decode('utf-8')}")
        return e.code, None
    except Exception as e:
        print(f"  FAILED (Exception: {e})")
        return None, None

def main():
    print("Waiting 5 seconds for server to start...")
    time.sleep(5)

    # 1. Create Candidate
    print("\n--- Step 1: Create Candidate ---")
    candidate_data = {
        "name": "Juan",
        "email": "j@j.com",
        "raw_profile": "Experto en Python y Docker"
    }
    status, candidate_res = make_request("POST", "/candidates/", candidate_data)
    if status != 201 or not candidate_res:
        print("Stopping: Failed to create candidate.")
        return
    candidate_id = candidate_res.get("_id")
    print(f"  -> Candidate ID: {candidate_id}")

    # 2. Create Job
    print("\n--- Step 2: Create Job ---")
    job_data = {
        "title": "Dev",
        "description": "Buscamos Python y Docker"
    }
    status, job_res = make_request("POST", "/jobs/", job_data)
    if status != 201 or not job_res:
        print("Stopping: Failed to create job.")
        return
    job_id = job_res.get("_id")
    print(f"  -> Job ID: {job_id}")

    # 3. Run Analysis
    print("\n--- Step 3: Run Analysis ---")
    analysis_data = {
        "candidate_id": candidate_id,
        "job_id": job_id
    }
    status, analysis_res = make_request("POST", "/analysis/", analysis_data)
    
    if status == 200 and analysis_res:
        print("\nSUCCESS: Analysis completed.")
        print(f"  -> Affinity Score: {analysis_res.get('affinity_score')}")
    else:
        print("\nFAILURE: Analysis failed.")

if __name__ == "__main__":
    main()
