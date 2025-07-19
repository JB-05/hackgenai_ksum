# Story-to-Video Generator

An AI-powered web application that transforms text stories into multimedia presentations with AI-generated images, voice narration, background music, and final video compilation.

## Features

- **Scene Breakdown**: AI analysis to extract key scenes from stories
- **Image Generation**: DALL-E 3 powered scene visualization
- **Voice Synthesis**: ElevenLabs AI voice narration
- **Music Generation**: Background music matching story mood
- **Video Creation**: Automated slideshow compilation

## Project Structure

```
hackgenai-ksum/
├── api/                    # Backend API server
├── frontend/              # Streamlit frontend
├── save_outputs/          # Generated files storage
│   ├── scenes/           # Scene breakdowns
│   ├── images/           # Generated images
│   ├── audio/            # Voice narration
│   ├── music/            # Background music
│   └── videos/           # Final videos
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

3. Run the backend:
   ```bash
   cd api
   uvicorn main:app --reload
   ```

4. Run the frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

## API Endpoints

- `POST /story-to-scenes` - Break story into scenes
- `POST /generate-image` - Generate image for scene
- `POST /generate-voice` - Generate voice narration
- `POST /generate-music` - Generate background music
- `POST /create-slideshow` - Create final video 