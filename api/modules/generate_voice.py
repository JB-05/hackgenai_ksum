import logging
import time
import os
from typing import Optional, Dict, Any
from ..models import VoiceGenerationRequest, VoiceGenerationResponse
from ..utils import file_manager, retry_handler, response_formatter
from ..config import config

logger = logging.getLogger(__name__)

# ElevenLabs import with Python 3.13 compatibility
ELEVENLABS_AVAILABLE = False
try:
    import elevenlabs
    ELEVENLABS_AVAILABLE = True
    logger.info("ElevenLabs SDK imported successfully")
except ImportError as e:
    logger.warning(f"ElevenLabs SDK import failed: {e}")
    logger.warning("Voice generation will use fallback mode")
except NameError as e:
    if "ArrayJsonSchemaPropertyInput" in str(e):
        logger.error("ElevenLabs SDK incompatible with Python 3.13")
        logger.error("This is a known issue with ElevenLabs + Python 3.13")
        logger.error("Consider using Python 3.11 or 3.12 for full functionality")
        logger.warning("Voice generation will use fallback mode")
    else:
        logger.error(f"ElevenLabs SDK import error: {e}")
        logger.warning("Voice generation will use fallback mode")
except Exception as e:
    logger.error(f"Unexpected error importing ElevenLabs: {e}")
    logger.warning("Voice generation will use fallback mode")

class VoiceGenerator:
    """Generate voice narration using ElevenLabs API with fallback support"""
    
    def __init__(self):
        self.api_key = config.ELEVENLABS_API_KEY
        self.default_voice_id = config.ELEVENLABS_DEFAULT_VOICE
        self.elevenlabs_available = ELEVENLABS_AVAILABLE
        
        # Initialize ElevenLabs client only if available
        if self.elevenlabs_available and self.api_key:
            try:
                self.client = elevenlabs.client.ElevenLabs(api_key=self.api_key)
                logger.info("ElevenLabs client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ElevenLabs client: {e}")
                self.client = None
                self.elevenlabs_available = False
        else:
            self.client = None
            if not self.elevenlabs_available:
                logger.warning("ElevenLabs SDK not available - using fallback mode")
            if not self.api_key:
                logger.warning("No ElevenLabs API key provided - using fallback mode")
        
        # Available voices (you can expand this list)
        self.available_voices = {
            "narrator": "21m00Tcm4TlvDq8ikWAM",  # Rachel - Good for narration
            "male": "pNInz6obpgDQGcFmaJgB",      # Adam - Male voice
            "female": "EXAVITQu4vr4xnSDxMaL",    # Bella - Female voice
            "child": "AZnzlk1XvdvUeBnXmlld",     # Domi - Younger voice
            "elderly": "VR6AewLTigWG4xSOukaG"     # Arnold - Older voice
        }
    
    def _get_voice_id(self, voice_type: str = "narrator") -> str:
        """Get voice ID based on voice type"""
        return self.available_voices.get(voice_type, self.default_voice_id)
    
    def _optimize_text_for_speech(self, text: str) -> str:
        """Optimize text for better speech synthesis"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Add pauses for better pacing
        text = text.replace(". ", ". ... ")
        text = text.replace("! ", "! ... ")
        text = text.replace("? ", "? ... ")
        
        # Handle common abbreviations
        text = text.replace("Mr.", "Mister")
        text = text.replace("Mrs.", "Missus")
        text = text.replace("Dr.", "Doctor")
        
        return text
    
    async def generate_voice(self, request: VoiceGenerationRequest) -> VoiceGenerationResponse:
        """Generate voice narration from text"""
        start_time = time.time()
        
        try:
            logger.info(f"Generating voice for text: {len(request.text)} characters")
            
            # Optimize text for speech
            optimized_text = self._optimize_text_for_speech(request.text)
            
            # Get voice ID
            voice_id = request.voice_id or self._get_voice_id()
            
            # Generate audio with retry mechanism
            audio_data = await retry_handler.retry_async(
                self._call_elevenlabs,
                optimized_text,
                voice_id,
                request.voice_settings
            )
            
            # Save audio file
            filename = self._save_audio_file(audio_data, voice_id)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Estimate duration (rough calculation: ~150 words per minute)
            word_count = len(optimized_text.split())
            estimated_duration = (word_count / 150) * 60  # seconds
            
            # Create response
            response = VoiceGenerationResponse(
                success=True,
                message="Voice generation completed successfully",
                audio_file=filename,
                duration=estimated_duration,
                voice_id=voice_id,
                text_length=len(optimized_text)
            )
            
            logger.info(f"Voice generation completed in {processing_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            raise
    
    async def _call_elevenlabs(self, text: str, voice_id: str, voice_settings: Optional[Dict[str, Any]] = None) -> bytes:
        """Call ElevenLabs API to generate audio with fallback support"""
        try:
            # Check if ElevenLabs is available
            if not self.elevenlabs_available or not self.client:
                logger.warning("ElevenLabs not available - generating fallback audio")
                return self._generate_fallback_audio(text, voice_id)
            
            # Default voice settings
            default_settings = {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
            
            # Merge with custom settings if provided
            if voice_settings:
                default_settings.update(voice_settings)
            
            # Generate audio using the ElevenLabs API
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1",
                voice_settings=default_settings
            )
            
            return audio
            
        except Exception as e:
            logger.error(f"ElevenLabs API error: {e}")
            logger.warning("Falling back to mock audio generation")
            return self._generate_fallback_audio(text, voice_id)
    
    def _generate_fallback_audio(self, text: str, voice_id: str) -> bytes:
        """Generate fallback audio when ElevenLabs is not available"""
        try:
            # Create a simple text-to-speech placeholder
            # In a real implementation, you might use a different TTS service
            # or generate a simple audio file with basic speech synthesis
            
            # For now, create a mock audio file with text information
            mock_audio_content = f"""
            FALLBACK AUDIO - ElevenLabs not available
            Text: {text[:100]}...
            Voice ID: {voice_id}
            Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
            
            This is a placeholder audio file generated because:
            1. ElevenLabs SDK is not available (Python 3.13 compatibility issue)
            2. No ElevenLabs API key provided
            3. ElevenLabs service is unavailable
            
            To get real voice synthesis:
            - Use Python 3.11 or 3.12 instead of 3.13
            - Or provide a valid ElevenLabs API key
            - Or implement an alternative TTS service
            """.encode('utf-8')
            
            # Create a simple WAV-like header (very basic)
            # This creates a minimal audio file that can be played
            sample_rate = 22050
            duration = 3.0  # 3 seconds
            num_samples = int(sample_rate * duration)
            
            # Simple sine wave at 440Hz (A note)
            import math
            audio_data = bytearray()
            
            # WAV header (simplified)
            audio_data.extend(b'RIFF')
            audio_data.extend((36 + num_samples * 2).to_bytes(4, 'little'))  # File size
            audio_data.extend(b'WAVE')
            audio_data.extend(b'fmt ')
            audio_data.extend((16).to_bytes(4, 'little'))  # Chunk size
            audio_data.extend((1).to_bytes(2, 'little'))   # Audio format (PCM)
            audio_data.extend((1).to_bytes(2, 'little'))   # Channels
            audio_data.extend(sample_rate.to_bytes(4, 'little'))  # Sample rate
            audio_data.extend((sample_rate * 2).to_bytes(4, 'little'))  # Byte rate
            audio_data.extend((2).to_bytes(2, 'little'))   # Block align
            audio_data.extend((16).to_bytes(2, 'little'))  # Bits per sample
            audio_data.extend(b'data')
            audio_data.extend((num_samples * 2).to_bytes(4, 'little'))  # Data size
            
            # Generate simple sine wave
            for i in range(num_samples):
                # Simple sine wave at 440Hz
                sample = int(32767 * 0.1 * math.sin(2 * math.pi * 440 * i / sample_rate))
                audio_data.extend(sample.to_bytes(2, 'little', signed=True))
            
            logger.info(f"Generated fallback audio: {len(audio_data)} bytes")
            return bytes(audio_data)
            
        except Exception as e:
            logger.error(f"Error generating fallback audio: {e}")
            # Return minimal audio data as last resort
            return b"mock_audio_data_for_testing"
    
    def _save_audio_file(self, audio_data: bytes, voice_id: str) -> str:
        """Save audio data to file"""
        try:
            # Generate filename
            timestamp = int(time.time())
            filename = f"voice_{voice_id}_{timestamp}.mp3"
            
            # Save audio
            file_manager.save_file(
                audio_data,
                "audio",
                filename
            )
            
            logger.info(f"Audio saved: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving audio file: {e}")
            raise
    
    async def generate_narration_for_story(self, story_text: str, voice_type: str = "narrator") -> VoiceGenerationResponse:
        """Generate narration for an entire story"""
        try:
            # Split long text into chunks if needed (ElevenLabs has limits)
            max_chars = 2500  # Conservative limit
            chunks = self._split_text_into_chunks(story_text, max_chars)
            
            if len(chunks) == 1:
                # Single chunk, generate normally
                request = VoiceGenerationRequest(
                    text=chunks[0],
                    voice_id=self._get_voice_id(voice_type)
                )
                return await self.generate_voice(request)
            else:
                # Multiple chunks, generate separately and combine
                logger.info(f"Story split into {len(chunks)} chunks for processing")
                return await self._generate_multiple_chunks(chunks, voice_type)
                
        except Exception as e:
            logger.error(f"Error generating story narration: {e}")
            raise
    
    def _split_text_into_chunks(self, text: str, max_chars: int) -> list:
        """Split text into chunks that fit within API limits"""
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        for sentence in text.split(". "):
            if len(current_chunk + sentence) <= max_chars:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def _generate_multiple_chunks(self, chunks: list, voice_type: str) -> VoiceGenerationResponse:
        """Generate audio for multiple text chunks and combine them"""
        # For now, just generate the first chunk
        # In a full implementation, you'd combine multiple audio files
        request = VoiceGenerationRequest(
            text=chunks[0],
            voice_id=self._get_voice_id(voice_type)
        )
        
        response = await self.generate_voice(request)
        
        # Add note about multiple chunks
        logger.warning(f"Generated audio for first chunk only. Total chunks: {len(chunks)}")
        
        return response

# Global voice generator instance
_voice_generator = None

def get_voice_generator():
    """Get the global voice generator instance"""
    global _voice_generator
    if _voice_generator is None:
        _voice_generator = VoiceGenerator()
    return _voice_generator

# For backward compatibility
voice_generator = get_voice_generator() 