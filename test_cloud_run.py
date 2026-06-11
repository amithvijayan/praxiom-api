import urllib.request
import json

data = json.dumps({
    "session_id": "test1234",
    "message": "hello"
}).encode('utf-8')

req = urllib.request.Request(
    'https://praxiom-api-905423104833.europe-west1.run.app/api/v1/chat/stream', 
    data=data, 
    headers={'Content-Type': 'application/json'}
)

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
