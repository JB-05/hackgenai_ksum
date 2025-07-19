import openai
import logging
import time
from typing import List, Dict, Any
from ..models import StoryRequest, Scene, SceneBreakdownResponse
from ..utils import file_manager, retry_handler, response_formatter
from ..config import config

logger = logging.getLogger(__name__)

class StoryToScenesProcessor:
    """Process stories and break them down into scenes using GPT-4"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
    
    def _create_scene_prompt(self, story_text: str, title: str, max_scenes: int) -> str:
        """Create the prompt for scene breakdown"""
        return f"""
You are a professional story analyst. Break down the following story into {max_scenes} key scenes.

Story Title: {title}
Story: {story_text}

Instructions:
1. Analyze the story and identify {max_scenes} most important scenes
2. Each scene should be a distinct moment or event in the story
3. Create a compelling image generation prompt for each scene
4. Ensure scenes flow logically and cover the entire story

Output Format (JSON):
{{
    "scenes": [
        {{
            "scene_number": 1,
            "description": "Brief scene description (1-2 sentences)",
            "prompt": "Detailed image generation prompt for this scene",
            "duration": 5
        }}
    ]
}}

Requirements:
- Scene descriptions should be clear and concise
- Image prompts should be detailed and visual
- Each scene should have 5 seconds duration
- Ensure the JSON is valid and properly formatted
"""
    
    async def process_story(self, request: StoryRequest) -> SceneBreakdownResponse:
        """Process a story and break it down into scenes"""
        start_time = time.time()
        
        try:
            logger.info(f"Processing story: {request.title or 'Untitled'}")
            
            # Create the prompt
            prompt = self._create_scene_prompt(
                request.story_text, 
                request.title or "Untitled Story", 
                request.max_scenes
            )
            
            # Call GPT-4 with retry mechanism
            response = await retry_handler.retry_async(
                self._call_openai,
                prompt
            )
            
            # Parse the response
            scenes_data = self._parse_openai_response(response)
            
            # Create scene objects
            scenes = []
            for scene_data in scenes_data:
                scene = Scene(
                    scene_number=scene_data["scene_number"],
                    description=scene_data["description"],
                    prompt=scene_data["prompt"],
                    duration=scene_data.get("duration", 5)
                )
                scenes.append(scene)
            
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
            filename = file_manager.save_json(
                response_data.model_dump(),
                "scenes",
                f"scenes_{int(start_time)}_{request.title or 'untitled'}.json"
            )
            
            logger.info(f"Scene breakdown completed: {len(scenes)} scenes in {processing_time:.2f}s")
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing story: {e}")
            raise
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional story analyst and JSON formatter."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.OPENAI_MAX_TOKENS,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _parse_openai_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse the OpenAI response to extract scenes"""
        import json
        import re
        
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                return data.get("scenes", [])
            else:
                # Fallback: try to parse the entire response as JSON
                data = json.loads(response)
                return data.get("scenes", [])
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            logger.error(f"Response: {response}")
            
            # Fallback: create a simple scene breakdown
            return self._create_fallback_scenes(response)
    
    def _create_fallback_scenes(self, response: str) -> List[Dict[str, Any]]:
        """Create fallback scenes if JSON parsing fails"""
        logger.warning("Using fallback scene creation")
        
        # Split response into lines and create basic scenes
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        
        scenes = []
        for i, line in enumerate(lines[:4], 1):  # Max 4 scenes
            scenes.append({
                "scene_number": i,
                "description": line[:100] + "..." if len(line) > 100 else line,
                "prompt": f"Scene {i}: {line}",
                "duration": 5
            })
        
        return scenes

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