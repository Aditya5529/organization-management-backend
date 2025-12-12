
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_full_flow():
    # 1. Create Organization
    org_name = f"TestOrg_{uuid.uuid4().hex[:8]}"
    email = f"admin_{uuid.uuid4().hex[:8]}@example.com"
    password = "securepassword"
    
    print(f"Creating Org: {org_name}, {email}")
    
    response = client.post("/org/create", json={
        "organization_name": org_name,
        "email": email,
        "password": password
    })
    
    if response.status_code != 200:
        print(f"Create failed: {response.text}")
        return
    
    print("Create successful")
    
    # 2. Login
    print("Logging in...")
    login_response = client.post("/admin/login", json={
        "email": email,
        "password": password
    })
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
        
    token = login_response.json()["access_token"]
    print(f"Login successful, token: {token[:10]}...")
    
    # 3. Delete Organization
    print("Deleting Organization...")
    headers = {"Authorization": f"Bearer {token}"}
    # IMPORTANT: Delete with JSON body
    delete_response = client.request("DELETE", "/org/delete", headers=headers, json={
        "organization_name": org_name
    })
    
    print(f"Delete Status: {delete_response.status_code}")
    print(f"Delete Response: {delete_response.text}")

if __name__ == "__main__":
    test_full_flow()
