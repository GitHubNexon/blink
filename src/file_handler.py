"""File handler module for reading, creating, and modifying files"""

import os
from pathlib import Path
from typing import Optional


class FileHandler:
    """Handle file operations for the AI agent"""

    def __init__(self, workspace_root: Path):
        """Initialize file handler with workspace root"""
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(exist_ok=True)

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Read a file from the workspace
        
        Args:
            file_path: Relative or absolute path to the file
            
        Returns:
            File contents as string, or None if file doesn't exist
        """
        full_path = self._resolve_path(file_path)
        
        if not full_path.exists():
            return None
            
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Error reading file {full_path}: {e}")

    def create_file(self, file_path: str, content: str) -> str:
        """
        Create a new file in the workspace
        
        Args:
            file_path: Relative path to the file (relative to workspace root)
            content: File contents
            
        Returns:
            Full path to created file
        """
        full_path = self._resolve_path(file_path)
        
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return str(full_path)
        except Exception as e:
            raise IOError(f"Error creating file {full_path}: {e}")

    def modify_file(self, file_path: str, content: str) -> str:
        """
        Modify an existing file in the workspace
        
        Args:
            file_path: Relative path to the file
            content: New file contents
            
        Returns:
            Full path to modified file
        """
        full_path = self._resolve_path(file_path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"File {full_path} does not exist")
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return str(full_path)
        except Exception as e:
            raise IOError(f"Error modifying file {full_path}: {e}")

    def list_files(self, directory: str = ".") -> list[str]:
        """
        List all files in a directory (non-recursive)
        
        Args:
            directory: Directory path relative to workspace root
            
        Returns:
            List of file paths
        """
        full_path = self._resolve_path(directory)
        
        if not full_path.exists() or not full_path.is_dir():
            return []
        
        try:
            files = [str(f.relative_to(self.workspace_root)) for f in full_path.glob("*") if f.is_file()]
            return sorted(files)
        except Exception as e:
            raise IOError(f"Error listing files in {full_path}: {e}")

    def list_directories(self, directory: str = ".") -> list[str]:
        """
        List all directories in a directory (non-recursive)
        
        Args:
            directory: Directory path relative to workspace root
            
        Returns:
            List of directory paths
        """
        full_path = self._resolve_path(directory)
        
        if not full_path.exists() or not full_path.is_dir():
            return []
        
        try:
            dirs = [str(d.relative_to(self.workspace_root)) for d in full_path.glob("*") if d.is_dir()]
            return sorted(dirs)
        except Exception as e:
            raise IOError(f"Error listing directories in {full_path}: {e}")

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists"""
        return self._resolve_path(file_path).exists()

    def _resolve_path(self, file_path: str) -> Path:
        """
        Resolve file path relative to workspace root
        
        Args:
            file_path: File path (relative or absolute)
            
        Returns:
            Absolute Path object
        """
        if Path(file_path).is_absolute():
            return Path(file_path)
        return self.workspace_root / file_path
