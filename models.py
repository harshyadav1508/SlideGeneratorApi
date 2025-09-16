# src/models.py
from pydantic import BaseModel, Field
from enum import Enum # --- NEW: Import Enum ---

# --- NEW: Create an Enum for the allowed aspect ratios ---
class AspectRatio(str, Enum):
    widescreen = "16:9"
    standard = "4:3"

class PresentationRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The topic or subject of the presentation."
    )
    num_slides: int = Field(
        default=5,
        ge=1,
        le=20,
        description="The desired number of slides, between 1 and 20."
    )
    # --- NEW: Add the optional aspect_ratio field with a default value ---
    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.widescreen,
        description="The aspect ratio for the presentation slides."
    )