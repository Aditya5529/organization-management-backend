
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
    
    assert response.status_code == 200, f"Create failed: {response.text}"
    print("Create successful")
    
    # 2. Login
    print("Logging in...")
    login_response = client.post("/admin/login", json={
        "email": email,
        "password": password
    })
    
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json()["access_token"]
    print(f"Login successful")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Update Check (Authenticated)
    print("Updating Org Creds...")
    new_email = f"new_{email}"
    update_response = client.put("/org/update", headers=headers, json={
        "email": new_email,
        "password": "newpassword"
    })
    assert update_response.status_code == 200, f"Update failed: {update_response.text}"
    print("Update successful")
    
    # 4. Delete Organization (No Body)
    print("Deleting Organization (without body)...")
    delete_response = client.delete("/org/delete", headers=headers)
    
    assert delete_response.status_code == 200, f"Delete failed: {delete_response.text}"
    print(f"Delete Response: {delete_response.json()}")

if __name__ == "__main__":
    try:
        test_full_flow()
        print("\nALL TESTS PASSED")
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
    except Exception as e:
        print(f"\nERROR: {e}")
