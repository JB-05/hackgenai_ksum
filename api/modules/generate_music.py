"""
Music Generation Module
Generates background music for video scenes using Suno.ai API or placeholder system.
"""

import requests
import logging
import time
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from pathlib import Path
from pydantic import BaseModel

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utilities
from utils import file_manager

logger = logging.getLogger(__name__)

class MusicGenerationRequest(BaseModel):
    story_title: str
    story_text: str
    scenes: List[Dict]
    mood: str = "neutral"  # happy, sad, mysterious, adventurous, calm
    duration: int = 60  # total duration in seconds
    style: str = "ambient"  # ambient, orchestral, electronic, acoustic

class MusicGenerationResponse(BaseModel):
    success: bool
    message: str
    music_file: Optional[str] = None
    duration: Optional[int] = None
    style: Optional[str] = None
    mood: Optional[str] = None

class SunoMusicGenerator:
    """Suno.ai API integration for music generation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.suno.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_music(self, prompt: str, duration: int = 30) -> Optional[str]:
        """
        Generate music using Suno.ai API
        
        Args:
            prompt: Text description of the music to generate
            duration: Duration in seconds (max 30)
            
        Returns:
            File path to generated music or None if failed
        """
        try:
            payload = {
                "prompt": prompt,
                "duration": min(duration, 30),  # Suno.ai limit
                "model": "suno-music-1"
            }
            
            response = requests.post(
                f"{self.base_url}/music/generate",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                audio_url = data.get("audio_url")
                
                if audio_url:
                    # Download the audio file
                    audio_response = requests.get(audio_url, timeout=60)
                    if audio_response.status_code == 200:
                        filename = f"music_{int(time.time())}.mp3"
                        file_manager.save_file(audio_response.content, "music", filename)
                        return file_manager.get_file_path("music", filename)
            
            logger.error(f"Suno.ai API error: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error generating music with Suno.ai: {str(e)}")
            return None

class PlaceholderMusicGenerator:
    """Placeholder music generator for testing without API keys"""
    
    def __init__(self):
        self.mood_prompts = {
            "happy": "Upbeat, cheerful background music with piano and strings",
            "sad": "Melancholic, emotional music with soft piano and cello",
            "mysterious": "Dark, atmospheric music with deep bass and ambient sounds",
            "adventurous": "Epic, action-packed orchestral music with drums and brass",
            "calm": "Peaceful, relaxing ambient music with nature sounds",
            "neutral": "Gentle, unobtrusive background music with soft instruments"
        }
    
    def generate_music(self, prompt: str, duration: int = 30) -> str:
        """
        Generate placeholder music file
        
        Args:
            prompt: Text description (not used in placeholder)
            duration: Duration in seconds
            
        Returns:
            File path to placeholder music file
        """
        try:
            # Create a simple placeholder audio file
            # In a real implementation, this would generate actual audio
            filename = f"placeholder_music_{int(time.time())}.mp3"
            file_manager.save_file(b"placeholder_audio_data", "music", filename)
            
            # Simulate processing time
            time.sleep(2)
            
            filepath = file_manager.get_file_path("music", filename)
            logger.info(f"Generated placeholder music: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating placeholder music: {str(e)}")
            raise

def analyze_story_mood(story_text: str, story_title: str) -> str:
    """
    Analyze story content to determine appropriate mood for music
    
    Args:
        story_text: The story content
        story_title: The story title
        
    Returns:
        Mood string (happy, sad, mysterious, adventurous, calm, neutral)
    """
    text_lower = (story_text + " " + story_title).lower()
    
    # Simple keyword-based mood detection
    happy_keywords = ["happy", "joy", "celebrate", "laugh", "smile", "fun", "cheerful"]
    sad_keywords = ["sad", "cry", "tear", "grief", "loss", "death", "mourn", "sorrow"]
    mysterious_keywords = ["mystery", "secret", "hidden", "dark", "shadow", "unknown", "strange"]
    adventurous_keywords = ["adventure", "journey", "quest", "battle", "fight", "hero", "explore"]
    calm_keywords = ["peace", "quiet", "gentle", "soft", "calm", "serene", "tranquil"]
    
    scores = {
        "happy": sum(1 for word in happy_keywords if word in text_lower),
        "sad": sum(1 for word in sad_keywords if word in text_lower),
        "mysterious": sum(1 for word in mysterious_keywords if word in text_lower),
        "adventurous": sum(1 for word in adventurous_keywords if word in text_lower),
        "calm": sum(1 for word in calm_keywords if word in text_lower)
    }
    
    # Find the mood with highest score
    max_score = max(scores.values())
    if max_score > 0:
        for mood, score in scores.items():
            if score == max_score:
                return mood
    
    return "neutral"

def create_music_prompt(story_title: str, story_text: str, scenes: List[Dict], mood: str, style: str) -> str:
    """
    Create a detailed prompt for music generation
    
    Args:
        story_title: The story title
        story_text: The story content
        scenes: List of scene descriptions
        mood: The desired mood
        style: The desired style
        
    Returns:
        Formatted prompt for music generation
    """
    # Extract key themes from scenes
    scene_themes = []
    for scene in scenes:
        description = scene.get("description", "")
        if description:
            # Extract key words from scene description
            words = description.split()[:5]  # First 5 words
            scene_themes.extend(words)
    
    # Create a comprehensive prompt
    prompt_parts = [
        f"Background music for a story titled '{story_title}'",
        f"Mood: {mood}",
        f"Style: {style}",
        f"Story theme: {story_text[:100]}...",
    ]
    
    if scene_themes:
        prompt_parts.append(f"Scene themes: {', '.join(set(scene_themes))}")
    
    prompt_parts.extend([
        "The music should be:",
        "- Non-intrusive and supportive of narration",
        "- Emotionally appropriate for the story content",
        "- Smooth transitions between different moods",
        "- Professional quality suitable for video production"
    ])
    
    return ". ".join(prompt_parts)

# Global music generator instance
_music_generator = None

def get_music_generator():
    """Get the global music generator instance"""
    global _music_generator
    if _music_generator is None:
        _music_generator = PlaceholderMusicGenerator()
    return _music_generator

# For backward compatibility
generator = get_music_generator()

def generate_music_for_story(story_title: str, story_text: str, scenes: List[Dict], mood: str = "adventurous", duration: int = 120, style: str = "orchestral"):
    """Generate background music for a story"""
    return get_music_generator().generate_music_for_story(story_title, story_text, scenes, mood, duration, style)

# Export the main function
__all__ = ["generate_music_for_story", "MusicGenerationRequest", "MusicGenerationResponse"] 