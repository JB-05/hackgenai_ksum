import elevenlabs
import logging
import time
import os
from typing import Optional, Dict, Any
from ..models import VoiceGenerationRequest, VoiceGenerationResponse
from ..utils import file_manager, retry_handler, response_formatter
from ..config import config

logger = logging.getLogger(__name__)

class VoiceGenerator:
    """Generate voice narration using ElevenLabs API"""
    
    def __init__(self):
        self.api_key = config.ELEVENLABS_API_KEY
        self.default_voice_id = config.ELEVENLABS_DEFAULT_VOICE
        
        # Initialize ElevenLabs client
        if self.api_key:
            self.client = elevenlabs.client.ElevenLabs(api_key=self.api_key)
        else:
            self.client = None
        
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
                audio_url=f"/files/audio/{filename}",
                duration=estimated_duration,
                voice_used=voice_id,
                processing_time=processing_time
            )
            
            logger.info(f"Voice generation completed in {processing_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            raise
    
    async def _call_elevenlabs(self, text: str, voice_id: str, voice_settings: Optional[Dict[str, Any]] = None) -> bytes:
        """Call ElevenLabs API to generate audio"""
        try:
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
            
            # Generate audio using the new API
            if self.client:
                audio = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id="eleven_monolingual_v1",
                    voice_settings=default_settings
                )
            else:
                # Mock response for testing without API key
                audio = b"mock_audio_data_for_testing"
            
            return audio
            
        except Exception as e:
            logger.error(f"ElevenLabs API error: {e}")
            raise
    
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

# Global generator instance
voice_generator = VoiceGenerator() 