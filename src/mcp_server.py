"""
Simple MCP (Model Context Protocol) Server for Blink AI Agent
Provides tools for Claude to autonomously read files, explore projects, and understand code structure
"""

import json
import sys
from pathlib import Path
from typing import Any, Optional
from src.file_handler import FileHandler


class BlinkMCPServer:
    """MCP Server that provides tools for Claude to interact with the file system"""

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize MCP server"""
        if workspace_root is None:
            from src.config import WORKSPACE_ROOT
            workspace_root = WORKSPACE_ROOT
        
        self.file_handler = FileHandler(workspace_root)
        self.workspace_root = workspace_root

    def read_file(self, path: str) -> dict:
        """
        Read a file from the workspace
        Tool for Claude to read file contents
        """
        try:
            content = self.file_handler.read_file(path)
            if content is None:
                return {
                    "success": False,
                    "error": f"File not found: {path}"
                }
            
            file_path = Path(path)
            return {
                "success": True,
                "path": path,
                "language": self._get_language(file_path.suffix),
                "size": len(content.encode('utf-8')),
                "lines": len(content.split('\n')),
                "content": content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_directory(self, path: str = ".") -> dict:
        """
        List files and directories
        Tool for Claude to explore project structure
        """
        try:
            dirs = self.file_handler.list_directories(path)
            files = self.file_handler.list_files(path)
            
            return {
                "success": True,
                "path": path,
                "directories": dirs,
                "files": files,
                "file_count": len(files),
                "dir_count": len(dirs)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def search_files_by_pattern(self, pattern: str, directory: str = ".") -> dict:
        """
        Search for files matching a pattern
        Tool for Claude to find related files
        """
        try:
            workspace_path = self.workspace_root / directory
            matches = []
            
            if workspace_path.exists():
                for file_path in workspace_path.rglob("*"):
                    if file_path.is_file() and pattern.lower() in file_path.name.lower():
                        matches.append(str(file_path.relative_to(self.workspace_root)))
            
            return {
                "success": True,
                "pattern": pattern,
                "directory": directory,
                "matches": matches,
                "count": len(matches)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_file_info(self, path: str) -> dict:
        """
        Get metadata about a file without reading full content
        Useful for understanding file structure before reading
        """
        try:
            file_path = self.workspace_root / path
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {path}"
                }
            
            stat = file_path.stat()
            content = file_path.read_text() if file_path.is_file() else ""
            
            return {
                "success": True,
                "path": path,
                "exists": True,
                "is_file": file_path.is_file(),
                "language": self._get_language(file_path.suffix),
                "size": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "lines": len(content.split('\n')) if content else 0,
                "extension": file_path.suffix
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_project_structure(self, max_depth: int = 3) -> dict:
        """
        Get overview of project structure
        Helps Claude understand the codebase organization
        """
        try:
            structure = {}
            self._build_tree(self.workspace_root, structure, depth=0, max_depth=max_depth)
            
            return {
                "success": True,
                "root": str(self.workspace_root),
                "structure": structure
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _build_tree(self, path: Path, tree: dict, depth: int = 0, max_depth: int = 3):
        """Recursively build project tree structure"""
        if depth > max_depth:
            return
        
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith('.'):
                    continue
                
                if item.is_dir():
                    tree[f"{item.name}/"] = {}
                    self._build_tree(item, tree[f"{item.name}/"], depth + 1, max_depth)
                else:
                    tree[item.name] = {
                        "size": item.stat().st_size,
                        "lang": self._get_language(item.suffix)
                    }
        except PermissionError:
            pass

    def _get_language(self, extension: str) -> str:
        """Detect programming language from file extension"""
        lang_map = {
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript React',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript React',
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.sql': 'SQL',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
        }
        return lang_map.get(extension.lower(), 'Unknown')

    def format_for_claude(self, data: dict) -> str:
        """Format tool results for Claude to understand"""
        return json.dumps(data, indent=2)

    # MCP Protocol Methods
    def handle_tool_call(self, tool_name: str, tool_args: dict) -> str:
        """Handle tool calls from Claude via MCP protocol"""
        if tool_name == "read_file":
            result = self.read_file(tool_args.get("path", ""))
        elif tool_name == "list_directory":
            result = self.list_directory(tool_args.get("path", "."))
        elif tool_name == "search_files":
            result = self.search_files_by_pattern(
                tool_args.get("pattern", ""),
                tool_args.get("directory", ".")
            )
        elif tool_name == "get_file_info":
            result = self.get_file_info(tool_args.get("path", ""))
        elif tool_name == "get_project_structure":
            result = self.get_project_structure(tool_args.get("max_depth", 3))
        else:
            result = {"success": False, "error": f"Unknown tool: {tool_name}"}
        
        return self.format_for_claude(result)

    def get_tools_definition(self) -> list[dict]:
        """Get tool definitions for Claude"""
        return [
            {
                "name": "read_file",
                "description": "Read the full contents of a file from the workspace",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file to read (relative to workspace)"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "list_directory",
                "description": "List files and directories in a path",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to list (default: current directory)"
                        }
                    }
                }
            },
            {
                "name": "search_files",
                "description": "Search for files matching a pattern",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Pattern to search for in filenames"
                        },
                        "directory": {
                            "type": "string",
                            "description": "Directory to search in (default: current)"
                        }
                    },
                    "required": ["pattern"]
                }
            },
            {
                "name": "get_file_info",
                "description": "Get metadata about a file (size, language, line count)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "get_project_structure",
                "description": "Get an overview of the project structure",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "max_depth": {
                            "type": "integer",
                            "description": "Maximum directory depth to show (default: 3)"
                        }
                    }
                }
            }
        ]
