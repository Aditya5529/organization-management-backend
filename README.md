# Organization Management Backend – FastAPI (Assignment Solution)

Backend implementation for the Organization Management Service as described in the assignment PDF.
This service allows creation, update, retrieval, and deletion of organizations along with admin authentication using JWT, and supports multi-tenant MongoDB collections.

## 🚀 Features Implemented
Organization APIs

Create Organization

Get Organization Details

Update Organization + Dynamic Collection Migration

Delete Organization + Authorization Required

Admin Authentication

Admin login using email + password

Passwords stored securely using bcrypt hashing

JWT-based authentication for protected endpoints

Multi-Tenant Support

Each organization gets its own MongoDB collection:

org_<organization_name>

Technology Stack

FastAPI

Python 3.11

MongoDB

PyMongo

JWT (python-jose)

Passlib bcrypt

## 📁 Project Structure
backend-assignment/
│
├── app/
│   ├── main.py
│   ├── database/
│   │   ├── master_client.py
│   │   ├── tenant_client.py
│   ├── routes/
│   │   ├── org_routes.py
│   │   ├── auth_routes.py
│   ├── services/
│   │   ├── org_service.py
│   │   ├── auth_service.py
│   ├── schemas/
│   │   ├── org_schema.py
│   │   ├── admin_schema.py
│   ├── utils/
│   │   ├── jwt_handler.py
│   │   ├── password_handler.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore

## ⚙️ Setup Instructions
### 1️⃣ Clone Repository
git clone <your-repo-url>
cd backend-assignment

2️⃣ Create Virtual Environment
python -m venv .venv


Activate:

Windows:
.venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create .env file:

MONGO_URL=mongodb://localhost:27017
JWT_SECRET=mysecret


You may customize the secret as needed.

5️⃣ Start MongoDB

Ensure MongoDB server is running at:

mongodb://localhost:27017


If using MongoDB Compass, no extra steps needed.

6️⃣ Run the Application
uvicorn app.main:app --reload


Swagger Documentation:

http://127.0.0.1:8000/docs

## 🔐 Authentication Workflow
### Admin Login
POST /admin/login


Body:

{
  "email": "admin@org.com",
  "password": "StrongPassword123"
}


Response:

{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}

### Authorize in Swagger

Click Authorize → Paste:

Bearer <your-token>

## 🧪 API Endpoints
### Create Organization
POST /org/create


Request:

{
  "organization_name": "TechNova",
  "email": "admin@technova.com",
  "password": "StrongPass123"
}

### Get Organization
GET /org/get?organization_name=TechNova

### Update Organization
PUT /org/update


Request:

{
  "organization_name": "TechNova",
  "email": "newadmin@technova.com",
  "password": "NewPass123"
}

### Delete Organization (JWT Protected)
DELETE /org/delete


Request:

{
  "organization_name": "TechNova"
}


Requires:

Authorization: Bearer <token>

## 🛠 MongoDB Collections Created Automatically
Master DB:
admins
organizations

Tenant DB:
org_<organization_name>   e.g., org_technova


On update → new collection is created:

org_<organization_name>_updated

## 🧪 Testing With cURL
Login:
curl -X POST http://127.0.0.1:8000/admin/login ^
-H "Content-Type: application/json" ^
-d "{\"email\":\"admin@technova.com\", \"password\": \"StrongPass123\"}"

Delete Organization:
curl -X DELETE http://127.0.0.1:8000/org/delete ^
-H "Authorization: Bearer <token>" ^
-H "Content-Type: application/json" ^
-d "{\"organization_name\":\"TechNova\"}"

Author
Aditya Gupta
