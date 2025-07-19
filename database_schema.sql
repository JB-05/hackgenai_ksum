-- Story-to-Video Generator Database Schema
-- SQLite database for storing workflows, files, and metadata

-- Users table (for future user management)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflows table (main workflow tracking)
CREATE TABLE IF NOT EXISTS workflows (
    id VARCHAR(36) PRIMARY KEY,  -- UUID
    user_id INTEGER,  -- NULL for anonymous users
    original_prompt TEXT NOT NULL,
    enhanced_story TEXT,
    story_title VARCHAR(255),
    max_scenes INTEGER DEFAULT 4,
    current_phase VARCHAR(50) DEFAULT 'prompt_enhancement',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_processing_time REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Generated files table (track all generated assets)
CREATE TABLE IF NOT EXISTS generated_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id VARCHAR(36) NOT NULL,
    file_type VARCHAR(20) NOT NULL,  -- 'image', 'audio', 'music', 'video', 'scene'
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    metadata TEXT,  -- JSON string for additional data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id)
);

-- Scene breakdowns table
CREATE TABLE IF NOT EXISTS scenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id VARCHAR(36) NOT NULL,
    scene_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    prompt TEXT NOT NULL,
    duration INTEGER DEFAULT 5,
    image_file_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id),
    FOREIGN KEY (image_file_id) REFERENCES generated_files(id)
);

-- Generation progress tracking
CREATE TABLE IF NOT EXISTS generation_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id VARCHAR(36) NOT NULL,
    progress_percentage REAL DEFAULT 0.0,
    current_step VARCHAR(255),
    status VARCHAR(50) DEFAULT 'processing',
    estimated_time_remaining REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id)
);

-- API usage tracking (for cost monitoring)
CREATE TABLE IF NOT EXISTS api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id VARCHAR(36) NOT NULL,
    api_provider VARCHAR(50) NOT NULL,  -- 'openai', 'elevenlabs', 'suno'
    endpoint VARCHAR(100) NOT NULL,
    tokens_used INTEGER,
    cost_usd REAL,
    response_time REAL,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id)
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_workflows_user_id ON workflows(user_id);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
CREATE INDEX IF NOT EXISTS idx_workflows_created_at ON workflows(created_at);
CREATE INDEX IF NOT EXISTS idx_files_workflow_id ON generated_files(workflow_id);
CREATE INDEX IF NOT EXISTS idx_files_type ON generated_files(file_type);
CREATE INDEX IF NOT EXISTS idx_scenes_workflow_id ON scenes(workflow_id);
CREATE INDEX IF NOT EXISTS idx_progress_workflow_id ON generation_progress(workflow_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_workflow_id ON api_usage(workflow_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_provider ON api_usage(api_provider);

-- Triggers for updated_at timestamps
CREATE TRIGGER IF NOT EXISTS update_workflows_timestamp 
    AFTER UPDATE ON workflows
    BEGIN
        UPDATE workflows SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
    AFTER UPDATE ON users
    BEGIN
        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END; 