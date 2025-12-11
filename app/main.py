from fastapi import FastAPI
from app.routes import org_routes, auth_routes

app = FastAPI(
    title="Organization Management Service",
    version="1.0.0",
)

app.include_router(org_routes.router)
app.include_router(auth_routes.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
