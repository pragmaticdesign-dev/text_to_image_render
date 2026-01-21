from fastapi import APIRouter
from src.app.api.v1.endpoints import generation

api_router = APIRouter()

# Register the generation endpoint
# This connects the code you wrote in 'generation.py' to the main app
api_router.include_router(generation.router)