from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EngineType(str, Enum):
    HTML = "html"
    MERMAID = "mermaid"
    AI = "ai"
    KOKORRO_TTS = "kokorro"


class RenderOptions(BaseModel):
    width: int = Field(1024, description="The width of the output image in pixels.")
    height: int = Field(768, description="The height of the output image in pixels.")
    scale_factor: float = Field(1.0, description="The device scale factor for HiDPI rendering.")
    omit_background: bool = Field(False, description="If True, removes the default white background for transparency.")
    tight_crop: bool = Field(True, description="If True, crops the image to the content content. If False, keeps the full viewport dimensions.")
    # --- Audio Options ---
    voice: str = Field("af_heart", description="Voice ID for Kokoro TTS (e.g., 'af_heart', 'am_adam').")
    speed: float = Field(1.0, description="Audio playback speed (default: 1.0).")


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
