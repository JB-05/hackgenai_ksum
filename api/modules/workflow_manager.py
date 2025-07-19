import asyncio
import logging
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import os

from ..workflow_models import (
    UserPromptRequest, EnhancedPromptResponse, UserConfirmationRequest,
    GenerationProgress, StoryScript, FinalVideoResponse, WorkflowStatus
)
from api.models import StoryRequest, SceneBreakdownResponse
from .prompt_enhancer import prompt_enhancer
from .story_to_scenes import story_processor
from .generate_image import image_generator
from .generate_voice import voice_generator
from .generate_music import generate_music_for_story
from ..utils import file_manager

logger = logging.getLogger(__name__)

class WorkflowManager:
    """Manages the complete workflow from prompt to video"""
    
    def __init__(self):
        self.active_workflows: Dict[str, WorkflowStatus] = {}
        # Store workflow data separately
        self.workflow_data: Dict[str, Dict[str, Any]] = {}
    
    def create_workflow(self) -> str:
        """Create a new workflow and return its ID"""
        workflow_id = str(uuid.uuid4())
        self.active_workflows[workflow_id] = WorkflowStatus(
            workflow_id=workflow_id,
            current_phase="prompt_enhancement",
            status="active"
        )
        # Initialize workflow data storage
        self.workflow_data[workflow_id] = {
            "enhanced_story": None,
            "story_title": None,
            "max_scenes": None,
            "original_prompt": None
        }
        logger.info(f"Created new workflow: {workflow_id}")
        return workflow_id
    
    async def enhance_prompt(self, workflow_id: str, request: UserPromptRequest) -> EnhancedPromptResponse:
        """Phase 1: Enhance user prompt"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            workflow.current_phase = "prompt_enhancement"
            workflow.updated_at = datetime.now()
            
            # Store original prompt
            self.workflow_data[workflow_id]["original_prompt"] = request.user_prompt
            self.workflow_data[workflow_id]["max_scenes"] = request.max_scenes
            
            # Enhance the prompt
            enhanced_response = await prompt_enhancer.enhance_prompt(request)
            
            # Store enhanced data
            self.workflow_data[workflow_id]["enhanced_story"] = enhanced_response.enhanced_story
            self.workflow_data[workflow_id]["story_title"] = enhanced_response.story_title
            
            # Update workflow status
            workflow.current_phase = "user_confirmation"
            workflow.updated_at = datetime.now()
            
            logger.info(f"Workflow {workflow_id}: Prompt enhancement completed")
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error in prompt enhancement for workflow {workflow_id}: {e}")
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id].status = "failed"
            raise
    
    async def process_user_confirmation(self, workflow_id: str, confirmation: UserConfirmationRequest) -> bool:
        """Phase 2: Process user confirmation"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            if not confirmation.proceed:
                workflow.status = "cancelled"
                workflow.current_phase = "cancelled"
                workflow.updated_at = datetime.now()
                logger.info(f"Workflow {workflow_id}: User cancelled generation")
                return False
            
            # Update workflow status
            workflow.current_phase = "generation"
            workflow.updated_at = datetime.now()
            
            logger.info(f"Workflow {workflow_id}: User confirmed, starting generation")
            return True
            
        except Exception as e:
            logger.error(f"Error processing user confirmation for workflow {workflow_id}: {e}")
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id].status = "failed"
            raise
    
    async def generate_complete_video(self, workflow_id: str, enhanced_story: str, story_title: str, max_scenes: int) -> FinalVideoResponse:
        """Phase 3: Generate complete video with all assets"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            # Use stored data if not provided
            if not enhanced_story and workflow_id in self.workflow_data:
                enhanced_story = self.workflow_data[workflow_id]["enhanced_story"]
                story_title = self.workflow_data[workflow_id]["story_title"]
                max_scenes = self.workflow_data[workflow_id]["max_scenes"]
            
            if not enhanced_story:
                raise ValueError("No enhanced story available for generation")
            
            total_start_time = time.time()
            
            # Initialize progress tracking
            progress = GenerationProgress(
                status="processing",
                progress_percentage=0.0,
                current_step="Starting generation",
                estimated_time_remaining=300.0  # 5 minutes estimate
            )
            workflow.progress = progress
            
            # Step 1: Scene Breakdown (10%)
            progress.current_step = "Breaking story into scenes"
            progress.progress_percentage = 10.0
            workflow.updated_at = datetime.now()
            
            story_request = StoryRequest(
                story_text=enhanced_story,
                title=story_title,
                max_scenes=max_scenes
            )
            
            scene_response = await story_processor.process_story(story_request)
            
            # Step 2: Generate Images (30%)
            progress.current_step = "Generating images for scenes"
            progress.progress_percentage = 30.0
            workflow.updated_at = datetime.now()
            
            image_files = []
            for scene in scene_response.scenes:
                try:
                    img_request = await image_generator.generate_image(
                        scene_description=scene.prompt,
                        scene_number=scene.scene_number,
                        style="realistic",
                        size="1024x1024"
                    )
                    image_files.append(img_request.image_url)
                    progress.progress_percentage = 30.0 + (scene.scene_number / len(scene_response.scenes)) * 30.0
                    workflow.updated_at = datetime.now()
                except Exception as e:
                    logger.warning(f"Failed to generate image for scene {scene.scene_number}: {e}")
                    # Continue with other scenes
            
            # Step 3: Generate Voice Narration (70%)
            progress.current_step = "Generating voice narration"
            progress.progress_percentage = 70.0
            workflow.updated_at = datetime.now()
            
            voice_response = await voice_generator.generate_voice(
                text=enhanced_story,
                voice_id="21m00Tcm4TlvDq8ikWAM"
            )
            
            # Step 4: Generate Background Music (85%)
            progress.current_step = "Generating background music"
            progress.progress_percentage = 85.0
            workflow.updated_at = datetime.now()
            
            scenes_data = [scene.model_dump() for scene in scene_response.scenes]
            music_response = generate_music_for_story(
                story_title=story_title,
                story_text=enhanced_story,
                scenes=scenes_data,
                mood="adventurous",
                duration=120,
                style="orchestral"
            )
            
            # Step 5: Create Final Video (95%)
            progress.current_step = "Assembling final video"
            progress.progress_percentage = 95.0
            workflow.updated_at = datetime.now()
            
            # Create actual video file
            video_file = await self._create_video_file(workflow_id, image_files, voice_response.audio_file, music_response.music_file)
            
            # Step 6: Complete (100%)
            progress.current_step = "Generation completed"
            progress.progress_percentage = 100.0
            progress.status = "completed"
            workflow.updated_at = datetime.now()
            
            total_processing_time = time.time() - total_start_time
            
            # Create story script
            story_script = StoryScript(
                story_title=story_title,
                scenes=scenes_data,
                total_duration=len(scene_response.scenes) * 5.0,  # 5 seconds per scene
                narration_text=enhanced_story,
                music_description=f"Orchestral background music, {music_response.duration}s duration",
                generation_metadata={
                    "workflow_id": workflow_id,
                    "total_scenes": len(scene_response.scenes),
                    "image_style": "realistic",
                    "voice_id": voice_response.voice_id,
                    "music_style": music_response.style,
                    "music_mood": music_response.mood
                }
            )
            
            # Create final response
            final_response = FinalVideoResponse(
                story_script=story_script,
                video_file=video_file,
                audio_file=voice_response.audio_file,
                music_file=music_response.music_file,
                image_files=image_files,
                total_processing_time=total_processing_time,
                file_sizes={
                    "video": os.path.getsize(video_file) if os.path.exists(video_file) else 0,
                    "audio": os.path.getsize(voice_response.audio_file) if os.path.exists(voice_response.audio_file) else 0,
                    "music": os.path.getsize(music_response.music_file) if os.path.exists(music_response.music_file) else 0
                }
            )
            
            # Update workflow status
            workflow.current_phase = "completed"
            workflow.status = "completed"
            workflow.result = final_response
            workflow.updated_at = datetime.now()
            
            logger.info(f"Workflow {workflow_id}: Complete video generation finished in {total_processing_time:.2f}s")
            return final_response
            
        except Exception as e:
            logger.error(f"Error in video generation for workflow {workflow_id}: {e}")
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id].status = "failed"
                self.active_workflows[workflow_id].progress = GenerationProgress(
                    status="failed",
                    progress_percentage=0.0,
                    current_step=f"Error: {str(e)}"
                )
            raise
    
    async def _create_video_file(self, workflow_id: str, image_files: list, audio_file: str, music_file: str) -> str:
        """Create an actual video file using MoviePy"""
        try:
            from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
            
            # Create a simple video from images and audio
            video_filename = f"video_{workflow_id}_{int(time.time())}.mp4"
            video_path = file_manager.get_file_path("videos", video_filename)
            
            # Create video clips from images (5 seconds each)
            video_clips = []
            for i, image_file in enumerate(image_files):
                if os.path.exists(image_file):
                    clip = ImageClip(image_file, duration=5)
                    video_clips.append(clip)
            
            if not video_clips:
                # Create a placeholder clip if no images
                from PIL import Image
                import numpy as np
                
                # Create a simple colored image
                img = Image.new('RGB', (1024, 1024), color=(100, 150, 200))
                img_array = np.array(img)
                clip = ImageClip(img_array, duration=5)
                video_clips.append(clip)
            
            # Concatenate all clips
            final_video = concatenate_videoclips(video_clips)
            
            # Add audio if available
            if os.path.exists(audio_file):
                audio = AudioFileClip(audio_file)
                # Trim audio to match video duration
                if audio.duration > final_video.duration:
                    audio = audio.subclip(0, final_video.duration)
                final_video = final_video.set_audio(audio)
            
            # Write the video file
            final_video.write_videofile(video_path, fps=24, codec='libx264')
            
            logger.info(f"Created video: {video_path}")
            return video_path
            
        except ImportError:
            logger.warning("MoviePy not available, creating placeholder video")
            return await self._create_placeholder_video(workflow_id, image_files, audio_file, music_file)
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return await self._create_placeholder_video(workflow_id, image_files, audio_file, music_file)
    
    async def _create_placeholder_video(self, workflow_id: str, image_files: list, audio_file: str, music_file: str) -> str:
        """Create a placeholder video file (in real implementation, this would create actual video)"""
        try:
            # Create a simple placeholder video file
            video_filename = f"video_{workflow_id}_{int(time.time())}.mp4"
            video_path = file_manager.get_file_path("videos", video_filename)
            
            # For now, just create an empty file
            with open(video_path, 'w') as f:
                f.write(f"Placeholder video for workflow {workflow_id}\n")
                f.write(f"Images: {len(image_files)}\n")
                f.write(f"Audio: {audio_file}\n")
                f.write(f"Music: {music_file}\n")
            
            logger.info(f"Created placeholder video: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error creating placeholder video: {e}")
            raise
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get the status of a workflow"""
        return self.active_workflows.get(workflow_id)
    
    def list_workflows(self) -> list:
        """List all active workflows"""
        return list(self.active_workflows.values())
    
    def cleanup_workflow(self, workflow_id: str):
        """Clean up a completed or failed workflow"""
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]
        if workflow_id in self.workflow_data:
            del self.workflow_data[workflow_id]
        logger.info(f"Cleaned up workflow: {workflow_id}")

# Global workflow manager instance
_workflow_manager = None

def get_workflow_manager():
    """Get the global workflow manager instance"""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = WorkflowManager()
    return _workflow_manager

# For backward compatibility
workflow_manager = get_workflow_manager() 