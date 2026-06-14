import requests

url = "https://praxiom-api-905423104833.europe-west1.run.app/"
try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    print("Headers:", response.headers)
    print("Response text:", response.text)
except Exception as e:
    print(f"Request failed: {str(e)}")
