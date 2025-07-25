import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # File Storage Configuration
    SAVE_OUTPUTS_DIR: str = os.getenv("SAVE_OUTPUTS_DIR", "save_outputs")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    
    # Google Gemini Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    GEMINI_VISION_MODEL: str = os.getenv("GEMINI_VISION_MODEL", "gemini-1.5-flash")
    GEMINI_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_DEFAULT_VOICE: str = os.getenv("ELEVENLABS_DEFAULT_VOICE", "21m00Tcm4TlvDq8ikWAM")
    
    # Suno.ai Configuration (for music generation)
    SUNO_API_KEY: Optional[str] = os.getenv("SUNO_API_KEY")
    
    # Processing Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "1.0"))
    
    # Video Configuration
    DEFAULT_VIDEO_FPS: int = int(os.getenv("DEFAULT_VIDEO_FPS", "24"))
    DEFAULT_VIDEO_FORMAT: str = os.getenv("DEFAULT_VIDEO_FORMAT", "mp4")
    
    # Image Configuration
    DEFAULT_IMAGE_SIZE: str = os.getenv("DEFAULT_IMAGE_SIZE", "1024x1024")
    DEFAULT_IMAGE_STYLE: str = os.getenv("DEFAULT_IMAGE_STYLE", "realistic")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present"""
        required_keys = ["GEMINI_API_KEY"]
        missing_keys = [key for key in required_keys if not getattr(cls, key)]

        if missing_keys:
            raise RuntimeError(f"🚨 Missing required environment variables: {missing_keys}")
        print("✅ All required config variables are present.")
        return True
    
    @classmethod
    def get_api_keys_status(cls) -> dict:
        """Get status of API keys"""
        return {
            "openai": bool(cls.OPENAI_API_KEY),
            "gemini": bool(cls.GEMINI_API_KEY),
            "elevenlabs": bool(cls.ELEVENLABS_API_KEY),
            "suno": bool(cls.SUNO_API_KEY)
        }

# Global config instance
config = Config()

# Add logging for API keys loading status
print(f"[CONFIG CHECK] ✅ OPENAI_API_KEY Loaded: {bool(Config.OPENAI_API_KEY)}")
print(f"[CONFIG CHECK] ✅ GEMINI_API_KEY Loaded: {bool(Config.GEMINI_API_KEY)}")

# Validate configuration at startup
config.validate_config() 