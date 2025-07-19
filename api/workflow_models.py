from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserPromptRequest(BaseModel):
    """Initial user prompt request"""
    user_prompt: str = Field(..., description="User's original story prompt", min_length=10)
    title: Optional[str] = Field(None, description="Optional title for the story")
    max_scenes: Optional[int] = Field(4, description="Maximum number of scenes to generate", ge=2, le=6)

class EnhancedPromptResponse(BaseModel):
    """Enhanced prompt response for user review"""
    original_prompt: str = Field(..., description="User's original prompt")
    enhanced_story: str = Field(..., description="Enhanced and expanded story")
    story_title: str = Field(..., description="Generated story title")
    estimated_scenes: int = Field(..., description="Estimated number of scenes")
    processing_time: float = Field(..., description="Time taken to enhance prompt")
    enhancement_notes: List[str] = Field(..., description="Notes about what was enhanced")

class UserConfirmationRequest(BaseModel):
    """User confirmation to proceed with generation"""
    enhanced_story: str = Field(..., description="The enhanced story to proceed with")
    story_title: str = Field(..., description="Story title")
    max_scenes: int = Field(..., description="Number of scenes to generate")
    proceed: bool = Field(..., description="Whether user wants to proceed with generation")

class GenerationProgress(BaseModel):
    """Progress tracking for generation phase"""
    status: str = Field(..., description="Current status (processing, completed, failed)")
    progress_percentage: float = Field(..., description="Progress percentage (0-100)")
    current_step: str = Field(..., description="Current step being processed")
    estimated_time_remaining: Optional[float] = Field(None, description="Estimated time remaining in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)

class StoryScript(BaseModel):
    """Final story script structure"""
    story_title: str = Field(..., description="Title of the story")
    scenes: List[Dict[str, Any]] = Field(..., description="List of scene details")
    total_duration: float = Field(..., description="Total video duration in seconds")
    narration_text: str = Field(..., description="Full narration text")
    music_description: str = Field(..., description="Background music description")
    generation_metadata: Dict[str, Any] = Field(..., description="Generation metadata")

class FinalVideoResponse(BaseModel):
    """Final video response with all assets"""
    story_script: StoryScript = Field(..., description="Complete story script")
    video_file: str = Field(..., description="Path to final video file")
    audio_file: str = Field(..., description="Path to narration audio file")
    music_file: str = Field(..., description="Path to background music file")
    image_files: List[str] = Field(..., description="List of generated image files")
    total_processing_time: float = Field(..., description="Total time taken for generation")
    file_sizes: Dict[str, int] = Field(..., description="File sizes in bytes")

class WorkflowStatus(BaseModel):
    """Overall workflow status"""
    workflow_id: str = Field(..., description="Unique workflow identifier")
    current_phase: str = Field(..., description="Current phase (prompt_enhancement, user_confirmation, generation, completed)")
    status: str = Field(..., description="Status (active, completed, failed)")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    progress: Optional[GenerationProgress] = Field(None, description="Current progress if in generation phase")
    result: Optional[FinalVideoResponse] = Field(None, description="Final result if completed") 