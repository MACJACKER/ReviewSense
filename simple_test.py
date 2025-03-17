import requests
import json

# Test the health endpoint
response = requests.get("http://localhost:8000/api/health")
print(f"Health endpoint: {response.status_code}")
print(f"Response: {response.text}")

# Test the analyze endpoint
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"text": "I love this product!"},
    headers={"Authorization": "Bearer dummy_token"}
)
print(f"Analyze endpoint: {response.status_code}")
print(f"Response: {response.text}")

# Test the model info endpoint
response = requests.get(
    "http://localhost:8000/api/model-info",
    headers={"Authorization": "Bearer dummy_token"}
)
print(f"Model Info endpoint: {response.status_code}")
if response.status_code == 200:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
else:
    print(f"Response: {response.text}") 