from fastapi import HTTPException

from app.database.master_client import admins_col, organizations_col
from app.utils.password_handler import verify_password
from app.utils.jwt_handler import create_jwt


class AuthService:
    def login(self, email: str, password: str) -> dict:
        admin = admins_col.find_one({"email": email})
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, admin["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        org = organizations_col.find_one({"admin_id": admin["_id"]})
        if not org:
            raise HTTPException(status_code=400, detail="Organization not found for admin")

        token_payload = {
            "admin_id": str(admin["_id"]),
            "organization_name": org["organization_name"],
            "org_id": str(org["_id"]),
        }

        token = create_jwt(token_payload)
        return {"access_token": token, "token_type": "bearer"}
