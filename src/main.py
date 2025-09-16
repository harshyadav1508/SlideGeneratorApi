# src/main.py
import os
import uuid
import asyncio
import logging  # --- LOGGING: Import the logging module ---
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse

# Import slowapi components
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .models import PresentationRequest
from .services import LLMService, SlideBuilderService

# --- LOGGING: Set up basic configuration for logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Initialize the Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Slide Generator API",
    description="An API to generate presentation slides on any topic using AI."
)

# Add the limiter to the app state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Instantiate our services
llm_service = LLMService()
slide_builder_service = SlideBuilderService()

# Ensure the output directory exists
OUTPUT_DIR = "generated_presentations"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/generate", response_class=FileResponse)
@limiter.limit("5/minute")
async def generate_presentation(request: Request, presentation_request: PresentationRequest):
    """
    Accepts a topic and number of slides, generates a .pptx file, and returns it.
    """
    logger.info(f"Received request for topic: '{presentation_request.topic}'")

    # Step 1: Generate content using the LLM Service
    content_data = await llm_service.generate_slides_content(
        presentation_request.topic, presentation_request.num_slides
    )

    if "error" in content_data:
        logger.error(f"Error from LLM Service: {content_data.get('details')}")
        raise HTTPException(status_code=500, detail=content_data["error"])

    if not content_data or "slides" not in content_data:
        logger.error("LLM Service returned invalid or empty content.")
        raise HTTPException(status_code=500, detail="Failed to generate valid slide content.")

    # Step 2: Build the .pptx file using the Slide Builder Service
    try:
        logger.info("Starting presentation generation.")
        unique_filename = f"{uuid.uuid4()}.pptx"
        output_path = os.path.join(OUTPUT_DIR, unique_filename)

        await asyncio.to_thread(
            slide_builder_service.create_presentation,
            content_data,
            output_path,
            presentation_request.aspect_ratio.value
        )
        logger.info(f"Successfully created presentation: {output_path}")
    except Exception as e:
        logger.error(f"Failed to create presentation file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create presentation file: {e}")

    # Step 3: Return the generated file
    return FileResponse(
        path=output_path,
        media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        filename=f"{presentation_request.topic.replace(' ', '_')}_presentation.pptx"
    )


@app.get("/")
def read_root():
    return {"message": "Welcome to the Slide Generator API. Go to /docs to see the API documentation."}