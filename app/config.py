import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MASTER_DB_NAME = os.getenv("MASTER_DB_NAME", "master_db")
TENANT_DB_NAME = os.getenv("TENANT_DB_NAME", "tenant_db")

JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", "60"))


def get_jwt_exp_delta() -> timedelta:
    return timedelta(minutes=JWT_EXP_MINUTES)
