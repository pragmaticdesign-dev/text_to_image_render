from src.app.factories.engine_factory import EngineFactory
from src.app.schemas.requests import GenerateRequest


class GeneratorService:
    """
    The service layer responsible for orchestrating the image generation
    process.

    This class acts as the primary entry point for the business logic. It
    receives a validated request object, uses the EngineFactory to select the
    appropriate rendering engine, and then delegates the actual rendering work
    to that engine.
    """

    def __init__(self, engine_factory: EngineFactory):
        """
        Initializes the service with a dependency on the engine factory.

        Args:
            engine_factory: An instance of EngineFactory, provided via
                            dependency injection.
        """
        self._engine_factory = engine_factory

    async def process_request(self, request: GenerateRequest) -> bytes:
        """
        Processes an image generation request.

        1.  Retrieves the appropriate engine from the factory based on the
            request's `engine_type`.
        2.  Calls the engine's `render` method with the source code and
            options.
        3.  Returns the resulting image bytes.

        Args:
            request: A GenerateRequest Pydantic model containing all the
                     information for the rendering job.

        Returns:
            The raw bytes of the generated image.
        """
        # Select the correct engine using the factory
        engine = self._engine_factory.get_engine(request.engine_type)

        # Delegate the rendering task to the selected engine
        image_bytes = await engine.render(request.source_code, request.options)

        return image_bytes
