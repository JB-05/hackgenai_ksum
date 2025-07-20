import logging
import time
import requests
import os
from typing import Optional, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ImageGenerationRequest, ImageGenerationResponse
from utils import file_manager
from utils.gemini_client import get_gemini_client
from config import config
import asyncio

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Generate images using various AI services from scene prompts"""
    
    def __init__(self):
        self.gemini_client = get_gemini_client()
        self.default_size = config.DEFAULT_IMAGE_SIZE
        self.default_style = config.DEFAULT_IMAGE_STYLE
        # Note: For actual image generation, we might need to use a different service
        # as Gemini Pro Vision is primarily for image analysis
        self.use_openai_dalle = bool(config.OPENAI_API_KEY)
    
    def _enhance_prompt(self, scene_description: str, style: str = "realistic") -> str:
        """Enhance the scene description for better image generation"""
        style_prompts = {
            "realistic": "photorealistic, high quality, detailed",
            "artistic": "artistic, painterly style, creative",
            "cartoon": "cartoon style, animated, colorful",
            "cinematic": "cinematic, dramatic lighting, movie scene",
            "fantasy": "fantasy art style, magical, ethereal"
        }
        
        style_desc = style_prompts.get(style, style_prompts["realistic"])
        
        enhanced_prompt = f"{scene_description}, {style_desc}, high resolution, professional photography"
        
        # Add common quality improvements
        enhanced_prompt += ", sharp focus, beautiful composition, professional lighting"
        
        return enhanced_prompt
    
    async def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate an image for a scene"""
        start_time = time.time()
        
        try:
            logger.info(f"Generating image for scene {request.scene_number}")
            
            # Enhance the prompt
            enhanced_prompt = self._enhance_prompt(
                request.scene_description, 
                request.style
            )
            
            # Generate image with retry mechanism
            image_url = await self._generate_image_with_service(
                enhanced_prompt,
                request.size
            )
            
            # Download and save the image
            filename = await self._download_and_save_image(image_url, request.scene_number)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create response
            response = ImageGenerationResponse(
                scene_number=request.scene_number,
                image_url=f"/files/images/{filename}",
                prompt_used=enhanced_prompt,
                processing_time=processing_time
            )
            
            logger.info(f"Image generation completed for scene {request.scene_number} in {processing_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating image for scene {request.scene_number}: {e}")
            raise
    
    async def _generate_image_with_service(self, prompt: str, size: str) -> str:
        """Generate image using available services"""
        try:
            if self.use_openai_dalle:
                # Use DALL-E if OpenAI API key is available
                import openai
                client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality="standard",
                    n=1
                )
                return response.data[0].url
            else:
                # Fallback: Use Gemini for prompt enhancement and return placeholder
                logger.warning("⚠️ Image generation not available with current setup")
                logger.info("Using Gemini to enhance prompt for future image generation")
                
                # Use Gemini to enhance the prompt
                enhanced_prompt = await self.gemini_client.generate_text(
                    f"Enhance this image generation prompt for better results: {prompt}",
                    "You are an expert at creating detailed image generation prompts."
                )
                
                # For now, return a placeholder URL
                # In a real implementation, you might use another image generation service
                return f"placeholder_image_{int(time.time())}.png"
                
        except Exception as e:
            logger.error(f"Image generation API error: {e}")
            raise
    
    async def _download_and_save_image(self, image_url: str, scene_number: int) -> str:
        """Download image from URL and save to local storage"""
        try:
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            timestamp = int(time.time())
            filename = f"scene_{scene_number}_{timestamp}.png"
            
            # Save image
            file_manager.save_file(
                response.content,
                "images",
                filename
            )
            
            logger.info(f"Image saved: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error downloading/saving image: {e}")
            raise
    
    async def generate_images_for_scenes(self, scenes_data: list) -> list:
        """Generate images for multiple scenes"""
        results = []
        
        for scene in scenes_data:
            try:
                request = ImageGenerationRequest(
                    scene_description=scene["prompt"],
                    scene_number=scene["scene_number"],
                    style="realistic"
                )
                
                result = await self.generate_image(request)
                results.append(result)
                
                # Small delay between requests to be respectful to API
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to generate image for scene {scene['scene_number']}: {e}")
                # Continue with other scenes even if one fails
                continue
        
        return results

# Global image generator instance
_image_generator = None

def get_image_generator():
    """Get the global image generator instance"""
    global _image_generator
    if _image_generator is None:
        _image_generator = ImageGenerator()
    return _image_generator

# For backward compatibility
image_generator = get_image_generator() 