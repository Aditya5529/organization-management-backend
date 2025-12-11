from fastapi import APIRouter

from app.schemas.admin_schema import AdminLoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin", tags=["Admin"])
service = AuthService()


@router.post("/login", response_model=TokenResponse)
def admin_login(payload: AdminLoginRequest):
    return service.login(email=payload.email, password=payload.password)
