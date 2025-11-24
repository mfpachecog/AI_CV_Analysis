import urllib.request
import urllib.error
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_test(name, method, url, data=None, expected_status=200):
    print(f"Running Test {name}: {method} {url} ...", end=" ")
    
    full_url = f"{BASE_URL}{url}"
    headers = {'Content-Type': 'application/json'} if data else {}
    
    if data:
        data_bytes = json.dumps(data).encode('utf-8')
    else:
        data_bytes = None

    req = urllib.request.Request(full_url, data=data_bytes, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            response_body = response.read().decode('utf-8')
            
            if status == expected_status:
                print("PASSED")
                return json.loads(response_body) if response_body else {}
            else:
                print(f"FAILED (Status: {status}, Expected: {expected_status})")
                print(f"Response: {response_body}")
                return None
    except urllib.error.HTTPError as e:
        print(f"FAILED (HTTPError: {e.code})")
        print(f"Response: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"FAILED (Exception: {e})")
        return None

def main():
    print("Waiting 5 seconds for server to start...")
    time.sleep(5)

    # Test A: Health
    run_test("A (Health)", "GET", "/", expected_status=200)

    # Test B: Create Candidate
    candidate_data = {
        "name": "Juan Perez",
        "email": "juan@test.com",
        "raw_profile": "Ingeniero Python Senior"
    }
    candidate_response = run_test("B (Create Candidate)", "POST", "/candidates/", data=candidate_data, expected_status=201)
    
    if not candidate_response or "_id" not in candidate_response:
        print("CRITICAL: Could not create candidate, skipping Test C.")
        candidate_id = None
    else:
        candidate_id = candidate_response["_id"]
        print(f"  -> Candidate ID: {candidate_id}")

    # Test C: Read Candidate
    if candidate_id:
        read_response = run_test(f"C (Read Candidate {candidate_id})", "GET", f"/candidates/{candidate_id}", expected_status=200)
        if read_response:
            # Verify data matches
            if (read_response.get("name") == candidate_data["name"] and 
                read_response.get("email") == candidate_data["email"]):
                print("  -> Data verification PASSED")
            else:
                print("  -> Data verification FAILED")
                print(f"     Expected: {candidate_data}")
                print(f"     Got: {read_response}")

    # Test D: Create Job
    job_data = {
        "title": "DevOps Engineer",
        "description": "Experiencia en Azure"
    }
    run_test("D (Create Job)", "POST", "/jobs/", data=job_data, expected_status=201)

    print("\nALL TESTS COMPLETED.")

if __name__ == "__main__":
    main()
