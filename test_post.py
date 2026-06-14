import requests
import json

url = "http://127.0.0.1:8000/api/v1/chat/stream"
payload = {
    "session_id": "test-session",
    "message": "Pull live market data for TSLA, NEE, and ENPH"
}

headers = {"Content-Type": "application/json"}

print("Sending request...")
response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Response text:", response.text)
