from src.app.engines.html_playwright import HtmlPlaywrightEngine
from src.app.factories.engine_factory import EngineFactory
from src.app.schemas.requests import EngineType
from src.app.services.generator_service import GeneratorService
from src.app.engines.mermaid_playwright import MermaidPlaywrightEngine

# This file acts as a manual Dependency Injection (DI) container.
# In a larger application, a framework like `dependency-injector` might be
# used, but for this scale, manual instantiation is clear and effective.


# --- Singleton Instances ---

# 1. Create a singleton instance of the HTML engine.
#    If the engine had dependencies (like API keys), they would be
#    configured and injected here.
html_playwright_engine = HtmlPlaywrightEngine()
mermaid_engine = MermaidPlaywrightEngine()


# 2. Create a singleton instance of the EngineFactory.
engine_factory = EngineFactory()


# 3. Register the concrete engine implementations with the factory.
#    This is the central point for adding new rendering capabilities.
engine_factory.register_engine(EngineType.HTML, html_playwright_engine)
# Future engines would be registered here as well:
# from .engines.mermaid_cli import MermaidCliEngine
# mermaid_engine = MermaidCliEngine()
# engine_factory.register_engine(EngineType.MERMAID, mermaid_engine)
engine_factory.register_engine(EngineType.MERMAID, mermaid_engine)

# 4. Create a singleton instance of the GeneratorService, injecting its
#    dependency (the factory).
generator_service = GeneratorService(engine_factory=engine_factory)


# --- Dependency Provider Functions ---

# These functions are used by FastAPI's `Depends` system to inject the
# created singletons into the API endpoint handlers.


def get_generator_service() -> GeneratorService:
    """FastAPI dependency provider for the GeneratorService."""
    return generator_service
