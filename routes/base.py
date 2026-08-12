from fastapi import  APIRouter
import os

base_router = APIRouter()


@base_router.get("/health")
def health():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "message":"Application is running successfully",
        "app_name":app_name,
        "app_version":app_version
    }