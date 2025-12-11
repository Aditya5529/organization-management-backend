from pydantic import BaseModel, EmailStr


class OrgCreateRequest(BaseModel):
    organization_name: str
    email: EmailStr
    password: str


class OrgUpdateRequest(BaseModel):
    organization_name: str
    email: EmailStr
    password: str


class OrgDeleteRequest(BaseModel):
    organization_name: str


class OrgResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_id: str | None = None
