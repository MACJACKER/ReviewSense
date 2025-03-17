import requests
import json
import time
from datetime import datetime
import random
import string

# Configuration
BASE_URL = "http://localhost:8001"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_TEXT = "I really enjoyed this product. It exceeded my expectations!"

def print_separator():
    print("\n" + "="*50 + "\n")

def test_health_check():
    print("Testing health check endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check test passed")

def test_register_user():
    print("Testing user registration...")
    email = random_email()
    password = "test123456"
    
    data = {
        "email": email,
        "password": password
    }
    
    print(f"Registering user with email: {email}")
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json() if response.status_code < 400 else response.text}")
    
    if response.status_code == 200:
        print("Registration successful!")
        return email, password
    else:
        print("Registration failed!")
        return None, None

def test_login(email, password):
    print("Testing user login...")
    data = {
        "username": email,
        "password": password
    }
    
    print(f"Logging in with email: {email}")
    response = requests.post(f"{BASE_URL}/token", data=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json() if response.status_code < 400 else response.text}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Login successful!")
        return token
    else:
        print("Login failed!")
        return None

def test_analyze_sentiment(token):
    print("Testing authenticated sentiment analysis...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        f"{BASE_URL}/api/analyze",
        json={"text": TEST_TEXT},
        headers=headers
    )
    print(f"Status code: {response.status_code}")
    
    assert response.status_code == 200
    result = response.json()
    print(f"Response: {result}")
    assert "sentiment" in result
    assert "confidence" in result
    assert "timestamp" in result
    
    print("✅ Authenticated sentiment analysis test passed")
    return result

def test_analyze_sentiment_public():
    print("Testing public sentiment analysis...")
    response = requests.post(
        f"{BASE_URL}/api/analyze-public",
        json={"text": TEST_TEXT}
    )
    print(f"Status code: {response.status_code}")
    
    assert response.status_code == 200
    result = response.json()
    print(f"Response: {result}")
    assert "sentiment" in result
    assert "confidence" in result
    assert "timestamp" in result
    
    print("✅ Public sentiment analysis test passed")
    return result

def test_model_info(token):
    print("Testing model info endpoint...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        f"{BASE_URL}/api/model-info",
        headers=headers
    )
    print(f"Status code: {response.status_code}")
    
    assert response.status_code == 200
    result = response.json()
    print(f"Response: {result}")
    assert "model_type" in result
    assert "hidden_size" in result
    assert "num_labels" in result
    assert "vocab_size" in result
    assert "device" in result
    
    print("✅ Model info test passed")

def test_user_profile(token):
    print("Testing user profile endpoint...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        f"{BASE_URL}/api/me",
        headers=headers
    )
    print(f"Status code: {response.status_code}")
    
    assert response.status_code == 200
    result = response.json()
    print(f"Response: {result}")
    assert "email" in result
    assert result["email"] == TEST_EMAIL
    
    print("✅ User profile test passed")

def random_email():
    random_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{random_str}@example.com"

def run_all_tests():
    print(f"Starting API tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print_separator()
    
    try:
        # Test health check
        test_health_check()
        print_separator()
        
        # Test user registration
        email, password = test_register_user()
        if email and password:
            # Test login
            token = test_login(email, password)
            if token:
                # Test authenticated sentiment analysis
                sentiment_result = test_analyze_sentiment(token)
                print_separator()
                
                # Test public sentiment analysis
                public_sentiment_result = test_analyze_sentiment_public()
                print_separator()
                
                # Test model info
                test_model_info(token)
                print_separator()
                
                # Test user profile
                test_user_profile(token)
                print_separator()
                
                # Compare results
                print("Comparing authenticated and public sentiment analysis results:")
                print(f"Authenticated: {sentiment_result['sentiment']} with confidence {sentiment_result['confidence']}")
                print(f"Public: {public_sentiment_result['sentiment']} with confidence {public_sentiment_result['confidence']}")
                
                print_separator()
                print("🎉 All tests completed successfully!")
            else:
                print("\nLogin test failed!")
        else:
            print("\nRegistration test failed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_all_tests() 