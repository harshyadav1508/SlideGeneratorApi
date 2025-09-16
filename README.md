Of course. Here is the complete documentation formatted as a `README.md` file. You can copy the entire content below and paste it directly into your `README.md` file on GitHub.

-----

# Slide Generator API

## Overview

This project is a Python-based backend application that generates customizable presentation slides on any topic. It leverages a Large Language Model (Google's Gemini) for content creation and provides a robust, asynchronous API built with FastAPI. The final output is a downloadable Microsoft PowerPoint (`.pptx`) file.

This application fulfills all core requirements of the take-home assignment, including AI content generation, multiple slide layouts, custom styling, and `.pptx` export. It also implements several stretch goals such as request/response validation, error handling, rate limiting, caching, and efficient handling of concurrent requests.

**Key Technologies:**

  * **Backend:** FastAPI
  * **AI Content Generation:** Google Gemini API (`google-generativeai`)
  * **Presentation Generation:** `python-pptx`
  * **API Specification:** OpenAPI (via FastAPI's automatic docs)
  * **Concurrency:** `asyncio`

## Features

  * **AI-Powered Content:** Generates relevant slide content for any given topic using the Gemini LLM.
  * **Customizable Presentations:**
      * Supports a variable number of slides (from 1 to 20).
      * Handles multiple aspect ratios (16:9 Widescreen and 4:3 Standard).
      * Uses custom templates for consistent styling, themes, fonts, and colors.
  * **Multiple Slide Layouts:** Supports title slides, bullet point lists, and two-column content layouts.
  * **Formatted Content:** Intelligently parses markdown (`**bold**`, `__underline__`) from the LLM to apply rich text formatting in the final presentation.
  * **Robust API:**
      * Asynchronous architecture to handle multiple simultaneous requests efficiently.
      * Built-in request validation for all parameters.
      * Graceful error handling for API failures or invalid content.
      * IP-based rate limiting to prevent abuse.
  * **Performance Optimized:**
      * In-memory caching for LLM responses to provide near-instantaneous results for repeated requests and reduce API costs.
      * Fully asynchronous request handling to prevent blocking and maximize throughput.

## Setup Instructions

Follow these steps to set up and run the project locally.

### Prerequisites

  * Python 3.10+
  * `pip` and `venv` (usually included with Python)
  * A Google Gemini API Key.

### Step-by-Step Guide

1.  **Clone the Repository**

    ```bash
    git clone https://github.dev/harshyadav1508/SlideGeneratorApi
    cd https://github.dev/harshyadav1508/SlideGeneratorApi
    ```

2.  **Create and Activate a Virtual Environment**

      * **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
      * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies**
    A `requirements.txt` file should be included. Install all necessary packages with:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**

      * Create a file named `.env` in the root directory of the project.
      * Add your Gemini API key to this file:
        ```env
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

5.  **Prepare Presentation Templates**

      * This project uses separate templates for different aspect ratios to ensure correct formatting.
      * Create two PowerPoint template files in the project's root directory:
          * **`template_16_9.pptx`**: A presentation file saved with a 16:9 (Widescreen) aspect ratio.
          * **`template_4_3.pptx`**: A presentation file saved with a 4:3 (Standard) aspect ratio.
      * You can customize the design, colors, and fonts within these templates using PowerPoint's Slide Master view.

6.  **Run the Application**

      * Use Uvicorn to run the FastAPI server:
        ```bash
        uvicorn src.main:app --reload
        ```
      * The `--reload` flag enables hot-reloading for development.

7.  **Access the API**

      * The application will be running at `http://127.0.0.1:8000`.
      * For interactive API documentation, open your browser and navigate to **`http://127.0.0.1:8000/docs`**.

## API Documentation

The API provides one primary endpoint for generating presentations.

### Endpoint: `POST /generate`

This endpoint generates a presentation based on the provided topic and parameters and returns it as a `.pptx` file.

#### Request Body

The request body must be a JSON object with the following structure:

```json
{
  "topic": "The History of Artificial Intelligence",
  "num_slides": 7,
  "aspect_ratio": "16:9"
}
```

**Fields:**

  * `topic` (string, **required**): The subject of the presentation. Must be between 3 and 100 characters.
  * `num_slides` (integer, *optional*, default: 5): The desired number of slides. Must be between 1 and 20.
  * `aspect_ratio` (string, *optional*, default: "16:9"): The aspect ratio of the slides. Allowed values are `"16:9"` or `"4:3"`.

#### Responses

  * **`200 OK` (Success)**

      * **Content-Type:** `application/vnd.openxmlformats-officedocument.presentationml.presentation`
      * **Body:** The binary content of the generated `.pptx` file.

  * **`422 Unprocessable Entity` (Validation Error)**

      * Returned if the request body fails validation (e.g., `num_slides` is 25, or `topic` is missing). The response body will contain details about the validation error.

  * **`429 Too Many Requests` (Rate Limit Exceeded)**

      * Returned if the client exceeds the rate limit of 5 requests per minute from a single IP address.

  * **`500 Internal Server Error` (Server Error)**

      * Returned if an unexpected error occurs on the server, such as a failure to communicate with the Gemini API or an error during file generation. The response body will contain an error detail message.

#### Example `curl` Request

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
-H "Content-Type: application/json" \
-d '{"topic": "The Moons of Jupiter", "num_slides": 5, "aspect_ratio": "16:9"}' \
--output jupiter_moons.pptx
```

## Source Code Documentation (Project Structure)

The source code is organized into a `src` directory with a clear separation of concerns.

  * `src/`
      * `main.py`: The entry point of the application. Defines the FastAPI app, the `/generate` endpoint, rate limiting, and the main request/response flow.
      * `services.py`: Contains the core business logic.
          * `LLMService`: Handles all interaction with the Google Gemini API, including prompt engineering, content generation, and caching.
          * `SlideBuilderService`: Handles the creation of the `.pptx` file using the `python-pptx` library, including template selection, slide creation, and text formatting.
      * `models.py`: Defines the Pydantic models used for API request body validation (`PresentationRequest`).
      * `config.py`: Handles loading environment variables, such as the `GOOGLE_API_KEY`.
  * `generated_presentations/`: A directory where the output `.pptx` files are temporarily stored before being sent to the client.
  * `template_16_9.pptx` & `template_4_3.pptx`: The PowerPoint template files that define the visual styling for the presentations.
  * `.env`: A local file (not committed to Git) for storing secret keys.
  * `requirements.txt`: A list of all Python dependencies for the project.