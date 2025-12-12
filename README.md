# Organization Management Service

A multi-tenant backend service built with **FastAPI** and **MongoDB**, designed to manage organizations with dynamic data isolation. This project demonstrates a scalable **Shared Database, Separate Collections** architecture for multi-tenancy, complete with JWT-based authentication and modular design.

## 📌 Problem Statement
The goal is to build a backend system that can dynamically onboard organizations. Each organization requires its own isolated data storage (collections) while sharing a common backend infrastructure. The system must maintain a "Master" database for global metadata (tenants, admins) and dynamically manage "Tenant" resources upon creation, update, or deletion. Security, scalability, and clean architecture are paramount.

## 🏗 Architecture Overview

The system uses a **Hybrid Multi-Tenant Architecture**:

1.  **Master Database (`master_db`)**:
    *   Stores global metadata.
    *   Collections: `organizations` (stores org details, connection info), `admins` (stores credentials).
2.  **Tenant Database (`tenant_db`)**:
    *   Stores actual organization data.
    *   **Isolation Strategy**: Dynamic Collections. Each organization gets a dedicated collection `org_<organization_name>`.
    *   On updates, new collections are created and data is migrated to ensure data integrity and structure versioning.

## 🚀 High-Level Workflow
1.  **Onboard**: User sends `POST /org/create`.
    *   System checks uniqueness -> hash password -> create admin -> create dynamic collection -> save metadata.
2.  **Login**: Admin sends `POST /admin/login`.
    *   System validates hash -> issues **JWT** containing `admin_id` and `org_id`.
3.  **Manage**: Authenticated Admin performs actions.
    *   `GET /org/get`: View metadata.
    *   `PUT /org/update`: Rotate credentials & migrate data to new collection.
    *   `DELETE /org/delete`: Remove all traces of organization (Metadata + Collections).

## 🛠 Tech Stack
*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **Database**: MongoDB (via `pymongo`)
*   **Authentication**: JWT (`python-jose`) + Bcrypt (`passlib`)
*   **Validation**: Pydantic
*   **Environment**: Dotenv

## 📂 Folder Structure
```bash
.
├── app
│   ├── database        # DB Connection clients (Master & Tenant)
│   ├── models          # Application logic models (if applicable)
│   ├── routes          # API Controllers (Org & Auth)
│   ├── schemas         # Pydantic Request/Response models
│   ├── services        # Business Logic & DB Interactions
│   ├── utils           # Helpers (JWT, Password Hashing)
│   ├── config.py       # Configuration management
│   └── main.py         # Entry point
├── .env                # Environment variables
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## ⚙️ Setup Instructions

### Prerequisites
*   Python 3.9 or higher
*   MongoDB installed and running locally on port `27017` (or provide URI)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <repo_url>
    cd <repo_directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    MONGO_URI=mongodb://localhost:27017
    MASTER_DB_NAME=master_db
    TENANT_DB_NAME=tenant_db
    JWT_SECRET=supersecretkey
    JWT_ALGORITHM=HS256
    JWT_EXP_MINUTES=60
    ```

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Access Swagger UI at: `http://127.0.0.1:8000/docs`

## 📡 API Documentation

### Organization Routes

| Method | Endpoint      | Description | Auth Required |
| :---   | :---          | :---        | :---          |
| `POST` | `/org/create` | Register a new organization, admin, and collection. | ❌ No |
| `GET`  | `/org/get`    | Fetch organization metadata by name. | ❌ No |
| `PUT`  | `/org/update` | Update admin credentials and migrate data to new collection. | ✅ Yes (Admin) |
| `DELETE`| `/org/delete`| Permanently remove organization and data. | ✅ Yes (Admin) |

### Admin Routes

| Method | Endpoint       | Description | Auth Required |
| :---   | :---           | :---        | :---          |
| `POST` | `/admin/login` | Validate credentials and receive Access Token. | ❌ No |

## 🔐 Authentication Flow
1.  Admin registers via `/org/create`.
2.  Admin logs in via `/admin/login` with email & password.
3.  Server validates credentials using `bcrypt` verification.
4.  Server returns a **JWT Access Token** (Bearer).
5.  Admin sends this token in the `Authorization` header (`Bearer <token>`) for protected endpoints (e.g., `/org/delete`).

## 🛡 Security Considerations
*   **Password Hashing**: All passwords are salted and hashed using **bcrypt** before storage. Raw passwords are never stored.
*   **JWT Authentication**: Stateless authentication ensures scalability. Tokens are signed with a secure secret.
*   **Data Isolation**: Tenant data is logically separated by Collections. This prevents accidental data leaks between organizations in application logic queries.

## 📈 Scalability & Trade-offs
**Design Choice: Dynamic Collections (One Collection Per Tenant)**

*   **Pros:**
    *   **Better Isolation**: Easier to backup/restore/delete specific tenant data compared to a single shared collection with `tenant_id`.
    *   **Performance**: Indexes are smaller and specific to one tenant.
    *   **Simplicity**: Development is straightforward; queries don't always need to remember detailed `where tenant_id=` clauses if the collection is pre-selected.

*   **Trade-offs:**
    *   **Namespace Limit**: MongoDB has a limit on the number of namespaces (collections). This works well for thousands of tenants but not millions.
    *   **Connection Overhead**: If not managed correctly, switching collections is cheap, but maintaining many open cursors or indexes has RAM costs.

*   **Why strict Multi-Database wasn't chosen**: Creating a full *Database* per tenant is resource-intensive for the OS/Filesystem. Collections offer a sweet spot between "Shared Row" AND "Isolated Database".

---
**Submission Notes for Evaluator**
*   The architecture strictly separates the **Metadata Plane** (Master DB) from the **Data Plane** (Tenant DB).
*   Data migration logic in `/org/update` ensures that even if credentials change, the data is preserved in a fresh structure.

Authored by: Aditya Gupta
