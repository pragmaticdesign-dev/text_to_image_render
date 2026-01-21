from fastapi import APIRouter, Depends, Response

from src.app.schemas.requests import GenerateRequest , EngineType
from src.app.services.generator_service import GeneratorService
from src.app.core.container import get_generator_service

# FIX: Removed prefix="/v1" because main.py already handles the /api/v1 part
router = APIRouter(tags=["Media Generation"]) 

@router.post(
    "/generate",
    summary="Render an image from source code",
    response_description="A PNG image file.",
    responses={
        200: {"content": {"image/png": {}}},
        400: {"description": "Invalid input or unsupported engine."},
        500: {"description": "Internal server error during rendering."},
    },
)
async def generate_media(
    request: GenerateRequest,
    service: GeneratorService = Depends(get_generator_service),
) -> Response:
    image_bytes = await service.process_request(request)
    media_type = "audio/mpeg" if request.engine_type == EngineType.KOKORRO_TTS else "image/png"
    return Response(content=image_bytes, media_type=media_type)