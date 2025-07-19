#!/usr/bin/env python3
"""
Main entry point for the Story-to-Video Generator API
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print(f"🚀 Starting Story-to-Video Generator API on {host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🏥 Health Check: http://{host}:{port}/health")
    print("Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(
        "workflow_api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    ) 