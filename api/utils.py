import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

class FileManager:
    """Utility class for managing files in the save_outputs directory"""
    
    def __init__(self, base_dir: str = "save_outputs"):
        self.base_dir = Path(base_dir)
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.base_dir,
            self.base_dir / "scenes",
            self.base_dir / "images",
            self.base_dir / "audio", 
            self.base_dir / "music",
            self.base_dir / "videos"
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def save_json(self, data: Dict[str, Any], file_type: str, filename: Optional[str] = None) -> str:
        """Save JSON data to a file"""
        if filename is None:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.json"
        
        file_path = self.base_dir / file_type / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved JSON file: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Error saving JSON file: {e}")
            raise
    
    def load_json(self, file_type: str, filename: str) -> Dict[str, Any]:
        """Load JSON data from a file"""
        file_path = self.base_dir / file_type / filename
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded JSON file: {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON file: {e}")
            raise
    
    def save_file(self, content: bytes, file_type: str, filename: str) -> str:
        """Save binary content to a file"""
        file_path = self.base_dir / file_type / filename
        
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"Saved file: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise
    
    def file_exists(self, file_type: str, filename: str) -> bool:
        """Check if a file exists"""
        file_path = self.base_dir / file_type / filename
        return file_path.exists()
    
    def list_files(self, file_type: str) -> List[str]:
        """List all files in a directory"""
        dir_path = self.base_dir / file_type
        if not dir_path.exists():
            return []
        
        files = []
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                files.append(file_path.name)
        return files
    
    def get_file_path(self, file_type: str, filename: str) -> str:
        """Get the full path to a file"""
        file_path = self.base_dir / file_type / filename
        return str(file_path)
    
    def get_file_size(self, file_type: str, filename: str) -> int:
        """Get the size of a file in bytes"""
        file_path = self.base_dir / file_type / filename
        if file_path.exists():
            return file_path.stat().st_size
        return 0

class RetryHandler:
    """Utility class for handling retries with exponential backoff"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def retry_async(self, func, *args, **kwargs):
        """Retry an async function with exponential backoff"""
        import asyncio
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    logger.error(f"Max retries reached for {func.__name__}: {e}")
                    raise
                
                delay = self.base_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s: {e}")
                await asyncio.sleep(delay)
    
    def retry_sync(self, func, *args, **kwargs):
        """Retry a sync function with exponential backoff"""
        import time
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    logger.error(f"Max retries reached for {func.__name__}: {e}")
                    raise
                
                delay = self.base_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s: {e}")
                time.sleep(delay)

class ResponseFormatter:
    """Utility class for formatting API responses"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        """Format a successful response"""
        response = {
            "success": True,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        if data is not None:
            response["data"] = data
        return response
    
    @staticmethod
    def error(message: str, error_code: str = None, details: Any = None) -> Dict[str, Any]:
        """Format an error response"""
        response = {
            "success": False,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        if error_code:
            response["error_code"] = error_code
        if details:
            response["details"] = details
        return response

# Global instances
file_manager = FileManager()
retry_handler = RetryHandler()
response_formatter = ResponseFormatter() 