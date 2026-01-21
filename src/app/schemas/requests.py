from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EngineType(str, Enum):
    HTML = "html"
    MERMAID = "mermaid"
    AI = "ai"


class RenderOptions(BaseModel):
    width: int = Field(1024, description="The width of the output image in pixels.")
    height: int = Field(768, description="The height of the output image in pixels.")
    scale_factor: float = Field(1.0, description="The device scale factor for HiDPI rendering.")


class GenerateRequest(BaseModel):
    engine_type: EngineType = Field(
        ...,
        description="The rendering engine to use.",
        examples=[EngineType.HTML],
    )
    source_code: str = Field(
        ...,
        description="The source code, text, or prompt to be rendered into an image.",
        examples=["<h1>Hello, World!</h1>"],
    )
    options: RenderOptions = Field(
        default_factory=RenderOptions,
        description="Fine-tuning parameters for the rendering process.",
    )
