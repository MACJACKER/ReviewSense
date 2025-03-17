import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_TEXT = "This product is amazing! I love it."

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Health check: {response.status_code}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    return True

def test_register():
    # Generate a unique email to avoid conflicts
    timestamp = int(time.time())
    email = f"test_user_{timestamp}@example.com"
    
    data = {
        "email": email,
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/register", json=data)
    print(f"Register: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    assert response.json()["email"] == email
    return email

def test_login(email):
    data = {
        "username": email,
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/token", data=data)
    print(f"Login: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

def test_analyze(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "text": "I love this product, it's amazing!"
    }
    
    response = requests.post(f"{BASE_URL}/analyze", json=data, headers=headers)
    print(f"Analyze: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    result = response.json()
    assert "sentiment" in result
    assert "confidence" in result
    assert result["sentiment"] in ["positive", "negative"]
    print(f"Sentiment: {result['sentiment']}, Confidence: {result['confidence']}")
    return True

def test_model_info(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/model-info", headers=headers)
    print(f"Model Info: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    result = response.json()
    print(f"Model Info: {json.dumps(result, indent=2)}")
    return True

def test_model_metrics(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/model-metrics", headers=headers)
    print(f"Model Metrics: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    result = response.json()
    print(f"Model Metrics: {json.dumps(result, indent=2)}")
    return True

def test_analyze_public():
    data = {
        "text": TEST_TEXT
    }
    
    response = requests.post(f"{BASE_URL}/api/analyze-public", json=data)
    print(f"Analyze Public: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    assert "sentiment" in response.json()
    assert "confidence" in response.json()
    return response.json()

def run_tests():
    try:
        print("Testing API endpoints...")
        
        # Test health endpoint
        test_health()
        
        # Test public sentiment analysis (no auth required)
        test_analyze_public()
        
        # Test user registration
        email = test_register()
        
        # Test login
        token = test_login(email)
        
        # Test sentiment analysis
        test_analyze(token)
        
        # Test model info
        test_model_info(token)
        
        # Test model metrics
        test_model_metrics(token)
        
        print("All tests passed!")
        return True
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
        return False
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    run_tests() 