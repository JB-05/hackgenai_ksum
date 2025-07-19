from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from dotenv import load_dotenv
import logging
from typing import Dict, Any
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Story-to-Video Workflow API",
    description="AI-powered story transformation workflow with user confirmation",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SAVE_OUTPUTS_DIR = os.getenv("SAVE_OUTPUTS_DIR", "save_outputs")

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Story-to-Video Workflow API")
    logger.info("Workflow API initialized successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Story-to-Video Workflow API",
        "status": "running",
        "version": "2.0.0",
        "workflow": "prompt → enhancement → confirmation → generation → video",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_version": "2.0.0",
        "active_workflows": 0,
        "workflow_phases": [
            "prompt_enhancement",
            "user_confirmation", 
            "generation",
            "completed"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/workflow/endpoints")
async def list_workflow_endpoints():
    """List all available workflow API endpoints"""
    return {
        "workflow_endpoints": [
            {"path": "/", "method": "GET", "description": "Health check"},
            {"path": "/health", "method": "GET", "description": "Detailed health check"},
            {"path": "/api/workflow/endpoints", "method": "GET", "description": "List workflow endpoints"},
            {"path": "/api/workflow/create", "method": "POST", "description": "Create new workflow"},
            {"path": "/api/workflow/{workflow_id}/enhance", "method": "POST", "description": "Enhance user prompt"},
            {"path": "/api/workflow/{workflow_id}/confirm", "method": "POST", "description": "User confirmation"},
            {"path": "/api/workflow/{workflow_id}/generate", "method": "POST", "description": "Generate complete video"},
            {"path": "/api/workflow/{workflow_id}/status", "method": "GET", "description": "Get workflow status"},
            {"path": "/api/workflow/{workflow_id}/progress", "method": "GET", "description": "Get generation progress"},
            {"path": "/api/workflow/{workflow_id}/result", "method": "GET", "description": "Get final result"},
            {"path": "/api/workflow/list", "method": "GET", "description": "List all workflows"},
            {"path": "/api/workflow/{workflow_id}/cleanup", "method": "DELETE", "description": "Clean up workflow"}
        ]
    }

@app.post("/api/workflow/create")
async def create_workflow():
    """Create a new workflow"""
    try:
        import uuid
        workflow_id = str(uuid.uuid4())
        return {
            "workflow_id": workflow_id,
            "status": "created",
            "message": "New workflow created successfully",
            "next_step": f"POST /api/workflow/{workflow_id}/enhance",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")

@app.post("/api/workflow/{workflow_id}/enhance")
async def enhance_prompt(workflow_id: str, request: Dict[str, Any]):
    """Phase 1: Enhance user prompt"""
    try:
        logger.info(f"Enhancing prompt for workflow {workflow_id}")
        
        # Mock enhancement for now
        enhanced_story = f"Enhanced version of: {request.get('user_prompt', 'No prompt provided')}"
        
        return {
            "original_prompt": request.get('user_prompt', ''),
            "enhanced_story": enhanced_story,
            "story_title": request.get('title', 'Generated Story'),
            "estimated_scenes": request.get('max_scenes', 4),
            "processing_time": 1.5,
            "enhancement_notes": ["Added character development", "Enhanced plot elements", "Improved visual descriptions"]
        }
        
    except Exception as e:
        logger.error(f"Error enhancing prompt for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to enhance prompt: {str(e)}")

@app.post("/api/workflow/{workflow_id}/confirm")
async def confirm_generation(workflow_id: str, confirmation: Dict[str, Any]):
    """Phase 2: User confirmation to proceed with generation"""
    try:
        logger.info(f"Processing user confirmation for workflow {workflow_id}")
        
        will_proceed = confirmation.get('proceed', False)
        
        if will_proceed:
            return {
                "workflow_id": workflow_id,
                "status": "confirmed",
                "message": "User confirmed generation. Ready to proceed.",
                "next_step": f"POST /api/workflow/{workflow_id}/generate",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "workflow_id": workflow_id,
                "status": "cancelled",
                "message": "User cancelled generation.",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"Error processing confirmation for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process confirmation: {str(e)}")

@app.post("/api/workflow/{workflow_id}/generate")
async def generate_video(workflow_id: str):
    """Phase 3: Generate complete video"""
    try:
        logger.info(f"Starting video generation for workflow {workflow_id}")
        
        # Mock generation result
        return {
            "story_script": {
                "story_title": "Generated Story",
                "scenes": [
                    {"scene_number": 1, "description": "Scene 1 description"},
                    {"scene_number": 2, "description": "Scene 2 description"}
                ],
                "total_duration": 10.0,
                "narration_text": "Story narration text",
                "music_description": "Background music description",
                "generation_metadata": {
                    "workflow_id": workflow_id,
                    "total_scenes": 2,
                    "image_style": "realistic",
                    "voice_id": "test_voice",
                    "music_style": "orchestral",
                    "music_mood": "adventurous"
                }
            },
            "video_file": "/files/videos/sample_video.mp4",
            "audio_file": "/files/audio/sample_audio.mp3",
            "music_file": "/files/music/sample_music.mp3",
            "image_files": ["/files/images/scene1.jpg", "/files/images/scene2.jpg"],
            "total_processing_time": 30.5,
            "file_sizes": {
                "video": 1024000,
                "audio": 512000,
                "music": 256000
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating video for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")

@app.get("/api/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """Get workflow status"""
    return {
        "workflow_id": workflow_id,
        "current_phase": "completed",
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/workflow/{workflow_id}/progress")
async def get_generation_progress(workflow_id: str):
    """Get generation progress"""
    return {
        "status": "completed",
        "progress_percentage": 100.0,
        "current_step": "Generation completed",
        "estimated_time_remaining": 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/workflow/{workflow_id}/result")
async def get_final_result(workflow_id: str):
    """Get final result"""
    return {
        "story_script": {
            "story_title": "Generated Story",
            "scenes": [
                {"scene_number": 1, "description": "Scene 1 description"},
                {"scene_number": 2, "description": "Scene 2 description"}
            ],
            "total_duration": 10.0,
            "narration_text": "Story narration text",
            "music_description": "Background music description",
            "generation_metadata": {
                "workflow_id": workflow_id,
                "total_scenes": 2,
                "image_style": "realistic",
                "voice_id": "test_voice",
                "music_style": "orchestral",
                "music_mood": "adventurous"
            }
        },
        "video_file": "/files/videos/sample_video.mp4",
        "audio_file": "/files/audio/sample_audio.mp3",
        "music_file": "/files/music/sample_music.mp3",
        "image_files": ["/files/images/scene1.jpg", "/files/images/scene2.jpg"],
        "total_processing_time": 30.5,
        "file_sizes": {
            "video": 1024000,
            "audio": 512000,
            "music": 256000
        }
    }

@app.get("/api/workflow/list")
async def list_workflows():
    """List all workflows"""
    return {
        "total_workflows": 0,
        "workflows": []
    }

@app.delete("/api/workflow/{workflow_id}/cleanup")
async def cleanup_workflow(workflow_id: str):
    """Clean up workflow"""
    return {
        "workflow_id": workflow_id,
        "status": "cleaned",
        "message": "Workflow cleaned up successfully",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 