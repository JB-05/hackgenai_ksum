import google.generativeai as genai
import logging
import time
import os
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)



class GeminiClient:
    """Wrapper for Google Gemini API with error handling and retry logic"""
    
    def __init__(self):
        # Get config from environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.vision_model_name = os.getenv("GEMINI_VISION_MODEL", "gemini-1.5-flash")
        self.max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))

        print(f"[GEMINI INIT] api_key = {self.api_key[:10] + '...' if self.api_key else 'None'}")
        print(f"[GEMINI INIT] model_name = {self.model_name}")
        print(f"[GEMINI INIT] vision_model_name = {self.vision_model_name}")
        print(f"[GEMINI INIT] max_tokens = {self.max_tokens}")
        logger.debug(f"Initializing GeminiClient with API key: {self.api_key}")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.vision_model = genai.GenerativeModel(self.vision_model_name)
            
            # Configure generation config
            self.generation_config = genai.types.GenerationConfig(
                max_output_tokens=self.max_tokens,
                temperature=0.8,
                top_p=0.9,
                top_k=40
            )
            print(f"[GEMINI INIT] Successfully initialized Gemini client")
        except Exception as e:
            print(f"[GEMINI INIT] Error initializing Gemini client: {e}")
            raise
    
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """Generate text using Gemini Pro"""
        try:
            # Combine system and user prompts
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            logger.debug(f"[GEMINI] Generating text with prompt: {full_prompt[:100]}...")
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )
            
            if response.text:
                logger.debug(f"[GEMINI] Generated response: {response.text[:200]}...")
                return response.text
            else:
                raise Exception("Empty response from Gemini")
                
        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            raise
    
    async def generate_text_with_retry(self, prompt: str, system_prompt: str = None, max_retries: int = 3) -> str:
        """Generate text with retry logic"""
        for attempt in range(max_retries):
            try:
                return await self.generate_text(prompt, system_prompt)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                wait_time = (2 ** attempt) * 1  # Exponential backoff
                logger.warning(f"⚠️ Gemini API attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
    
    async def generate_image(self, prompt: str) -> Optional[bytes]:
        """Generate image using Gemini Pro Vision (if available)"""
        try:
            logger.debug(f"[GEMINI VISION] Generating image with prompt: {prompt[:100]}...")
            
            # Note: Gemini Pro Vision is primarily for image analysis, not generation
            # For image generation, we might need to use a different service
            # This is a placeholder for future implementation
            logger.warning("⚠️ Image generation not yet implemented with Gemini")
            return None
            
        except Exception as e:
            logger.error(f"❌ Gemini Vision API error: {e}")
            return None
    
    def handle_gemini_error(self, error: Exception) -> Dict[str, Any]:
        """Handle Gemini-specific errors and return appropriate fallback"""
        error_message = str(error).lower()
        
        if "quota" in error_message or "rate limit" in error_message:
            logger.error("🚨 Gemini API quota exceeded or rate limited")
            return {
                "error": "quota_exceeded",
                "message": "API quota exceeded. Please try again later.",
                "retry_after": 60
            }
        elif "auth" in error_message or "invalid" in error_message:
            logger.error("🚨 Gemini API authentication error")
            return {
                "error": "authentication_error",
                "message": "Invalid API key or authentication error.",
                "retry_after": None
            }
        elif "content" in error_message or "safety" in error_message:
            logger.error("🚨 Gemini content policy violation")
            return {
                "error": "content_policy",
                "message": "Content violates safety policies. Please modify your prompt.",
                "retry_after": None
            }
        else:
            logger.error(f"🚨 Unknown Gemini API error: {error}")
            return {
                "error": "unknown_error",
                "message": "An unexpected error occurred. Please try again.",
                "retry_after": 30
            }

# Global Gemini client instance
_gemini_client = None

def get_gemini_client() -> GeminiClient:
    """Get the global Gemini client instance"""
    global _gemini_client
    if _gemini_client is None:
        try:
            print(f"[GEMINI CLIENT] Creating new Gemini client instance")
            _gemini_client = GeminiClient()
            print(f"[GEMINI CLIENT] Successfully created Gemini client")
        except ValueError as e:
            print(f"[GEMINI CLIENT] Gemini client initialization failed: {e}")
            logger.warning(f"⚠️ Gemini client initialization failed: {e}")
            _gemini_client = None
        except Exception as e:
            print(f"[GEMINI CLIENT] Unexpected error creating Gemini client: {e}")
            logger.error(f"Unexpected error creating Gemini client: {e}")
            _gemini_client = None
    else:
        print(f"[GEMINI CLIENT] Returning existing Gemini client instance")
    return _gemini_client

# For backward compatibility - only create if API key is available
try:
    gemini_client = get_gemini_client()
except:
    gemini_client = None 