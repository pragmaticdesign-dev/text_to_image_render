from fastapi import APIRouter, Depends, Response

from src.app.schemas.requests import GenerateRequest
from src.app.services.generator_service import GeneratorService

# The container will be responsible for creating and injecting the service.
# We will define a dependency getter for it in the container file.
# For now, we define the router and will wire it up later.
from src.app.core.container import get_generator_service

router = APIRouter(prefix="/v1", tags=["Image Generation"])


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
async def generate_image(
    request: GenerateRequest,
    service: GeneratorService = Depends(get_generator_service),
) -> Response:
    """
    Generates and returns an image based on a source input.

    This endpoint accepts a source code payload (e.g., HTML, Mermaid) and
    rendering options, then returns the resulting image.

    - **engine_type**: Specify the rendering engine ('html', 'mermaid', etc.).
    - **source_code**: The code or text to render.
    - **options**: Parameters like width, height, and scale factor.
    """
    image_bytes = await service.process_request(request)
    return Response(content=image_bytes, media_type="image/png")
