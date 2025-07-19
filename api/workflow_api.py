from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import uvicorn
from dotenv import load_dotenv
import logging
from typing import Dict, Any
from datetime import datetime
import mimetypes
import pathlib
import json

# Import our workflow modules
from .modules.workflow_manager  import (
    UserPromptRequest, EnhancedPromptResponse, UserConfirmationRequest,
    GenerationProgress, StoryScript, FinalVideoResponse, WorkflowStatus
)
from .modules.workflow_manager import get_workflow_manager

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

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:8501",  # Streamlit (if used)
        "http://127.0.0.1:8501",  # Alternative Streamlit
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Configuration
SAVE_OUTPUTS_DIR = os.getenv("SAVE_OUTPUTS_DIR", "save_outputs")

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

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.now()
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Story-to-Video Workflow API")
    ensure_directories()
    logger.info("Directories initialized successfully")
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
        "active_workflows": len(get_workflow_manager().active_workflows),
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
        workflow_id = get_workflow_manager().create_workflow()
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

@app.post("/api/workflow/{workflow_id}/enhance", response_model=EnhancedPromptResponse)
async def enhance_prompt(workflow_id: str, request: UserPromptRequest):
    """Phase 1: Enhance user prompt"""
    try:
        logger.info(f"Enhancing prompt for workflow {workflow_id}")
        
        # Enhance the prompt
        enhanced_response = await get_workflow_manager().enhance_prompt(workflow_id, request)
        
        logger.info(f"Prompt enhancement completed for workflow {workflow_id}")
        return enhanced_response
        
    except ValueError as e:
        logger.error(f"Workflow not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error enhancing prompt for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to enhance prompt: {str(e)}")

@app.post("/api/workflow/{workflow_id}/confirm")
async def confirm_generation(workflow_id: str, confirmation: UserConfirmationRequest):
    """Phase 2: User confirmation to proceed with generation"""
    try:
        logger.info(f"Processing user confirmation for workflow {workflow_id}")
        
        # Process user confirmation
        will_proceed = await get_workflow_manager().process_user_confirmation(workflow_id, confirmation)
        
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
        
    except ValueError as e:
        logger.error(f"Workflow not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing confirmation for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process confirmation: {str(e)}")

@app.post("/api/workflow/{workflow_id}/generate", response_model=FinalVideoResponse)
async def generate_video(workflow_id: str, background_tasks: BackgroundTasks):
    """Phase 3: Generate complete video (runs in background)"""
    try:
        logger.info(f"Starting video generation for workflow {workflow_id}")
        
        # Get workflow status
        workflow = get_workflow_manager().get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
        if workflow.current_phase != "generation":
            raise HTTPException(status_code=400, detail=f"Workflow is in phase '{workflow.current_phase}', not ready for generation")
        
        # Get the stored workflow data
        workflow_data = get_workflow_manager().workflow_data.get(workflow_id, {})
        enhanced_story = workflow_data.get("enhanced_story")
        story_title = workflow_data.get("story_title")
        max_scenes = workflow_data.get("max_scenes", 4)
        
        if not enhanced_story:
            raise HTTPException(status_code=400, detail="No enhanced story available. Please complete the enhancement phase first.")
        
        # Generate the complete video
        result = await get_workflow_manager().generate_complete_video(workflow_id, enhanced_story, story_title, max_scenes)
        
        logger.info(f"Video generation completed for workflow {workflow_id}")
        return result
        
    except ValueError as e:
        logger.error(f"Workflow not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating video for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")

@app.get("/api/workflow/{workflow_id}/status", response_model=WorkflowStatus)
async def get_workflow_status(workflow_id: str):
    """Get the current status of a workflow"""
    try:
        workflow = get_workflow_manager().get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
        return workflow
        
    except Exception as e:
        logger.error(f"Error getting workflow status for {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow status: {str(e)}")

@app.get("/api/workflow/{workflow_id}/progress")
async def get_generation_progress(workflow_id: str):
    """Get the current progress of video generation"""
    try:
        workflow = get_workflow_manager().get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
        if workflow.current_phase != "generation":
            return {
                "workflow_id": workflow_id,
                "phase": workflow.current_phase,
                "status": workflow.status,
                "message": f"Workflow is in {workflow.current_phase} phase"
            }
        
        if workflow.progress:
            return workflow.progress
        else:
            return {
                "workflow_id": workflow_id,
                "status": "unknown",
                "message": "No progress information available"
            }
        
    except Exception as e:
        logger.error(f"Error getting progress for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@app.get("/api/workflow/{workflow_id}/result", response_model=FinalVideoResponse)
async def get_final_result(workflow_id: str):
    """Get the final result of a completed workflow"""
    try:
        workflow = get_workflow_manager().get_workflow_status(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
        if workflow.current_phase != "completed":
            raise HTTPException(status_code=400, detail=f"Workflow is not completed. Current phase: {workflow.current_phase}")
        
        if not workflow.result:
            raise HTTPException(status_code=404, detail="No result available for this workflow")
        
        return workflow.result
        
    except Exception as e:
        logger.error(f"Error getting result for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get result: {str(e)}")

@app.get("/api/workflow/list")
async def list_workflows():
    """List all active workflows"""
    try:
        workflows = get_workflow_manager().list_workflows()
        return {
            "total_workflows": len(workflows),
            "workflows": [
                {
                    "workflow_id": w.workflow_id,
                    "current_phase": w.current_phase,
                    "status": w.status,
                    "created_at": w.created_at.isoformat(),
                    "updated_at": w.updated_at.isoformat()
                }
                for w in workflows
            ]
        }
        
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")

@app.delete("/api/workflow/{workflow_id}/cleanup")
async def cleanup_workflow(workflow_id: str):
    """Clean up a completed or failed workflow"""
    try:
        get_workflow_manager().cleanup_workflow(workflow_id)
        return {
            "workflow_id": workflow_id,
            "status": "cleaned_up",
            "message": "Workflow cleaned up successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup workflow: {str(e)}")

@app.get("/files/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """Download generated files with proper MIME types and headers"""
    try:
        logger.info(f"File download request: {file_type}/{filename}")
        
        # Validate file type
        allowed_types = ["scenes", "images", "audio", "music", "videos"]
        if file_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_types}")
        
        # Construct file path using pathlib for cross-platform compatibility
        file_path = pathlib.Path(SAVE_OUTPUTS_DIR) / file_type / filename
        
        # Convert to string for FileResponse
        file_path_str = str(file_path)
        
        logger.info(f"Looking for file: {file_path_str}")
        
        # Check if file exists
        if not file_path.exists():
            logger.error(f"File not found: {file_path_str}")
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
        
        # Get file size
        file_size = file_path.stat().st_size
        logger.info(f"File size: {file_size} bytes")
        
        # Determine MIME type based on file extension
        mime_type_map = {
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.json': 'application/json',
            '.txt': 'text/plain',
        }
        
        file_extension = pathlib.Path(filename).suffix.lower()
        mime_type = mime_type_map.get(file_extension, 'application/octet-stream')
        
        logger.info(f"Serving file: {filename} with MIME type: {mime_type}")
        
        # Return file with proper headers
        return FileResponse(
            path=file_path_str,
            filename=filename,
            media_type=mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(file_size),
                "Cache-Control": "no-cache",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving file {file_type}/{filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

@app.get("/test/generate-sample-files")
async def generate_sample_files():
    """Generate sample files for testing download functionality"""
    try:
        logger.info("Generating sample files for testing")
        
        # Ensure directories exist
        ensure_directories()
        
        # Generate sample video file
        video_content = b"Sample video content for testing\nThis is a placeholder video file.\n"
        video_path = pathlib.Path(SAVE_OUTPUTS_DIR) / "videos" / "sample_video.mp4"
        with open(video_path, 'wb') as f:
            f.write(video_content)
        
        # Generate sample audio file
        audio_content = b"Sample audio content for testing\nThis is a placeholder audio file.\n"
        audio_path = pathlib.Path(SAVE_OUTPUTS_DIR) / "audio" / "sample_audio.mp3"
        with open(audio_path, 'wb') as f:
            f.write(audio_content)
        
        # Generate sample music file
        music_content = b"Sample music content for testing\nThis is a placeholder music file.\n"
        music_path = pathlib.Path(SAVE_OUTPUTS_DIR) / "music" / "sample_music.mp3"
        with open(music_path, 'wb') as f:
            f.write(music_content)
        
        # Generate sample image file (simple text-based placeholder)
        image_content = b"Sample image content for testing\nThis is a placeholder image file.\n"
        image_path = pathlib.Path(SAVE_OUTPUTS_DIR) / "images" / "sample_image.png"
        with open(image_path, 'wb') as f:
            f.write(image_content)
        
        # Generate sample JSON file
        json_content = {
            "test": True,
            "message": "Sample JSON file for testing",
            "timestamp": datetime.now().isoformat(),
            "files": [
                "sample_video.mp4",
                "sample_audio.mp3", 
                "sample_music.mp3",
                "sample_image.png"
            ]
        }
        json_path = pathlib.Path(SAVE_OUTPUTS_DIR) / "scenes" / "sample_scenes.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
        
        logger.info("Sample files generated successfully")
        
        return {
            "success": True,
            "message": "Sample files generated for testing",
            "files": {
                "video": "sample_video.mp4",
                "audio": "sample_audio.mp3", 
                "music": "sample_music.mp3",
                "image": "sample_image.png",
                "scenes": "sample_scenes.json"
            },
            "download_urls": {
                "video": "/files/videos/sample_video.mp4",
                "audio": "/files/audio/sample_audio.mp3",
                "music": "/files/music/sample_music.mp3", 
                "image": "/files/images/sample_image.png",
                "scenes": "/files/scenes/sample_scenes.json"
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating sample files: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating sample files: {str(e)}")

@app.get("/test/health")
async def test_health():
    """Enhanced health check with file system status"""
    try:
        # Check if directories exist
        directories = [
            pathlib.Path(SAVE_OUTPUTS_DIR),
            pathlib.Path(SAVE_OUTPUTS_DIR) / "scenes",
            pathlib.Path(SAVE_OUTPUTS_DIR) / "images", 
            pathlib.Path(SAVE_OUTPUTS_DIR) / "audio",
            pathlib.Path(SAVE_OUTPUTS_DIR) / "music",
            pathlib.Path(SAVE_OUTPUTS_DIR) / "videos"
        ]
        
        dir_status = {}
        for directory in directories:
            dir_status[str(directory)] = {
                "exists": directory.exists(),
                "is_dir": directory.is_dir() if directory.exists() else False
            }
        
        return {
            "status": "healthy",
            "api_version": "2.0.0",
            "active_workflows": len(get_workflow_manager().active_workflows),
            "directories": dir_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "workflow_api:app",
        host=host,
        port=port,
        reload=True
    ) 