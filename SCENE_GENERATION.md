# Scene Generation with Google Gemini

This document describes the scene generation functionality that uses Google Gemini to break down stories into video scenes.

## Overview

The scene generation system:
- **Accepts**: Story text + title + scene count
- **Processes**: Uses Gemini Pro for intelligent scene breakdown
- **Returns**: Structured scene data with descriptions and image prompts
- **Supports**: Regeneration for different scene interpretations

## API Endpoints

### 1. Generate Scenes
```http
POST /api/workflow/{workflow_id}/scenes
```

**Request Body:**
```json
{
  "story_text": "Your story content here...",
  "title": "Story Title",
  "max_scenes": 4
}
```

**Response:**
```json
{
  "story_title": "Story Title",
  "scenes": [
    {
      "scene_number": 1,
      "description": "Brief scene description",
      "prompt": "Detailed image generation prompt",
      "duration": 5
    }
  ],
  "total_scenes": 4,
  "processing_time": 2.34
}
```

### 2. Regenerate Scenes
```http
POST /api/workflow/{workflow_id}/scenes/regenerate
```

Same request/response format as generate, but creates a new scene breakdown.

## Implementation Details

### Core Components

#### StoryToScenesProcessor (`api/modules/story_to_scenes.py`)
- **Main class** for scene generation
- **Gemini integration** using `get_gemini_client()`
- **Robust error handling** with fallback scenarios
- **JSON parsing** with regex extraction

#### Key Methods

```python
# Process story into scenes
async def process_story(request: StoryRequest) -> SceneBreakdownResponse

# Regenerate scenes (same input, different output)
async def regenerate_scenes(request: StoryRequest) -> SceneBreakdownResponse

# Internal processing with error handling
async def _process_story_internal(request: StoryRequest, is_regenerate: bool) -> SceneBreakdownResponse
```

### Prompt Engineering

The system uses a detailed prompt structure:

```
You are an expert story analyst and video director. Your task is to break down the following story into exactly {max_scenes} key scenes that will be used to create a compelling video.

STORY DETAILS:
Title: {title}
Story: {story_text}

ANALYSIS INSTRUCTIONS:
1. Read the story carefully and identify the {max_scenes} most important narrative moments
2. Each scene should represent a distinct event, location change, or emotional turning point
3. Ensure the scenes flow chronologically and cover the entire story arc
4. Consider visual storytelling - each scene should be visually distinct and engaging

SCENE REQUIREMENTS:
- Scene descriptions: Clear, concise summaries (1-2 sentences)
- Image prompts: Detailed, visual descriptions suitable for AI image generation
- Duration: Each scene should be 5 seconds for optimal video pacing
- Visual variety: Ensure scenes have different settings, lighting, or moods

OUTPUT FORMAT (Valid JSON only):
{
    "scenes": [
        {
            "scene_number": 1,
            "description": "Brief scene description that captures the key moment",
            "prompt": "Detailed visual prompt for image generation including setting, lighting, mood, characters, and style",
            "duration": 5
        }
    ]
}
```

### Error Handling & Fallbacks

#### 1. Empty Gemini Response
- **Detection**: Check if response is empty or whitespace
- **Fallback**: Use story sentences to create basic scenes
- **Logging**: Warning message with fallback notification

#### 2. Malformed JSON
- **Detection**: JSON parsing exceptions
- **Fallback**: Regex extraction of JSON blocks
- **Logging**: Error details and raw response for debugging

#### 3. Missing Scene Fields
- **Detection**: KeyError when accessing scene data
- **Fallback**: Skip invalid scenes, create additional ones
- **Logging**: Warning for each missing field

#### 4. Insufficient Scenes
- **Detection**: Generated scenes < requested scenes
- **Fallback**: Create additional placeholder scenes
- **Logging**: Warning about scene count mismatch

### Input Validation

```python
# Story text validation
if not request.story_text or len(request.story_text.strip()) < 10:
    raise ValueError("Story text must be at least 10 characters long")

# Scene count validation
if request.max_scenes < 2 or request.max_scenes > 6:
    raise ValueError("Max scenes must be between 2 and 6")
```

## Usage Examples

### Basic Scene Generation

```python
from api.modules.story_to_scenes import get_story_processor
from api.models import StoryRequest

async def generate_scenes():
    processor = get_story_processor()
    
    request = StoryRequest(
        story_text="A robot learns to paint and discovers creativity.",
        title="Robot Artist",
        max_scenes=3
    )
    
    response = await processor.process_story(request)
    print(f"Generated {response.total_scenes} scenes")
    
    for scene in response.scenes:
        print(f"Scene {scene.scene_number}: {scene.description}")
```

### Scene Regeneration

```python
async def regenerate_scenes():
    processor = get_story_processor()
    
    request = StoryRequest(
        story_text="A robot learns to paint and discovers creativity.",
        title="Robot Artist",
        max_scenes=4
    )
    
    # First generation
    response1 = await processor.process_story(request)
    
    # Regeneration (different interpretation)
    response2 = await processor.regenerate_scenes(request)
    
    # Compare results
    print(f"Original: {response1.total_scenes} scenes")
    print(f"Regenerated: {response2.total_scenes} scenes")
```

### API Usage

```bash
# Generate scenes
curl -X POST "http://localhost:8000/api/workflow/123/scenes" \
  -H "Content-Type: application/json" \
  -d '{
    "story_text": "A robot learns to paint and discovers creativity.",
    "title": "Robot Artist",
    "max_scenes": 3
  }'

# Regenerate scenes
curl -X POST "http://localhost:8000/api/workflow/123/scenes/regenerate" \
  -H "Content-Type: application/json" \
  -d '{
    "story_text": "A robot learns to paint and discovers creativity.",
    "title": "Robot Artist",
    "max_scenes": 3
  }'
```

## Test Cases

### Automated Testing

Run the test suite:

```bash
cd api
python test_scenes.py
```

### Test Scenarios

1. **Empty Gemini Response**
   - Test with very short story
   - Verify fallback scene creation
   - Check logging output

2. **Malformed JSON**
   - Test with complex story text
   - Verify JSON extraction
   - Check error handling

3. **Short vs Long Stories**
   - Test with minimal story (10 chars)
   - Test with detailed story (500+ chars)
   - Verify scene count consistency

4. **Repeated Regenerate**
   - Generate scenes multiple times
   - Compare results
   - Verify different interpretations

5. **Edge Cases**
   - Maximum scenes (6)
   - Minimum scenes (2)
   - Invalid input handling

## Integration with Frontend

### Workflow Integration

The scene generation integrates with the existing workflow:

1. **Phase 1**: User enters story prompt
2. **Phase 2**: Story enhancement with Gemini
3. **Phase 3**: Scene breakdown (NEW)
4. **Phase 4**: User confirmation
5. **Phase 5**: Video generation

### Frontend API Calls

```javascript
// Generate scenes
const scenesResponse = await fetch(`/api/workflow/${workflowId}/scenes`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    story_text: enhancedStory.enhanced_story,
    title: enhancedStory.story_title,
    max_scenes: enhancedStory.estimated_scenes
  })
});

// Regenerate scenes
const regenerateResponse = await fetch(`/api/workflow/${workflowId}/scenes/regenerate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    story_text: enhancedStory.enhanced_story,
    title: enhancedStory.story_title,
    max_scenes: enhancedStory.estimated_scenes
  })
});
```

## Performance Considerations

### Response Times
- **Typical**: 2-5 seconds for scene generation
- **Long stories**: 3-8 seconds
- **Regeneration**: Similar to initial generation

### Token Usage
- **Input tokens**: ~500-2000 depending on story length
- **Output tokens**: ~300-800 for scene descriptions
- **Total**: ~800-2800 tokens per request

### Caching
- Scene breakdowns are saved to JSON files
- Filenames include timestamp and regenerate flag
- Useful for debugging and analysis

## Troubleshooting

### Common Issues

1. **"Story processor not available"**
   - Check Gemini API key configuration
   - Verify `get_gemini_client()` returns valid client
   - Check environment variables

2. **"No scenes generated"**
   - Story text too short (< 10 characters)
   - Gemini response parsing failed
   - Check fallback scene creation

3. **"Invalid JSON response"**
   - Gemini returned malformed JSON
   - Check regex extraction
   - Review raw response in logs

4. **"Missing scene fields"**
   - Scene data incomplete
   - Check scene object creation
   - Verify required fields

### Debug Mode

Enable detailed logging:

```python
import logging
logging.getLogger('api.modules.story_to_scenes').setLevel(logging.DEBUG)
```

### Log Analysis

Key log messages to monitor:

```
INFO: Processing story: Story Title
DEBUG: [JSON Extracted] {"scenes": [...}
INFO: Scene breakdown completed: 4 scenes in 2.34s
WARNING: ⚠️ No JSON block found in Gemini response
ERROR: ❌ JSON parsing failed: Expecting property name
```

## Future Enhancements

### Planned Features
1. **Scene Templates**: Pre-defined scene structures
2. **Style Variations**: Different scene breakdown styles
3. **Batch Processing**: Multiple stories at once
4. **Scene Optimization**: AI-powered scene refinement

### Integration Opportunities
1. **Image Generation**: Direct integration with image services
2. **Video Templates**: Scene-to-video mapping
3. **User Preferences**: Customizable scene generation
4. **Analytics**: Scene generation metrics and insights

## Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
GEMINI_MODEL=gemini-pro
GEMINI_MAX_TOKENS=2048
```

### Model Settings

```python
# Generation config
generation_config = genai.types.GenerationConfig(
    max_output_tokens=2048,
    temperature=0.8,
    top_p=0.9,
    top_k=40
)
```

## Support

For issues related to:
- **Scene Generation**: Check this documentation
- **API Integration**: Review endpoint examples
- **Error Handling**: Check troubleshooting section
- **Performance**: Monitor response times and token usage 