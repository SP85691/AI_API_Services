from fastapi import APIRouter, Depends, HTTPException

service_routes = APIRouter(prefix="/api/services")

@service_routes.get("/")
def get_user():
    return {"message": "Hello User"}