# 🎬 Story-to-Video Generator - Workflow Edition

A complete AI-powered workflow that transforms user prompts into professional videos with images, voice narration, and background music.

## 🚀 New Workflow Approach

The project now follows a **user-controlled workflow**:

1. **📝 User Input**: User provides a story prompt
2. **✨ Enhancement**: AI enhances the prompt into a complete story
3. **✅ User Confirmation**: User reviews and decides whether to proceed
4. **🎬 Generation**: Only if confirmed, generates video, sound effects, and music
5. **🎉 Final Output**: Provides story structure/script and the final video

## 🏗️ Project Structure

```
hackgenai-ksum/
├── api/
│   ├── workflow_models.py          # Workflow data models
│   ├── workflow_api.py             # Main workflow API endpoints
│   ├── modules/
│   │   ├── prompt_enhancer.py      # Enhances user prompts
│   │   ├── workflow_manager.py     # Manages complete workflow
│   │   ├── story_to_scenes.py      # Breaks stories into scenes
│   │   ├── generate_image.py       # Generates images
│   │   ├── generate_voice.py       # Generates voice narration
│   │   └── generate_music.py       # Generates background music
│   └── ...
├── frontend-nextjs/                # Next.js frontend (recommended)
│   ├── app/                        # App router pages
│   ├── components/                 # React components
│   └── ...
└── WORKFLOW_README.md              # This file
```

## 🛠️ Installation & Setup

### 1. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file based on `env_example.txt`:
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs API Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Suno.ai API Configuration (for music generation)
SUNO_API_KEY=your_suno_api_key_here

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# File Storage Configuration
SAVE_OUTPUTS_DIR=save_outputs
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

### 3. Start the Workflow API
```bash
cd api
uvicorn workflow_api:app --reload
```

### 4. Choose Your Frontend

#### Option A: Next.js Frontend (Recommended)
```bash
cd frontend-nextjs
npm install
npm run dev
```
Then open [http://localhost:3000](http://localhost:3000)

#### Option B: Streamlit Frontend (Legacy)
```bash
cd frontend
streamlit run workflow_app.py
```
Then open [http://localhost:8501](http://localhost:8501)

## 🎯 How to Use

### Option 1: Next.js Web Interface (Recommended)
1. Open your browser to `http://localhost:3000`
2. Follow the 5-phase workflow:
   - **Phase 1**: Enter your story prompt
   - **Phase 2**: Review the enhanced story
   - **Phase 3**: Confirm generation
   - **Phase 4**: Wait for generation
   - **Phase 5**: Download your video

### Option 2: Streamlit Web Interface
1. Open your browser to `http://localhost:8501`
2. Follow the same 5-phase workflow

### Option 2: API Direct Usage
```python
import requests

# 1. Create workflow
response = requests.post("http://localhost:8000/api/workflow/create")
workflow_id = response.json()["workflow_id"]

# 2. Enhance prompt
enhance_data = {
    "user_prompt": "A young wizard discovers a magical library",
    "title": "The Magical Library",
    "max_scenes": 4
}
response = requests.post(
    f"http://localhost:8000/api/workflow/{workflow_id}/enhance",
    json=enhance_data
)
enhanced_story = response.json()

# 3. Confirm generation
confirm_data = {
    "enhanced_story": enhanced_story["enhanced_story"],
    "story_title": enhanced_story["story_title"],
    "max_scenes": enhanced_story["estimated_scenes"],
    "proceed": True
}
response = requests.post(
    f"http://localhost:8000/api/workflow/{workflow_id}/confirm",
    json=confirm_data
)

# 4. Generate video
response = requests.post(
    f"http://localhost:8000/api/workflow/{workflow_id}/generate"
)
final_result = response.json()
```

### Option 3: Demo Script (Removed)
The demo script has been removed to clean up the codebase. You can test the workflow using the Next.js frontend or direct API calls.

## 🔄 Workflow Phases

### Phase 1: Prompt Input
- User enters a story prompt (minimum 10 characters)
- Optional: Provide story title and scene count
- System validates input and creates workflow

### Phase 2: Enhancement
- AI enhances the prompt into a complete story (300-500 words)
- Adds character development, plot elements, and visual descriptions
- Provides enhancement notes explaining what was added
- User can review before proceeding

### Phase 3: User Confirmation
- User reviews the enhanced story
- System shows what will be generated (video, images, voice, music)
- User decides whether to proceed with generation
- If cancelled, workflow is cleaned up

### Phase 4: Generation
- **Scene Breakdown**: Story is broken into scenes
- **Image Generation**: AI generates images for each scene
- **Voice Synthesis**: Story is converted to professional narration
- **Music Generation**: Background music is created
- **Video Assembly**: All elements are combined into final video

### Phase 5: Final Output
- **Story Script**: Complete script with scene breakdown
- **Video File**: Final MP4 video
- **Audio Files**: Separate narration and music files
- **Download Links**: Easy download of all assets

## 📊 API Endpoints

### Workflow Management
- `POST /api/workflow/create` - Create new workflow
- `GET /api/workflow/list` - List all workflows
- `DELETE /api/workflow/{id}/cleanup` - Clean up workflow

### Workflow Phases
- `POST /api/workflow/{id}/enhance` - Enhance user prompt
- `POST /api/workflow/{id}/confirm` - User confirmation
- `POST /api/workflow/{id}/generate` - Generate complete video

### Status & Results
- `GET /api/workflow/{id}/status` - Get workflow status
- `GET /api/workflow/{id}/progress` - Get generation progress
- `GET /api/workflow/{id}/result` - Get final result

### File Downloads
- `GET /files/{type}/{filename}` - Download generated files

## 🎨 Features

### Prompt Enhancement
- **AI-Powered**: Uses GPT-4 to expand simple prompts
- **Story Structure**: Ensures beginning, middle, and end
- **Visual Focus**: Adds descriptions suitable for video
- **Character Development**: Creates engaging characters
- **Plot Enhancement**: Adds conflict and resolution

### Video Generation
- **Scene Breakdown**: Automatic scene identification
- **Image Generation**: DALL-E 3 powered scene images
- **Voice Narration**: ElevenLabs professional voice synthesis
- **Background Music**: Suno.ai mood-matched music
- **Video Assembly**: Complete video with all elements

### User Control
- **Review Phase**: Users can review before generation
- **Cancellation**: Users can cancel at any time
- **Progress Tracking**: Real-time generation progress
- **File Management**: Easy download of all assets

## 🔧 Configuration

### API Keys Required
- **OpenAI**: For prompt enhancement and image generation
- **ElevenLabs**: For voice synthesis
- **Suno.ai**: For background music generation

### Performance Settings
- **Scene Count**: 3-6 scenes per story
- **Image Style**: Realistic, artistic, cartoon, cinematic, fantasy
- **Voice Options**: Multiple voice types available
- **Music Styles**: Ambient, orchestral, electronic, acoustic

## 📁 Output Files

### Generated Assets
- `video_{workflow_id}.mp4` - Final video
- `voice_{voice_id}.mp3` - Narration audio
- `music_{timestamp}.mp3` - Background music
- `scene_{number}.png` - Scene images

### Metadata Files
- `scenes_{timestamp}.json` - Scene breakdown
- `workflow_{id}_result.json` - Complete workflow result

## 🧪 Testing

### Run Complete Demo
```bash
python test_workflow_demo.py
```

### Test Individual Components
```bash
python test_all_models_fixed.py
python test_sample_story.py
```

### API Testing
```bash
# Test workflow API
curl http://localhost:8000/health

# Test workflow creation
curl -X POST http://localhost:8000/api/workflow/create
```

## 🚀 Deployment

### Local Development
1. Start API: `python api/workflow_api.py`
2. Start Frontend: `streamlit run frontend/workflow_app.py`
3. Access: `http://localhost:8501`

### Production Deployment
1. Set up environment variables
2. Use production WSGI server (Gunicorn)
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Monitor API usage and costs

## 💡 Best Practices

### Prompt Writing
- **Be Specific**: Include characters, setting, and conflict
- **Visual Details**: Describe scenes that can be illustrated
- **Story Arc**: Include beginning, middle, and end
- **Length**: 10-200 characters for best enhancement

### Cost Management
- **Review Before Generation**: Use enhancement phase to avoid unnecessary costs
- **Monitor Usage**: Track API calls and costs
- **Optimize Settings**: Adjust scene count and quality settings
- **Cache Results**: Reuse generated content when possible

### Quality Control
- **Review Enhanced Stories**: Check AI enhancements before proceeding
- **Test Different Styles**: Experiment with image and music styles
- **Validate Outputs**: Ensure generated files meet quality standards
- **User Feedback**: Collect feedback to improve the system

## 🐛 Troubleshooting

### Common Issues
1. **API Connection Failed**: Ensure API server is running
2. **Enhancement Failed**: Check OpenAI API key and quota
3. **Generation Failed**: Verify all API keys are set
4. **File Not Found**: Check file permissions and paths

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python api/workflow_api.py
```

## 📈 Future Enhancements

### Planned Features
- **WebSocket Support**: Real-time progress updates
- **Batch Processing**: Multiple stories at once
- **Custom Styles**: User-defined image and music styles
- **Video Templates**: Pre-made video templates
- **Social Sharing**: Direct sharing to social platforms
- **Collaboration**: Multi-user story creation

### API Improvements
- **Rate Limiting**: Prevent API abuse
- **Caching**: Cache generated content
- **Compression**: Optimize file sizes
- **CDN Integration**: Faster file delivery

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**🎉 Happy Storytelling!** Transform your ideas into amazing videos with AI-powered creativity. 