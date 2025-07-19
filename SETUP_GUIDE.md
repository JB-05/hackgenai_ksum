# 🚀 Story-to-Video Generator - Setup Guide

This guide will help you set up the Story-to-Video Generator with real API integration and working file downloads.

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **API Keys** for the following services:
  - OpenAI (GPT-4 + DALL-E 3)
  - ElevenLabs (Voice synthesis)
  - Suno.ai (Music generation) - Optional

## 🔧 Quick Setup

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend-nextjs
npm install
cd ..
```

### 2. Configure Environment Variables

```bash
# Copy the environment template
cp env_example.txt .env

# Edit .env file with your API keys
```

**Required API Keys:**
```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs API Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Suno.ai API Configuration (optional)
SUNO_API_KEY=your_suno_api_key_here
```

### 3. Test Imports (Optional but Recommended)

```bash
# Test that all imports work correctly
python test_imports.py
```

### 4. Start the Application

**Option A: Using Batch Files (Windows)**
```bash
# Terminal 1: Start Backend
start_backend.bat

# Terminal 2: Start Frontend
start_frontend.bat
```

**Option B: Manual Start**
```bash
# Terminal 1: Start Backend
cd api
python main.py

# Terminal 2: Start Frontend
cd frontend-nextjs
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Testing the Setup

Run the test script to verify everything is working:

```bash
python test_backend.py
```

You should see:
```
🧪 Testing Backend API...

1. Testing health check...
✅ Health check passed: {...}

2. Testing workflow creation...
✅ Workflow created: {workflow_id}

3. Testing prompt enhancement...
✅ Prompt enhanced: The Magical Library

4. Testing generation confirmation...
✅ Generation confirmed: confirmed

5. Testing workflow status...
✅ Workflow status: generation

🎉 All tests passed! Backend is working correctly.
✅ Backend is ready for frontend integration!
```

## 🔄 How It Works

### Frontend Workflow
1. **Phase 1**: User enters a story prompt
2. **Phase 2**: AI enhances the prompt into a full story
3. **Phase 3**: User reviews and confirms the enhanced story
4. **Phase 4**: Real-time generation with progress tracking
5. **Phase 5**: Download generated files (video, audio, music)

### Backend Process
1. **Prompt Enhancement**: Uses GPT-4 to expand user prompts
2. **Scene Breakdown**: Analyzes story and creates visual scenes
3. **Image Generation**: Creates images for each scene using DALL-E 3
4. **Voice Synthesis**: Generates professional narration using ElevenLabs
5. **Music Generation**: Creates background music using Suno.ai
6. **Video Assembly**: Combines all elements into final video

## 📁 File Structure

```
hackgenai-ksum/
├── api/                    # FastAPI backend
│   ├── modules/           # AI processing modules
│   ├── workflow_api.py    # Main API endpoints
│   └── workflow_models.py # Data models
├── frontend-nextjs/       # Next.js frontend
│   ├── components/        # React components
│   └── lib/api.ts         # API integration
├── save_outputs/          # Generated files
│   ├── images/           # Generated images
│   ├── audio/            # Voice narration
│   ├── music/            # Background music
│   └── videos/           # Final videos
└── test_backend.py        # Backend test script
```

## 🛠️ Troubleshooting

### Common Issues

**1. Backend won't start**
```bash
# Test imports first
python test_imports.py

# Check if dependencies are installed
pip install -r requirements.txt

# Check if .env file exists
ls .env

# Check if API keys are valid
python test_backend.py
```

**2. Frontend can't connect to backend**
```bash
# Verify backend is running on port 8000
curl http://localhost:8000/health

# Check frontend API configuration
# frontend-nextjs/lib/api.ts should point to http://localhost:8000
```

**3. File downloads don't work**
```bash
# Check if save_outputs directory exists
ls save_outputs/

# Check file permissions
chmod -R 755 save_outputs/
```

**4. Generation fails**
```bash
# Check API keys in .env file
cat .env

# Check backend logs for errors
# Look for specific error messages in the terminal
```

### API Key Setup

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to .env file: `OPENAI_API_KEY=sk-...`

**ElevenLabs API Key:**
1. Go to https://elevenlabs.io/
2. Sign up and get your API key
3. Add to .env file: `ELEVENLABS_API_KEY=...`

**Suno.ai API Key (Optional):**
1. Go to https://suno.ai/
2. Get your API key
3. Add to .env file: `SUNO_API_KEY=...`

## 🎯 Features

### ✅ Working Features
- Real-time API integration
- Progress tracking during generation
- File downloads (video, audio, music)
- Error handling and user feedback
- Modern, responsive UI

### 🔄 Real-time Updates
- Live progress tracking
- Status updates every 2 seconds
- Automatic completion detection
- Error handling with retry logic

### 📁 File Downloads
- Video files (MP4 format)
- Audio narration (MP3 format)
- Background music (MP3 format)
- Proper file paths and sizes

## 🚀 Production Deployment

For production deployment:

1. **Environment Variables**: Set proper production values
2. **Database**: Use PostgreSQL instead of in-memory storage
3. **File Storage**: Use cloud storage (AWS S3, etc.)
4. **Security**: Add authentication and rate limiting
5. **Monitoring**: Add logging and monitoring

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run `python test_backend.py` to verify backend functionality
3. Check browser console for frontend errors
4. Review backend logs for detailed error messages

## 🎉 Success!

Once everything is set up correctly, you should be able to:

1. Enter a story prompt
2. See AI-enhanced story
3. Confirm generation
4. Watch real-time progress
5. Download generated video and assets

The application now works with real API calls and generates actual files instead of using static data! 