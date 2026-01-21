from fastapi import APIRouter
from src.app.api.v1.endpoints import generation

api_router = APIRouter()

# Register the generation endpoint
# Note: In generation.py, you defined prefix="/v1". 
# Usually, we handle versioning here, but since it's already there, 
# we just include it.
api_router.include_router(generation.router)