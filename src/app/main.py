from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.config import settings
from src.app.api.v1.router import api_router

def create_application() -> FastAPI:
    """
    Application Factory to create and configure the FastAPI app.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Microservice for rendering code (HTML/Mermaid) to images via Playwright.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 1. Middleware (CORS - Allow all for now, restrict in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Include Routers
    # This mounts the routes defined in api/v1/router.py
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # 3. Health Check (Simple endpoint to verify app is running)
    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "service": "render-engine"}

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    # This allows running the file directly for debugging
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)