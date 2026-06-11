import urllib.request
import json

data = json.dumps({
    "session_id": "test1234",
    "message": "Read this URL and learn from it: https://en.wikipedia.org/wiki/Electricity_market"
}).encode('utf-8')

req = urllib.request.Request(
    'http://localhost:8000/api/v1/chat/stream', 
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
