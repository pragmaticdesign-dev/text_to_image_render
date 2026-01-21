from typing import Dict

from src.app.core.interfaces.engine_contract import BaseRenderingEngine
from src.app.schemas.requests import EngineType


class EngineFactory:
    """
    The EngineFactory is a central registry for all available rendering
    engines.

    It holds a map of engine types (e.g., "html") to their corresponding
    concrete engine instances. This decouples the service layer from the
    concrete engine implementations, allowing for easy extension with new
    engine types without modifying the core service logic.
    """

    def __init__(self):
        self._registry: Dict[EngineType, BaseRenderingEngine] = {}

    def register_engine(
        self, engine_type: EngineType, engine_instance: BaseRenderingEngine
    ):
        """
        Adds a concrete engine instance to the factory's registry.

        This method is typically called at application startup by the
        dependency
        injection container to populate the factory.

        Args:
            engine_type: The enum key (e.g., EngineType.HTML).
            engine_instance: An instance of a class that implements the
                             BaseRenderingEngine interface.
        """
        self._registry[engine_type] = engine_instance

    def get_engine(self, engine_type: EngineType) -> BaseRenderingEngine:
        """
        Retrieves a rendering engine from the registry.

        Args:
            engine_type: The enum key for the desired engine.

        Returns:
            The corresponding engine instance.

        Raises:
            ValueError: If the requested engine type has not been registered.
        """
        engine = self._registry.get(engine_type)
        if not engine:
            raise ValueError(f"Engine for type '{engine_type.value}' not found.")
        return engine
