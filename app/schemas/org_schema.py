from pydantic import BaseModel, EmailStr


class OrgCreateRequest(BaseModel):
    organization_name: str
    email: EmailStr
    password: str


class OrgUpdateCredentialsRequest(BaseModel):
    email: EmailStr
    password: str





class OrgResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_id: str | None = None
