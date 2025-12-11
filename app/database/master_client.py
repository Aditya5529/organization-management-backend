from pymongo import MongoClient
from app.config import MONGO_URI, MASTER_DB_NAME

client = MongoClient(MONGO_URI)
master_db = client[MASTER_DB_NAME]

organizations_col = master_db["organizations"]
admins_col = master_db["admins"]
