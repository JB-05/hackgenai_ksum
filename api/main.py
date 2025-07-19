from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any
import json
from datetime import datetime

# Import our modules
from .models import StoryRequest, SceneBreakdownResponse, ImageGenerationRequest, ImageGenerationResponse, VoiceGenerationRequest, VoiceGenerationResponse
from .modules.story_to_scenes import story_processor
from .modules.generate_image import image_generator
from .modules.generate_voice import voice_generator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Story-to-Video Generator API",
    description="AI-powered story transformation into multimedia presentations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SAVE_OUTPUTS_DIR = os.getenv("SAVE_OUTPUTS_DIR", "save_outputs")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB

# Ensure output directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        SAVE_OUTPUTS_DIR,
        f"{SAVE_OUTPUTS_DIR}/scenes",
        f"{SAVE_OUTPUTS_DIR}/images", 
        f"{SAVE_OUTPUTS_DIR}/audio",
        f"{SAVE_OUTPUTS_DIR}/music",
        f"{SAVE_OUTPUTS_DIR}/videos"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Initialize directories on startup
ensure_directories()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Story-to-Video Generator API")
    ensure_directories()
    logger.info("Directories initialized successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Story-to-Video Generator API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "directories_ready": all(
            os.path.exists(f"{SAVE_OUTPUTS_DIR}/{subdir}")
            for subdir in ["scenes", "images", "audio", "music", "videos"]
        ),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/endpoints")
async def list_endpoints():
    """List all available API endpoints"""
    return {
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Health check"},
            {"path": "/health", "method": "GET", "description": "Detailed health check"},
            {"path": "/api/endpoints", "method": "GET", "description": "List all endpoints"},
            {"path": "/story-to-scenes", "method": "POST", "description": "Break story into scenes"},
            {"path": "/generate-image", "method": "POST", "description": "Generate image for scene"},
            {"path": "/generate-voice", "method": "POST", "description": "Generate voice narration"},
            {"path": "/generate-music", "method": "POST", "description": "Generate background music"},
            {"path": "/create-slideshow", "method": "POST", "description": "Create final video"},
            {"path": "/files/{file_type}/{filename}", "method": "GET", "description": "Download generated files"}
        ]
    }

@app.get("/files/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """Download generated files"""
    allowed_types = ["scenes", "images", "audio", "music", "videos"]
    
    if file_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_types}")
    
    file_path = f"{SAVE_OUTPUTS_DIR}/{file_type}/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=filename)

@app.post("/story-to-scenes", response_model=SceneBreakdownResponse)
async def break_story_to_scenes(request: StoryRequest):
    """Break a story down into scenes using GPT-4"""
    try:
        logger.info(f"Received story breakdown request: {request.title or 'Untitled'}")
        
        # Process the story
        response = await story_processor.process_story(request)
        
        logger.info(f"Story breakdown completed: {response.total_scenes} scenes")
        return response
        
    except Exception as e:
        logger.error(f"Error in story breakdown endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process story: {str(e)}")

@app.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Generate an image for a scene using DALL-E 3"""
    try:
        logger.info(f"Received image generation request for scene {request.scene_number}")
        
        # Generate the image
        response = await image_generator.generate_image(request)
        
        logger.info(f"Image generation completed for scene {request.scene_number}")
        return response
        
    except Exception as e:
        logger.error(f"Error in image generation endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {str(e)}")

@app.post("/generate-images-for-scenes")
async def generate_images_for_scenes(scenes_data: list):
    """Generate images for multiple scenes"""
    try:
        logger.info(f"Received batch image generation request for {len(scenes_data)} scenes")
        
        # Generate images for all scenes
        results = await image_generator.generate_images_for_scenes(scenes_data)
        
        logger.info(f"Batch image generation completed: {len(results)} images generated")
        return {
            "success": True,
            "images_generated": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in batch image generation endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate images: {str(e)}")

@app.post("/generate-voice", response_model=VoiceGenerationResponse)
async def generate_voice(request: VoiceGenerationRequest):
    """Generate voice narration using ElevenLabs"""
    try:
        logger.info(f"Received voice generation request: {len(request.text)} characters")
        
        # Generate voice
        response = await voice_generator.generate_voice(request)
        
        logger.info(f"Voice generation completed")
        return response
        
    except Exception as e:
        logger.error(f"Error in voice generation endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate voice: {str(e)}")

@app.post("/generate-story-narration")
async def generate_story_narration(story_data: dict):
    """Generate narration for an entire story"""
    try:
        story_text = story_data.get("story_text", "")
        voice_type = story_data.get("voice_type", "narrator")
        
        logger.info(f"Received story narration request: {len(story_text)} characters")
        
        # Generate narration
        response = await voice_generator.generate_narration_for_story(story_text, voice_type)
        
        logger.info(f"Story narration completed")
        return response
        
    except Exception as e:
        logger.error(f"Error in story narration endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate story narration: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    ) 