import requests

BASE_URL = "http://127.0.0.1:8000"

def test_workflow():
    # 1. Test Signup
    user_data = {"username": "testuser_1", "password": "securepassword123"}
    print("--- Testing Signup ---")
    response = requests.post(f"{BASE_URL}/signup", json=user_data)
    print(response.status_code, response.json())

    # 2. Test Login (Get JWT Token)
    print("\n--- Testing Login ---")
    login_data = {"username": "testuser_1", "password": "securepassword123"}
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    token = response.json().get("access_token")
    print(f"Token received: {token[:20]}...")

    # 3. Test Save Note (Protected Route)
    print("\n--- Testing Save Note (CRUD) ---")
    headers = {"Authorization": f"Bearer {token}"}
    note_data = {
        "raw_text": "Photosynthesis is the process by which plants use sunlight...",
        "summary": "Plants make food using light.",
        "concepts": {"Biology": "Photosynthesis", "Energy": "Sunlight"}
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note_data, headers=headers)
    print(response.status_code, response.json())

if __name__ == "__main__":
    test_workflow()
    