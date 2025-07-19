import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseManager:
    """SQLite database manager for the story-to-video system"""
    
    def __init__(self, db_path: str = "story_video.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with schema"""
        try:
            # Read and execute schema
            schema_path = Path(__file__).parent.parent / "database_schema.sql"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    schema = f.read()
                
                with sqlite3.connect(self.db_path) as conn:
                    conn.executescript(schema)
                    conn.commit()
                
                logger.info(f"Database initialized: {self.db_path}")
            else:
                logger.warning("Schema file not found, creating basic tables")
                self._create_basic_tables()
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _create_basic_tables(self):
        """Create basic tables if schema file is not available"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS workflows (
                    id VARCHAR(36) PRIMARY KEY,
                    original_prompt TEXT NOT NULL,
                    enhanced_story TEXT,
                    story_title VARCHAR(255),
                    current_phase VARCHAR(50) DEFAULT 'prompt_enhancement',
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS generated_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id VARCHAR(36) NOT NULL,
                    file_type VARCHAR(20) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    file_name VARCHAR(255) NOT NULL,
                    file_size INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    
    def create_workflow(self, workflow_id: str, original_prompt: str, story_title: str = None, max_scenes: int = 4) -> bool:
        """Create a new workflow record"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO workflows (id, original_prompt, story_title, max_scenes)
                    VALUES (?, ?, ?, ?)
                """, (workflow_id, original_prompt, story_title, max_scenes))
                conn.commit()
            
            logger.info(f"Created workflow record: {workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            return False
    
    def update_workflow_phase(self, workflow_id: str, phase: str, enhanced_story: str = None) -> bool:
        """Update workflow phase and enhanced story"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if enhanced_story:
                    conn.execute("""
                        UPDATE workflows 
                        SET current_phase = ?, enhanced_story = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (phase, enhanced_story, workflow_id))
                else:
                    conn.execute("""
                        UPDATE workflows 
                        SET current_phase = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (phase, workflow_id))
                conn.commit()
            
            logger.info(f"Updated workflow {workflow_id} to phase: {phase}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating workflow: {e}")
            return False
    
    def complete_workflow(self, workflow_id: str, processing_time: float) -> bool:
        """Mark workflow as completed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE workflows 
                    SET status = 'completed', current_phase = 'completed', 
                        completed_at = CURRENT_TIMESTAMP, total_processing_time = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (processing_time, workflow_id))
                conn.commit()
            
            logger.info(f"Completed workflow: {workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing workflow: {e}")
            return False
    
    def add_generated_file(self, workflow_id: str, file_type: str, file_path: str, 
                          file_name: str, file_size: int = None, metadata: Dict = None) -> bool:
        """Add a generated file record"""
        try:
            metadata_json = json.dumps(metadata) if metadata else None
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO generated_files (workflow_id, file_type, file_path, file_name, file_size, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (workflow_id, file_type, file_path, file_name, file_size, metadata_json))
                conn.commit()
            
            logger.info(f"Added file record: {file_name} for workflow {workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding file record: {e}")
            return False
    
    def get_workflow_files(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get all files for a workflow"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM generated_files 
                    WHERE workflow_id = ? 
                    ORDER BY created_at
                """, (workflow_id,))
                
                files = []
                for row in cursor.fetchall():
                    file_data = dict(row)
                    if file_data['metadata']:
                        file_data['metadata'] = json.loads(file_data['metadata'])
                    files.append(file_data)
                
                return files
                
        except Exception as e:
            logger.error(f"Error getting workflow files: {e}")
            return []
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow details"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM workflows WHERE id = ?
                """, (workflow_id,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Error getting workflow: {e}")
            return None
    
    def list_workflows(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent workflows"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM workflows 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                workflows = []
                for row in cursor.fetchall():
                    workflows.append(dict(row))
                
                return workflows
                
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
            return []
    
    def track_api_usage(self, workflow_id: str, provider: str, endpoint: str, 
                       tokens_used: int = None, cost_usd: float = None, 
                       response_time: float = None, success: bool = True, 
                       error_message: str = None) -> bool:
        """Track API usage for cost monitoring"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO api_usage (workflow_id, api_provider, endpoint, tokens_used, 
                                         cost_usd, response_time, success, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (workflow_id, provider, endpoint, tokens_used, cost_usd, 
                     response_time, success, error_message))
                conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error tracking API usage: {e}")
            return False
    
    def get_api_usage_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get API usage summary for cost monitoring"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT 
                        api_provider,
                        COUNT(*) as total_calls,
                        SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_calls,
                        SUM(tokens_used) as total_tokens,
                        SUM(cost_usd) as total_cost,
                        AVG(response_time) as avg_response_time
                    FROM api_usage 
                    WHERE created_at >= datetime('now', '-{} days')
                    GROUP BY api_provider
                """.format(days))
                
                summary = {}
                for row in cursor.fetchall():
                    summary[row['api_provider']] = dict(row)
                
                return summary
                
        except Exception as e:
            logger.error(f"Error getting API usage summary: {e}")
            return {}
    
    def cleanup_old_workflows(self, days: int = 30) -> int:
        """Clean up old completed workflows"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Delete old workflow files
                cursor = conn.execute("""
                    DELETE FROM generated_files 
                    WHERE workflow_id IN (
                        SELECT id FROM workflows 
                        WHERE status = 'completed' 
                        AND created_at < datetime('now', '-{} days')
                    )
                """.format(days))
                
                # Delete old workflows
                cursor = conn.execute("""
                    DELETE FROM workflows 
                    WHERE status = 'completed' 
                    AND created_at < datetime('now', '-{} days')
                """.format(days))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                logger.info(f"Cleaned up {deleted_count} old workflows")
                return deleted_count
                
        except Exception as e:
            logger.error(f"Error cleaning up old workflows: {e}")
            return 0

# Global database manager instance
db_manager = DatabaseManager() 