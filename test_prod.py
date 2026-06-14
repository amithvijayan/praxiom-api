import requests
import json
import uuid

url = "https://praxiom-api-905423104833.europe-west1.run.app/api/v1/chat/stream"
payload = {
    "session_id": str(uuid.uuid4()),
    "message": "Pull live market data for TSLA, NEE, and ENPH"
}

headers = {"Content-Type": "application/json"}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print("Response text:", response.text)
except Exception as e:
    print(f"Request failed: {str(e)}")
