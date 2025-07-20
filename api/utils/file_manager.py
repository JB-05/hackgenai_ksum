import os
import json
from datetime import datetime

def save_json(data, folder: str, filename: str) -> str:
    """Save data as JSON file"""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filepath

def save_file(content: bytes, folder: str, filename: str) -> str:
    """Save binary content to file"""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    return filepath

def get_file_path(folder: str, filename: str) -> str:
    """Get the full file path"""
    return os.path.join(folder, filename)

def ensure_directory(directory: str) -> None:
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)
