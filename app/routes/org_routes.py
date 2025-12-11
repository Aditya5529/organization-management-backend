from fastapi import APIRouter, Depends, Query, Body

from app.schemas.org_schema import (
    OrgCreateRequest,
    OrgUpdateRequest,
    OrgDeleteRequest,
)
from app.services.org_service import OrganizationService
from app.utils.jwt_handler import get_current_admin

router = APIRouter(prefix="/org", tags=["Organization"])
service = OrganizationService()


@router.post("/create")
def create_org(payload: OrgCreateRequest):
    return service.create_organization(
        organization_name=payload.organization_name,
        email=payload.email,
        password=payload.password,
    )


@router.get("/get")
def get_org(organization_name: str = Query(...)):
    return service.get_organization(organization_name)


@router.put("/update")
def update_org(payload: OrgUpdateRequest):
    return service.update_organization(
        organization_name=payload.organization_name,
        email=payload.email,
        password=payload.password,
    )


@router.delete("/delete")
def delete_org(
    payload: OrgDeleteRequest = Body(...),
    current_admin=Depends(get_current_admin),
):
    admin_id = current_admin["admin_id"]
    return service.delete_organization(
        organization_name=payload.organization_name,
        admin_id=admin_id
    )
