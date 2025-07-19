# Story-to-Video Generator

An AI-powered web application that transforms text stories into multimedia presentations with AI-generated images, voice narration, background music, and final video compilation.

## Features

- **Interactive Workflow**: User prompt enhancement with confirmation before generation
- **Scene Breakdown**: AI analysis to extract key scenes from stories
- **Image Generation**: DALL-E 3 powered scene visualization
- **Voice Synthesis**: ElevenLabs AI voice narration
- **Music Generation**: Background music matching story mood
- **Video Creation**: Automated slideshow compilation
- **Modern UI**: Next.js frontend with real-time progress tracking

## Project Structure

```
hackgenai-ksum/
├── api/                    # Backend API server
│   ├── modules/           # Core AI modules
│   ├── workflow_api.py    # Main workflow API
│   ├── workflow_models.py # Pydantic models
│   └── ...
├── frontend-nextjs/       # Next.js frontend
│   ├── app/              # App router pages
│   ├── components/       # React components
│   └── ...
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

1. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp env_example.txt .env
   # Add your API keys to .env
   ```

3. Run the backend:
   ```bash
   cd api
   uvicorn workflow_api:app --reload
   ```

4. Run the frontend:
   ```bash
   cd frontend-nextjs
   npm install
   npm run dev
   ```

## Workflow API Endpoints

- `POST /api/workflow/create` - Create new workflow
- `POST /api/workflow/{id}/enhance` - Enhance user prompt
- `POST /api/workflow/{id}/confirm` - User confirmation
- `POST /api/workflow/{id}/generate` - Generate complete video
- `GET /api/workflow/{id}/status` - Get workflow status
- `GET /api/workflow/{id}/progress` - Get generation progress
- `GET /api/workflow/{id}/result` - Get final result

## Workflow Phases

1. **Prompt Enhancement**: AI enhances user's story prompt
2. **User Confirmation**: User reviews enhanced story and confirms
3. **Generation**: System generates images, voice, music, and video
4. **Completion**: Final video and assets are delivered 