from abc import ABC, abstractmethod

from src.app.schemas.requests import RenderOptions


class BaseRenderingEngine(ABC):
    """
    Abstract base class (Interface) for a rendering engine.

    This class defines the contract that all concrete rendering engines must
    adhere to. It ensures that the service layer can interact with any engine
in
    a uniform way.
    """

    @abstractmethod
    async def render(self, source_code: str, options: RenderOptions) -> bytes:
        """
        Renders the given source code into image bytes.

        This is the core method for any rendering engine. It must be
        implemented by all concrete subclasses.

        Args:
            source_code: The raw string payload to be rendered (e.g., HTML
                         code, Mermaid syntax, AI prompt).
            options: A Pydantic model containing rendering parameters like
                     width and height.

        Returns:
            The raw bytes of the generated image (e.g., in PNG, JPEG format).

        Raises:
            NotImplementedError: If the method is not implemented by the
                                 subclass.
        """
        raise NotImplementedError
