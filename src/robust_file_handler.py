"""Robust file handler with cross-platform support"""

import os
from pathlib import Path
from pathvalidate import sanitize_filepath
from typing import Optional


class RobustFileHandler:
    """Handle file operations with robust cross-platform support"""

    def __init__(self, workspace_root: Path):
        """Initialize file handler"""
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(exist_ok=True)

    def save_file(self, file_path: str, content: str) -> dict:
        """
        Save file with robust error handling
        
        Args:
            file_path: Path (absolute or relative)
            content: File content to save
            
        Returns:
            Dictionary with success status and details
        """
        try:
            # Strip quotes if present
            file_path = file_path.strip('"\'')
            
            # Sanitize the path
            sanitized = sanitize_filepath(file_path)
            
            # Determine if absolute or relative
            path_obj = Path(sanitized)
            
            if path_obj.is_absolute():
                # Use absolute path directly
                target_path = path_obj
            else:
                # Use workspace root for relative paths
                target_path = self.workspace_root / sanitized
            
            # Ensure parent directories exist
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the file
            with open(str(target_path), 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Verify
            if target_path.exists():
                size = target_path.stat().st_size
                return {
                    "success": True,
                    "path": str(target_path),
                    "size": size,
                    "message": f"Saved {size} bytes to {target_path}"
                }
            else:
                return {
                    "success": False,
                    "error": "File creation verification failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "input_path": file_path
            }

    def read_file(self, file_path: str) -> Optional[str]:
        """Read file with path handling"""
        try:
            file_path = file_path.strip('"\'')
            path_obj = Path(file_path)
            
            if path_obj.is_absolute():
                target_path = path_obj
            else:
                target_path = self.workspace_root / file_path
            
            if target_path.exists():
                return target_path.read_text(encoding='utf-8')
            return None
        except Exception as e:
            return None

    def ensure_directory(self, directory: str) -> bool:
        """Ensure directory exists"""
        try:
            directory = directory.strip('"\'')
            path_obj = Path(directory)
            
            if path_obj.is_absolute():
                target_path = path_obj
            else:
                target_path = self.workspace_root / directory
            
            target_path.mkdir(parents=True, exist_ok=True)
            return target_path.exists()
        except Exception as e:
            return False
