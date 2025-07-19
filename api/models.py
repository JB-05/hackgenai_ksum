from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class StoryRequest(BaseModel):
    """Request model for story input"""
    story_text: str = Field(..., description="The story text to process", min_length=10)
    title: Optional[str] = Field(None, description="Optional title for the story")
    max_scenes: Optional[int] = Field(4, description="Maximum number of scenes to generate", ge=2, le=6)

class Scene(BaseModel):
    """Model for a single scene"""
    scene_number: int = Field(..., description="Scene number")
    description: str = Field(..., description="Scene description")
    prompt: str = Field(..., description="Image generation prompt for this scene")
    duration: Optional[int] = Field(5, description="Duration in seconds for this scene")

class SceneBreakdownResponse(BaseModel):
    """Response model for scene breakdown"""
    story_title: str = Field(..., description="Title of the story")
    scenes: List[Scene] = Field(..., description="List of generated scenes")
    total_scenes: int = Field(..., description="Total number of scenes")
    processing_time: float = Field(..., description="Time taken to process in seconds")

class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""
    scene_description: str = Field(..., description="Scene description for image generation")
    scene_number: int = Field(..., description="Scene number")
    style: Optional[str] = Field("realistic", description="Image style (realistic, artistic, cartoon, etc.)")
    size: Optional[str] = Field("1024x1024", description="Image size")

class ImageGenerationResponse(BaseModel):
    """Response model for image generation"""
    scene_number: int = Field(..., description="Scene number")
    image_url: str = Field(..., description="URL or path to generated image")
    prompt_used: str = Field(..., description="Final prompt used for generation")
    processing_time: float = Field(..., description="Time taken to process in seconds")

class VoiceGenerationRequest(BaseModel):
    """Request model for voice generation"""
    text: str = Field(..., description="Text to convert to speech")
    voice_id: Optional[str] = Field("21m00Tcm4TlvDq8ikWAM", description="Voice ID for ElevenLabs")
    voice_settings: Optional[Dict[str, Any]] = Field(None, description="Voice settings")

class VoiceGenerationResponse(BaseModel):
    """Response model for voice generation"""
    success: bool = Field(..., description="Success status")
    message: str = Field(..., description="Response message")
    audio_file: Optional[str] = Field(None, description="Path to generated audio file")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    voice_id: Optional[str] = Field(None, description="Voice ID used")
    text_length: Optional[int] = Field(None, description="Length of processed text")

class MusicGenerationRequest(BaseModel):
    """Request model for music generation"""
    story_title: str = Field(..., description="Title of the story")
    story_text: str = Field(..., description="The story text")
    scenes: List[Dict] = Field(..., description="List of scene dictionaries")
    mood: Optional[str] = Field("neutral", description="Mood for music (happy, sad, mysterious, adventurous, calm, neutral)")
    duration: Optional[int] = Field(60, description="Duration in seconds", ge=10, le=300)
    style: Optional[str] = Field("ambient", description="Music style (ambient, orchestral, electronic, acoustic)")

class MusicGenerationResponse(BaseModel):
    """Response model for music generation"""
    success: bool = Field(..., description="Success status")
    message: str = Field(..., description="Response message")
    music_file: Optional[str] = Field(None, description="Path to generated music file")
    duration: Optional[int] = Field(None, description="Music duration in seconds")
    style: Optional[str] = Field(None, description="Music style used")
    mood: Optional[str] = Field(None, description="Mood used for generation")

class VideoCreationRequest(BaseModel):
    """Request model for video creation"""
    scene_images: List[str] = Field(..., description="List of image file paths")
    voice_audio: str = Field(..., description="Voice audio file path")
    background_music: str = Field(..., description="Background music file path")
    output_format: Optional[str] = Field("mp4", description="Output video format")
    fps: Optional[int] = Field(24, description="Frames per second")

class VideoCreationResponse(BaseModel):
    """Response model for video creation"""
    video_url: str = Field(..., description="URL or path to generated video")
    duration: float = Field(..., description="Video duration in seconds")
    file_size: int = Field(..., description="File size in bytes")
    format: str = Field(..., description="Video format")
    processing_time: float = Field(..., description="Time taken to process in seconds")

class ProcessingStatus(BaseModel):
    """Model for processing status"""
    status: str = Field(..., description="Processing status (pending, processing, completed, failed)")
    progress: float = Field(..., description="Progress percentage (0-100)")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now)

class SuccessResponse(BaseModel):
    """Model for success responses"""
    success: bool = Field(True, description="Success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now) 