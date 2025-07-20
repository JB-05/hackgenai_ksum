#!/usr/bin/env python3
"""
Debug script for the /api/workflow/{workflow_id}/enhance endpoint
This script will help identify the root cause of the 500 Internal Server Error
"""

import asyncio
import sys
import os
import traceback
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_environment_variables():
    """Test environment variable loading"""
    print("\n" + "="*60)
    print("🔍 TESTING ENVIRONMENT VARIABLES")
    print("="*60)
    
    # Test .env loading
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ dotenv loaded successfully")
    except Exception as e:
        print(f"❌ dotenv loading failed: {e}")
    
    # Check GEMINI_API_KEY
    gemini_key = os.getenv("GEMINI_API_KEY")
    print(f"🔑 GEMINI_API_KEY: {'✅ Loaded' if gemini_key else '❌ Missing'}")
    if gemini_key:
        print(f"   Key preview: {gemini_key[:10]}...{gemini_key[-4:] if len(gemini_key) > 14 else ''}")
    
    # Check other keys
    openai_key = os.getenv("OPENAI_API_KEY")
    print(f"🔑 OPENAI_API_KEY: {'✅ Loaded' if openai_key else '❌ Missing'}")
    
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    print(f"🔑 ELEVENLABS_API_KEY: {'✅ Loaded' if elevenlabs_key else '❌ Missing'}")

async def test_config_loading():
    """Test config.py loading"""
    print("\n" + "="*60)
    print("🔍 TESTING CONFIG LOADING")
    print("="*60)
    
    try:
        from config import config
        print("✅ config.py imported successfully")
        
        # Test config validation
        try:
            config.validate_config()
            print("✅ Config validation passed")
        except Exception as e:
            print(f"❌ Config validation failed: {e}")
        
        # Test API keys status
        status = config.get_api_keys_status()
        print("📊 API Keys Status:")
        for service, has_key in status.items():
            print(f"   {service}: {'✅' if has_key else '❌'}")
            
    except Exception as e:
        print(f"❌ config.py import failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")

async def test_gemini_client():
    """Test Gemini client initialization"""
    print("\n" + "="*60)
    print("🔍 TESTING GEMINI CLIENT")
    print("="*60)
    
    try:
        from utils.gemini_client import get_gemini_client, GeminiClient
        
        print("✅ gemini_client.py imported successfully")
        
        # Test client creation
        try:
            client = get_gemini_client()
            if client:
                print("✅ Gemini client created successfully")
                
                # Test a simple text generation
                try:
                    test_prompt = "Hello, this is a test prompt."
                    response = await client.generate_text(test_prompt)
                    print(f"✅ Test text generation successful: {response[:100]}...")
                except Exception as e:
                    print(f"❌ Test text generation failed: {e}")
                    print(f"   Traceback: {traceback.format_exc()}")
            else:
                print("❌ Gemini client creation returned None")
                
        except Exception as e:
            print(f"❌ Gemini client creation failed: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            
    except Exception as e:
        print(f"❌ gemini_client.py import failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")

async def test_prompt_enhancer():
    """Test prompt enhancer module"""
    print("\n" + "="*60)
    print("🔍 TESTING PROMPT ENHANCER")
    print("="*60)
    
    try:
        from modules.prompt_enhancer import PromptEnhancer, get_prompt_enhancer
        
        print("✅ prompt_enhancer.py imported successfully")
        
        # Test enhancer creation
        try:
            enhancer = get_prompt_enhancer()
            if enhancer:
                print("✅ Prompt enhancer created successfully")
                
                # Test prompt enhancement
                try:
                    from workflow_models import UserPromptRequest
                    
                    test_request = UserPromptRequest(
                        user_prompt="A brave knight saves a princess from a dragon",
                        title="The Brave Knight",
                        max_scenes=3
                    )
                    
                    print("🔄 Testing prompt enhancement...")
                    enhanced_response = await enhancer.enhance_prompt(test_request)
                    print(f"✅ Prompt enhancement successful!")
                    print(f"   Enhanced story: {enhanced_response.enhanced_story[:100]}...")
                    print(f"   Story title: {enhanced_response.story_title}")
                    print(f"   Estimated scenes: {enhanced_response.estimated_scenes}")
                    
                except Exception as e:
                    print(f"❌ Prompt enhancement failed: {e}")
                    print(f"   Traceback: {traceback.format_exc()}")
            else:
                print("❌ Prompt enhancer creation returned None")
                
        except Exception as e:
            print(f"❌ Prompt enhancer creation failed: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            
    except Exception as e:
        print(f"❌ prompt_enhancer.py import failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")

async def test_workflow_manager():
    """Test workflow manager"""
    print("\n" + "="*60)
    print("🔍 TESTING WORKFLOW MANAGER")
    print("="*60)
    
    try:
        from modules.workflow_manager import get_workflow_manager
        
        print("✅ workflow_manager.py imported successfully")
        
        # Test workflow manager creation
        try:
            manager = get_workflow_manager()
            if manager:
                print("✅ Workflow manager created successfully")
                
                # Test workflow creation
                try:
                    workflow_id = manager.create_workflow()
                    print(f"✅ Workflow created successfully: {workflow_id}")
                    
                    # Test prompt enhancement through workflow
                    try:
                        from workflow_models import UserPromptRequest
                        
                        test_request = UserPromptRequest(
                            user_prompt="A magical forest adventure",
                            title="Forest Adventure",
                            max_scenes=4
                        )
                        
                        print("🔄 Testing workflow prompt enhancement...")
                        enhanced_response = await manager.enhance_prompt(workflow_id, test_request)
                        print(f"✅ Workflow prompt enhancement successful!")
                        print(f"   Enhanced story: {enhanced_response.enhanced_story[:100]}...")
                        
                    except Exception as e:
                        print(f"❌ Workflow prompt enhancement failed: {e}")
                        print(f"   Traceback: {traceback.format_exc()}")
                        
                except Exception as e:
                    print(f"❌ Workflow creation failed: {e}")
                    print(f"   Traceback: {traceback.format_exc()}")
            else:
                print("❌ Workflow manager creation returned None")
                
        except Exception as e:
            print(f"❌ Workflow manager creation failed: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            
    except Exception as e:
        print(f"❌ workflow_manager.py import failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")

async def test_fastapi_endpoint():
    """Test the actual FastAPI endpoint"""
    print("\n" + "="*60)
    print("🔍 TESTING FASTAPI ENDPOINT")
    print("="*60)
    
    try:
        import uvicorn
        from fastapi.testclient import TestClient
        from workflow_api import app
        
        print("✅ FastAPI app imported successfully")
        
        # Create test client
        client = TestClient(app)
        
        # Test health endpoint first
        try:
            response = client.get("/health")
            print(f"✅ Health endpoint: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ Health endpoint failed: {e}")
        
        # Test workflow creation
        try:
            response = client.post("/api/workflow/create")
            print(f"✅ Workflow creation: {response.status_code}")
            if response.status_code == 200:
                workflow_data = response.json()
                workflow_id = workflow_data.get("workflow_id")
                print(f"   Workflow ID: {workflow_id}")
                
                # Test enhance endpoint
                if workflow_id:
                    enhance_data = {
                        "user_prompt": "A space adventure with robots",
                        "title": "Space Robots",
                        "max_scenes": 3
                    }
                    
                    print(f"🔄 Testing enhance endpoint for workflow {workflow_id}...")
                    response = client.post(f"/api/workflow/{workflow_id}/enhance", json=enhance_data)
                    print(f"✅ Enhance endpoint: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   Enhanced story: {result.get('enhanced_story', '')[:100]}...")
                    else:
                        print(f"   Error response: {response.text}")
                        
            else:
                print(f"   Error response: {response.text}")
                
        except Exception as e:
            print(f"❌ Workflow creation/enhance failed: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            
    except Exception as e:
        print(f"❌ FastAPI testing failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")

async def main():
    """Run all debug tests"""
    print("🚀 STARTING COMPREHENSIVE DEBUG OF ENHANCE ENDPOINT")
    print(f"📅 Timestamp: {datetime.now().isoformat()}")
    
    # Run all tests
    await test_environment_variables()
    await test_config_loading()
    await test_gemini_client()
    await test_prompt_enhancer()
    await test_workflow_manager()
    await test_fastapi_endpoint()
    
    print("\n" + "="*60)
    print("🏁 DEBUG COMPLETE")
    print("="*60)
    print("📋 SUMMARY:")
    print("   - Check the output above for any ❌ errors")
    print("   - Most likely issues:")
    print("     1. Missing GEMINI_API_KEY environment variable")
    print("     2. Invalid Gemini API key")
    print("     3. Import errors in modules")
    print("     4. Network connectivity issues")
    print("   - If all tests pass, the issue might be in the frontend request")

if __name__ == "__main__":
    asyncio.run(main()) 