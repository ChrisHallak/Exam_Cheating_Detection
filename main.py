from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(".env")

from routes.base import base_router
from routes.frame_analysis_routes import  frame_analysis_router

app = FastAPI()

app.include_router(base_router)
app.include_router(frame_analysis_router)

