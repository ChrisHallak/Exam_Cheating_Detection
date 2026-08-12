from fastapi import  APIRouter

base_router = APIRouter()


@base_router.get("/health")
def health():
    return {
        "message":"Application is running successfully"
    }