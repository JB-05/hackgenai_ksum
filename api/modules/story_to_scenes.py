import logging
import time
from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import StoryRequest, Scene, SceneBreakdownResponse
from utils import file_manager
from utils.gemini_client import get_gemini_client
from config import config

logger = logging.getLogger(__name__)

class StoryToScenesProcessor:
    """Process stories and break them down into scenes using Google Gemini"""
    
    def __init__(self):
        self.gemini_client = get_gemini_client()
        self.system_prompt = "You are a professional story analyst and JSON formatter."
    
    def _create_scene_prompt(self, story_text: str, title: str, max_scenes: int) -> str:
        """Create a detailed prompt for scene breakdown using Gemini"""
        return f"""
You are an expert story analyst and video director. Your task is to break down the following story into exactly {max_scenes} key scenes that will be used to create a compelling video.

STORY DETAILS:
Title: {title}
Story: {story_text}

ANALYSIS INSTRUCTIONS:
1. Read the story carefully and identify the {max_scenes} most important narrative moments
2. Each scene should represent a distinct event, location change, or emotional turning point
3. Ensure the scenes flow chronologically and cover the entire story arc
4. Consider visual storytelling - each scene should be visually distinct and engaging

SCENE REQUIREMENTS:
- Scene descriptions: Clear, concise summaries (1-2 sentences)
- Image prompts: Detailed, visual descriptions suitable for AI image generation
- Duration: Each scene should be 5 seconds for optimal video pacing
- Visual variety: Ensure scenes have different settings, lighting, or moods

OUTPUT FORMAT (Valid JSON only):
{{
    "scenes": [
        {{
            "scene_number": 1,
            "description": "Brief scene description that captures the key moment",
            "prompt": "Detailed visual prompt for image generation including setting, lighting, mood, characters, and style",
            "duration": 5
        }},
        {{
            "scene_number": 2,
            "description": "Next key moment in the story",
            "prompt": "Visual prompt for this scene with specific details",
            "duration": 5
        }}
    ]
}}

IMPORTANT:
- Return ONLY valid JSON - no additional text or explanations
- Ensure all scene numbers are sequential (1, 2, 3, etc.)
- Make image prompts rich in visual details for better AI generation
- Keep descriptions concise but informative
- Maintain narrative flow between scenes
"""
    
    async def process_story(self, request: StoryRequest) -> SceneBreakdownResponse:
        """Process a story and break it down into scenes"""
        return await self._process_story_internal(request, is_regenerate=False)
    
    async def regenerate_scenes(self, request: StoryRequest) -> SceneBreakdownResponse:
        """Regenerate scenes for a story - same as process_story but with different logging"""
        return await self._process_story_internal(request, is_regenerate=True)
    
    async def _process_story_internal(self, request: StoryRequest, is_regenerate: bool = False) -> SceneBreakdownResponse:
        """Internal method to process story with optional regenerate flag"""
        start_time = time.time()
        operation = "Regenerating" if is_regenerate else "Processing"
        
        try:
            logger.info(f"{operation} story: {request.title or 'Untitled'}")
            
            # Validate input
            if not request.story_text or len(request.story_text.strip()) < 10:
                raise ValueError("Story text must be at least 10 characters long")
            
            if request.max_scenes < 2 or request.max_scenes > 6:
                raise ValueError("Max scenes must be between 2 and 6")
            
            # Create the prompt
            prompt = self._create_scene_prompt(
                request.story_text, 
                request.title or "Untitled Story", 
                request.max_scenes
            )
            
            # Call Gemini with retry mechanism
            response = await self.gemini_client.generate_text_with_retry(
                prompt,
                self.system_prompt,
                max_retries=3
            )
            
            # Parse the response
            scenes_data = self._parse_gemini_response(response)
            
            # Validate scenes data
            if not scenes_data or len(scenes_data) == 0:
                logger.warning("⚠️ No scenes generated, using fallback")
                scenes_data = self._create_fallback_scenes(request.story_text)
            
            # Create scene objects
            scenes = []
            for scene_data in scenes_data:
                try:
                    scene = Scene(
                        scene_number=scene_data["scene_number"],
                        description=scene_data["description"],
                        prompt=scene_data["prompt"],
                        duration=scene_data.get("duration", 5)
                    )
                    scenes.append(scene)
                except KeyError as e:
                    logger.warning(f"⚠️ Missing field in scene data: {e}")
                    continue
            
            # Ensure we have the requested number of scenes
            if len(scenes) < request.max_scenes:
                logger.warning(f"⚠️ Generated {len(scenes)} scenes, requested {request.max_scenes}")
                # Add fallback scenes to reach the requested count
                additional_scenes = self._create_additional_scenes(request.story_text, len(scenes), request.max_scenes)
                scenes.extend(additional_scenes)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create response
            response_data = SceneBreakdownResponse(
                story_title=request.title or "Untitled Story",
                scenes=scenes,
                total_scenes=len(scenes),
                processing_time=processing_time
            )
            
            # Save the breakdown
            timestamp = int(start_time)
            filename = file_manager.save_json(
                response_data.model_dump(),
                "scenes",
                f"scenes_{timestamp}_{request.title or 'untitled'}_{'regenerate' if is_regenerate else 'original'}.json"
            )
            
            logger.info(f"Scene breakdown completed: {len(scenes)} scenes in {processing_time:.2f}s")
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error {operation.lower()} story: {e}")
            # Return fallback response instead of raising
            return await self._create_fallback_response(request, processing_time=time.time() - start_time)
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        try:
            return await self.gemini_client.generate_text(prompt, self.system_prompt)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            # Handle Gemini-specific errors
            error_info = self.gemini_client.handle_gemini_error(e)
            raise Exception(f"Gemini API error: {error_info['message']}")
    
    def _parse_gemini_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse the Gemini response to extract scenes"""
        import json
        import re
        
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                logger.debug(f"[JSON Extracted] {json_str[:200]}...")  # Preview
                data = json.loads(json_str)
                return data.get("scenes", [])
            else:
                logger.warning("⚠️ No JSON block found in Gemini response. Attempting fallback...")
                return self._create_fallback_scenes(response)
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            logger.debug(f"[Raw Response] {response}")
            return self._create_fallback_scenes(response)
    
    def _create_fallback_scenes(self, story_text: str) -> List[Dict[str, Any]]:
        """Create fallback scenes if JSON parsing fails"""
        logger.warning("Using fallback scene creation")
        
        # Split story into sentences and create basic scenes
        sentences = [s.strip() for s in story_text.split('.') if s.strip()]
        
        scenes = []
        max_scenes = min(4, len(sentences))
        
        for i in range(max_scenes):
            sentence = sentences[i] if i < len(sentences) else f"Scene {i+1} of the story"
            scenes.append({
                "scene_number": i + 1,
                "description": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                "prompt": f"Scene {i+1}: {sentence}",
                "duration": 5
            })
        
        return scenes
    
    def _create_additional_scenes(self, story_text: str, current_count: int, target_count: int) -> List[Scene]:
        """Create additional scenes to reach the target count"""
        additional_scenes = []
        remaining = target_count - current_count
        
        for i in range(remaining):
            scene_number = current_count + i + 1
            scene = Scene(
                scene_number=scene_number,
                description=f"Additional scene {scene_number}",
                prompt=f"Scene {scene_number}: Continuation of the story",
                duration=5
            )
            additional_scenes.append(scene)
        
        return additional_scenes
    
    async def _create_fallback_response(self, request: StoryRequest, processing_time: float) -> SceneBreakdownResponse:
        """Create a fallback response when processing fails"""
        logger.warning("Creating fallback response due to processing failure")
        
        # Create basic fallback scenes
        fallback_scenes_data = self._create_fallback_scenes(request.story_text)
        scenes = []
        
        for scene_data in fallback_scenes_data:
            scene = Scene(
                scene_number=scene_data["scene_number"],
                description=scene_data["description"],
                prompt=scene_data["prompt"],
                duration=scene_data.get("duration", 5)
            )
            scenes.append(scene)
        
        return SceneBreakdownResponse(
            story_title=request.title or "Untitled Story",
            scenes=scenes,
            total_scenes=len(scenes),
            processing_time=processing_time
        )

# Global processor instance
_story_processor = None

def get_story_processor():
    """Get the global story processor instance"""
    global _story_processor
    if _story_processor is None:
        _story_processor = StoryToScenesProcessor()
    return _story_processor

# For backward compatibility
story_processor = get_story_processor() 