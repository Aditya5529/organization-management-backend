from bson import ObjectId
from fastapi import HTTPException

from app.database.master_client import organizations_col, admins_col
from app.database.tenant_client import tenant_db, get_org_collection_name
from app.utils.password_handler import hash_password


class OrganizationService:
    def create_organization(self, organization_name: str, email: str, password: str) -> dict:
        existing = organizations_col.find_one({"organization_name": organization_name})
        if existing:
            raise HTTPException(status_code=400, detail="Organization already exists")

        collection_name = get_org_collection_name(organization_name)

        # Create dynamic collection
        # Create dynamic collection only if it does not already exist
        if collection_name not in tenant_db.list_collection_names():
            tenant_db.create_collection(collection_name)


        # Create admin user
        admin_doc = {
            "email": email,
            "password": hash_password(password),
            "organization_name": organization_name,
        }
        admin_result = admins_col.insert_one(admin_doc)

        org_doc = {
            "organization_name": organization_name,
            "collection_name": collection_name,
            "admin_id": admin_result.inserted_id,
            "connection_details": {
                "db": tenant_db.name,
                "collection": collection_name,
            },
        }
        organizations_col.insert_one(org_doc)

        return {
            "organization_name": organization_name,
            "collection_name": collection_name,
            "admin_id": str(admin_result.inserted_id),
        }

    def get_organization(self, organization_name: str) -> dict:
        org = organizations_col.find_one({"organization_name": organization_name})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        return {
            "organization_name": org["organization_name"],
            "collection_name": org["collection_name"],
            "admin_id": str(org["admin_id"]),
            "connection_details": org.get("connection_details", {}),
        }

    def update_organization(self, organization_name: str, email: str, password: str) -> dict:
        org = organizations_col.find_one({"organization_name": organization_name})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        old_collection = org["collection_name"]
        new_collection = get_org_collection_name(organization_name + "_updated")

        # Create new collection and migrate data
        if new_collection not in tenant_db.list_collection_names():
            tenant_db.create_collection(new_collection)

        old_col = tenant_db[old_collection]
        new_col = tenant_db[new_collection]

        docs = list(old_col.find())
        if docs:
            for d in docs:
                d.pop("_id", None)
            new_col.insert_many(docs)

        # Update admin info (email + password)
        admins_col.update_many(
            {"organization_name": organization_name},
            {
                "$set": {
                    "email": email,
                    "password": hash_password(password),
                }
            },
        )

        organizations_col.update_one(
            {"_id": org["_id"]},
            {
                "$set": {
                    "collection_name": new_collection,
                    "connection_details": {
                        "db": tenant_db.name,
                        "collection": new_collection,
                    },
                }
            },
        )

        return {
            "message": "Organization updated and data migrated",
            "organization_name": organization_name,
            "collection_name": new_collection,
        }

    def delete_organization(self, organization_name: str, admin_id: str) -> dict:
        org = organizations_col.find_one({"organization_name": organization_name})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        if str(org["admin_id"]) != admin_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this organization")

        # Drop tenant collection
        collection_name = org["collection_name"]
        tenant_db.drop_collection(collection_name)

        # Delete admin(s) and org metadata
        admins_col.delete_many({"organization_name": organization_name})
        organizations_col.delete_one({"_id": org["_id"]})

        return {"message": "Organization deleted successfully"}
