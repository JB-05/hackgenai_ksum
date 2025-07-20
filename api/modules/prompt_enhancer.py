import logging
import time
import re
from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow_models import UserPromptRequest, EnhancedPromptResponse
from utils.gemini_client import get_gemini_client
from config import config

logger = logging.getLogger(__name__)

class PromptEnhancer:
    """Enhances user prompts into full stories using Google Gemini"""
    
    def __init__(self):
        self.gemini_client = get_gemini_client()
        self.system_prompt = "You are a professional story writer and creative director specializing in video storytelling."
    
    def _create_enhancement_prompt(self, user_prompt: str, title: str = None, max_scenes: int = 4) -> str:
        """Create the prompt for story enhancement"""
        return f"""
You are a professional story writer and creative director. Your task is to enhance a user's story prompt into a complete, engaging story that can be turned into a video.

User's Original Prompt: "{user_prompt}"

Instructions:
1. Expand the user's prompt into a complete story (300-500 words)
2. Add rich details, character development, and engaging plot elements
3. Ensure the story has a clear beginning, middle, and end
4. Make it suitable for visual storytelling with distinct scenes
5. Create a compelling title if none provided
6. Ensure the story can be broken down into {max_scenes} clear scenes

Requirements:
- Engaging and imaginative storytelling
- Clear character motivations and development
- Visual descriptions that can be illustrated
- Emotional depth and narrative arc
- Age-appropriate content
- Suitable for video adaptation

Output Format (JSON):
{{
    "enhanced_story": "Complete enhanced story text...",
    "story_title": "Compelling story title",
    "estimated_scenes": {max_scenes},
    "enhancement_notes": [
        "Added character development for protagonist",
        "Expanded setting descriptions",
        "Created clear narrative arc",
        "Added emotional depth and conflict resolution"
    ]
}}

Make the story engaging, visual, and ready for video production.
"""
    
    async def enhance_prompt(self, request: UserPromptRequest) -> EnhancedPromptResponse:
        """Enhance a user prompt into a full story"""
        start_time = time.time()
        
        try:
            logger.info(f"Enhancing prompt: {request.user_prompt[:50]}...")
            
            # Create the enhancement prompt
            prompt = self._create_enhancement_prompt(
                request.user_prompt,
                request.title,
                request.max_scenes
            )
            
            # Call Gemini with retry mechanism
            response = await self.gemini_client.generate_text_with_retry(
                prompt,
                self.system_prompt
            )
            
            # Parse the response
            enhancement_data = self._parse_enhancement_response(response)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create response
            response_data = EnhancedPromptResponse(
                original_prompt=request.user_prompt,
                enhanced_story=enhancement_data["enhanced_story"],
                story_title=enhancement_data["story_title"],
                estimated_scenes=enhancement_data["estimated_scenes"],
                processing_time=processing_time,
                enhancement_notes=enhancement_data["enhancement_notes"]
            )
            
            logger.info(f"Prompt enhancement completed in {processing_time:.2f}s")
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error enhancing prompt: {e}")
            raise
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API for prompt enhancement"""
        try:
            return await self.gemini_client.generate_text(prompt, self.system_prompt)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            # Handle Gemini-specific errors
            error_info = self.gemini_client.handle_gemini_error(e)
            raise Exception(f"Gemini API error: {error_info['message']}")
    
    def _parse_enhancement_response(self, response: str) -> Dict[str, Any]:
        import json
        import re

        try:
            # Attempt to extract JSON blob from inside the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                logger.debug(f"[JSON Extracted] {json_str[:200]}...")  # Preview
                data = json.loads(json_str)
                return data
            else:
                logger.warning("⚠️ No JSON block found in model response. Attempting fallback...")
                return self._create_fallback_enhancement(response)
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            logger.debug(f"[Raw Response] {response}")
            return self._create_fallback_enhancement(response)
    
    def _create_fallback_enhancement(self, response: str) -> Dict[str, Any]:
        """Create fallback enhancement if JSON parsing fails"""
        logger.warning("Using fallback enhancement creation")
        
        # Extract title from response or create one
        title_match = re.search(r'title["\']?\s*:\s*["\']([^"\']+)["\']', response, re.IGNORECASE)
        story_title = title_match.group(1) if title_match else "Enhanced Story"
        
        # Use the response as enhanced story
        enhanced_story = response.strip()
        
        # Estimate scenes based on content
        estimated_scenes = min(4, max(2, len(enhanced_story.split('.')) // 3))
        
        return {
            "enhanced_story": enhanced_story,
            "story_title": story_title,
            "estimated_scenes": estimated_scenes,
            "enhancement_notes": [
                "Used fallback enhancement due to parsing error",
                "Story expanded from original prompt",
                "Ready for scene breakdown"
            ]
        }
    
    def analyze_prompt_quality(self, user_prompt: str) -> Dict[str, Any]:
        """Analyze the quality and potential of a user prompt"""
        analysis = {
            "length_score": min(100, len(user_prompt) / 2),  # Score based on length
            "detail_level": "low",
            "visual_potential": "medium",
            "story_elements": [],
            "suggestions": []
        }
        
        # Analyze prompt characteristics
        if len(user_prompt) < 50:
            analysis["detail_level"] = "low"
            analysis["suggestions"].append("Consider adding more details about characters and setting")
        elif len(user_prompt) < 150:
            analysis["detail_level"] = "medium"
        else:
            analysis["detail_level"] = "high"
        
        # Check for story elements
        story_elements = []
        if any(word in user_prompt.lower() for word in ["character", "person", "hero", "protagonist"]):
            story_elements.append("character")
        if any(word in user_prompt.lower() for word in ["setting", "place", "world", "location"]):
            story_elements.append("setting")
        if any(word in user_prompt.lower() for word in ["conflict", "problem", "challenge", "quest"]):
            story_elements.append("conflict")
        if any(word in user_prompt.lower() for word in ["ending", "conclusion", "resolution"]):
            story_elements.append("resolution")
        
        analysis["story_elements"] = story_elements
        
        # Assess visual potential
        visual_keywords = ["color", "light", "dark", "bright", "shadow", "texture", "shape", "size"]
        visual_count = sum(1 for word in visual_keywords if word in user_prompt.lower())
        if visual_count >= 3:
            analysis["visual_potential"] = "high"
        elif visual_count >= 1:
            analysis["visual_potential"] = "medium"
        else:
            analysis["visual_potential"] = "low"
            analysis["suggestions"].append("Consider adding visual descriptions for better video adaptation")
        
        return analysis

# Global enhancer instance
_prompt_enhancer = None

def get_prompt_enhancer():
    """Get the global prompt enhancer instance"""
    global _prompt_enhancer
    if _prompt_enhancer is None:
        _prompt_enhancer = PromptEnhancer()
    return _prompt_enhancer

# For backward compatibility
prompt_enhancer = get_prompt_enhancer() 