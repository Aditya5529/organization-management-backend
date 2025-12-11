from pymongo import MongoClient
from app.config import MONGO_URI, TENANT_DB_NAME

client = MongoClient(MONGO_URI)
tenant_db = client[TENANT_DB_NAME]


def get_org_collection_name(org_name: str) -> str:
    # normalize org name
    normalized = org_name.strip().lower().replace(" ", "_")
    return f"org_{normalized}"
