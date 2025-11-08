#!/usr/bin/env python3
"""
Test registration endpoint
"""

import requests
import json

def test_registration():
    """Test the registration endpoint"""
    url = "http://localhost:8000/auth/register"
    
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        print("🔄 Testing registration endpoint...")
        response = requests.post(url, json=test_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration endpoint is working!")
        else:
            print("❌ Registration endpoint has issues")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()




















