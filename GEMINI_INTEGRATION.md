# Google Gemini Integration

This document describes the integration of Google Gemini AI services to replace OpenAI for text generation and enhance the video generation pipeline.

## Overview

The application has been updated to use Google Gemini Pro for:
- **Text Generation**: Story enhancement and scene breakdown
- **Prompt Enhancement**: Improving image generation prompts
- **Future Image Generation**: Using Gemini Pro Vision for image analysis (when available)

## Configuration

### Environment Variables

Add the following to your `.env` file:

```bash
# Google Gemini API Configuration (Required)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
GEMINI_VISION_MODEL=gemini-pro-vision
GEMINI_MAX_TOKENS=2048

# OpenAI API Configuration (Optional - for image generation fallback)
OPENAI_API_KEY=your_openai_api_key_here
```

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## Installation

Install the required dependencies:

```bash
pip install google-generativeai==0.3.2
```

Or update your `requirements.txt`:

```
google-generativeai==0.3.2
```

## Architecture Changes

### 1. New Gemini Client (`api/utils/gemini_client.py`)

- **GeminiClient**: Wrapper around Google Generative AI SDK
- **Error Handling**: Graceful handling of quota, auth, and content policy errors
- **Retry Logic**: Exponential backoff for failed requests
- **Text Generation**: Async methods for generating text with system prompts

### 2. Updated Modules

#### Prompt Enhancer (`api/modules/prompt_enhancer.py`)
- Replaced OpenAI with Gemini Pro
- Enhanced JSON parsing with better error handling
- Maintains compatibility with existing response format

#### Story to Scenes (`api/modules/story_to_scenes.py`)
- Uses Gemini Pro for scene breakdown
- Improved JSON extraction and fallback handling
- Better logging for debugging

#### Image Generator (`api/modules/generate_image.py`)
- Flexible approach supporting both DALL-E and Gemini
- Fallback to OpenAI for image generation if available
- Uses Gemini for prompt enhancement

### 3. Configuration Updates (`api/config.py`)

- Added Gemini-specific configuration
- Updated validation to require Gemini API key
- Enhanced API key status reporting

## Features

### Text Generation
- **Story Enhancement**: Converts user prompts into complete stories
- **Scene Breakdown**: Analyzes stories and creates scene descriptions
- **JSON Output**: Maintains structured output format for compatibility

### Error Handling
- **Quota Management**: Handles rate limits and quota exceeded errors
- **Authentication**: Validates API keys and handles auth errors
- **Content Policy**: Manages safety filter violations
- **Fallback Logic**: Graceful degradation when services are unavailable

### Retry Logic
- **Exponential Backoff**: Intelligent retry with increasing delays
- **Max Retries**: Configurable retry attempts
- **Error Logging**: Detailed logging for debugging

## Usage Examples

### Basic Text Generation

```python
from api.utils.gemini_client import get_gemini_client

client = get_gemini_client()
response = await client.generate_text(
    "Write a short story about a robot learning to paint",
    "You are a creative storyteller."
)
```

### With Retry Logic

```python
response = await client.generate_text_with_retry(
    "Enhance this story prompt",
    "You are a story enhancer.",
    max_retries=3
)
```

### Error Handling

```python
try:
    response = await client.generate_text(prompt)
except Exception as e:
    error_info = client.handle_gemini_error(e)
    print(f"Error: {error_info['message']}")
```

## Migration from OpenAI

### What Changed
1. **API Client**: Replaced OpenAI client with Gemini client
2. **Model Names**: Updated to use Gemini Pro models
3. **Error Handling**: Enhanced with Gemini-specific error types
4. **Configuration**: Added Gemini API key requirement

### What Stayed the Same
1. **Response Format**: JSON output structure unchanged
2. **API Endpoints**: Frontend API remains the same
3. **Workflow**: User experience unchanged
4. **Fallback Behavior**: Similar error handling patterns

## Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   🚨 Missing required environment variables: ['GEMINI_API_KEY']
   ```
   Solution: Add your Gemini API key to `.env`

2. **Quota Exceeded**
   ```
   🚨 Gemini API quota exceeded or rate limited
   ```
   Solution: Wait for quota reset or upgrade plan

3. **Content Policy Violation**
   ```
   🚨 Gemini content policy violation
   ```
   Solution: Modify your prompt to comply with safety policies

4. **Authentication Error**
   ```
   🚨 Gemini API authentication error
   ```
   Solution: Check your API key is correct and valid

### Debug Mode

Enable debug logging to see detailed API interactions:

```python
import logging
logging.getLogger('api.utils.gemini_client').setLevel(logging.DEBUG)
```

## Performance

### Token Limits
- **Gemini Pro**: 30,720 tokens (input + output)
- **Configurable**: Adjust `GEMINI_MAX_TOKENS` in config

### Response Times
- **Typical**: 2-5 seconds for story enhancement
- **Scene Breakdown**: 1-3 seconds per story
- **Retry Delays**: Exponential backoff (1s, 2s, 4s)

## Future Enhancements

### Planned Features
1. **Image Generation**: Full Gemini Pro Vision integration
2. **Video Generation**: Text-to-video capabilities
3. **Multi-modal**: Combined text and image processing
4. **Streaming**: Real-time response streaming

### Integration Opportunities
1. **Google Cloud**: Integration with other Google AI services
2. **Vertex AI**: Enterprise-grade AI platform
3. **Custom Models**: Fine-tuned models for specific use cases

## Support

For issues related to:
- **Gemini API**: Check [Google AI Studio documentation](https://ai.google.dev/docs)
- **Integration**: Review this documentation and code examples
- **Configuration**: Verify environment variables and API keys

## License

This integration follows the same license as the main project. Ensure compliance with Google's API terms of service. 