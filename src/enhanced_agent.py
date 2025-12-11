"""Enhanced AI Agent with MCP Server integration"""

from pathlib import Path
from typing import Optional
from src.file_handler import FileHandler
from src.replicate_api import ReplicateClient
from src.conversation_memory import ConversationMemory
from src.mcp_server import BlinkMCPServer


class EnhancedCodeAgent:
    """AI Agent with MCP Server for smart file access and context"""

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize the Enhanced Code Agent with MCP capabilities
        
        Args:
            workspace_root: Root directory for the workspace
        """
        if workspace_root is None:
            from src.config import WORKSPACE_ROOT
            workspace_root = WORKSPACE_ROOT
        
        self.file_handler = FileHandler(workspace_root)
        self.api_client = ReplicateClient()
        self.workspace_root = workspace_root
        self.memory = ConversationMemory(workspace_root)
        
        # Initialize MCP Server for Claude to use
        self.mcp_server = BlinkMCPServer(workspace_root)

    def read_file(self, file_path: str) -> Optional[str]:
        """Read a file from the workspace"""
        return self.file_handler.read_file(file_path)

    def create_file(self, file_path: str, content: str) -> str:
        """Create a new file in the workspace"""
        return self.file_handler.create_file(file_path, content)

    def modify_file(self, file_path: str, content: str) -> str:
        """Modify an existing file in the workspace"""
        return self.file_handler.modify_file(file_path, content)

    def list_files(self, directory: str = ".") -> list[str]:
        """List files in a directory"""
        return self.file_handler.list_files(directory)

    def list_directories(self, directory: str = ".") -> list[str]:
        """List directories"""
        return self.file_handler.list_directories(directory)

    def generate_code_with_full_context(self, instruction: str, file_paths: list[str] = None) -> str:
        """
        Generate code with full file context provided directly
        Pre-reads all files and includes complete context in the prompt
        
        Args:
            instruction: The user's instruction
            file_paths: List of file paths to read and include
            
        Returns:
            Generated code
        """
        import re
        
        # If no paths provided, try to extract from instruction
        if not file_paths:
            file_paths = re.findall(r'"([^"]+)"', instruction)
        
        # Build comprehensive context
        context_section = ""
        if file_paths:
            context_section = "\n\nREFERENCE CODE FILES:\n"
            context_section += "=" * 80 + "\n"
            
            for path in file_paths:
                try:
                    content = self.read_file(path)
                    if content:
                        # Get file language
                        from pathlib import Path as PathLib
                        ext = PathLib(path).suffix
                        lang = self._get_language(ext)
                        
                        context_section += f"\nFILE: {path}\n"
                        context_section += f"LANGUAGE: {lang}\n"
                        context_section += "-" * 80 + "\n"
                        context_section += content
                        context_section += "\n" + "-" * 80 + "\n"
                except Exception as e:
                    context_section += f"\n[ERROR reading {path}: {e}]\n"
        
        # Build the complete prompt
        full_prompt = f"""TASK: {instruction}

{context_section}

REQUIREMENTS:
1. Match the exact language of the reference files (TypeScript, Python, etc.)
2. Follow the same code style and patterns shown in the reference files
3. Use the same naming conventions and structure
4. Include appropriate error handling and logging
5. Add documentation comments where needed
6. DO NOT generate code in a different language than the references
7. Create code that would logically extend or adapt from the reference files

Generate the code now:"""
        
        return self.api_client.generate_code(full_prompt)
    
    def _get_language(self, extension: str) -> str:
        """Detect language from extension"""
        lang_map = {
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript (React)',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript (React)',
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
        }
        return lang_map.get(extension.lower(), 'Unknown')

    def generate_code_with_mcp(self, specification: str) -> str:
        """
        Generate code using MCP server for intelligent file access
        Claude can autonomously call MCP tools to understand context
        """
        # Get available MCP tools
        tools = self.mcp_server.get_tools_definition()
        
        # Build system prompt that tells Claude about MCP tools
        system_prompt = """You are an expert code generation AI. You have access to MCP tools that let you:
1. read_file - Read any file to understand its structure and patterns
2. list_directory - Explore the project structure
3. search_files - Find related files
4. get_file_info - Get metadata about files
5. get_project_structure - Understand the overall project organization

IMPORTANT: Use these tools to understand context and patterns BEFORE generating code.

When the user asks you to create code based on files:
1. Use read_file to examine the provided files
2. Understand the language, patterns, and conventions
3. Generate code that EXACTLY matches the language and style

ALWAYS preserve the original programming language. If you're adapting TypeScript code, output TypeScript, not Python.
"""
        
        # Create a special format that Claude can understand for MCP tool calls
        mcp_instruction = f"""{specification}

Available MCP tools you can use:
{json.dumps(tools, indent=2)}

When you need to examine files, respond with:
[MCP_TOOL_CALL: tool_name]
{{"path": "...", ...}}
[/MCP_TOOL_CALL]

Then provide the answer based on tool results."""
        
        return self.api_client.generate_code(system_prompt + "\n\n" + mcp_instruction)

    def generate_code(self, specification: str) -> str:
        """Generate code based on specification (fallback to regular mode)"""
        return self.api_client.generate_code(specification)

    def analyze_code(self, code: str, instruction: str) -> str:
        """Analyze and modify code"""
        return self.api_client.analyze_code(code, instruction)

    def plan_tasks(self, objective: str) -> list[str]:
        """Create a plan for an objective"""
        return self.api_client.plan_tasks(objective)

    def refactor_code(self, file_path: str, refactoring_rules: str) -> str:
        """
        Refactor code in a file based on rules
        
        Args:
            file_path: Path to the file to refactor
            refactoring_rules: Rules for refactoring
            
        Returns:
            Refactored code
        """
        code = self.read_file(file_path)
        if not code:
            raise FileNotFoundError(f"File {file_path} not found")
        
        refactored = self.analyze_code(code, refactoring_rules)
        self.modify_file(file_path, refactored)
        return refactored

    def create_from_template(self, file_path: str, template_spec: str) -> str:
        """
        Create a file from a template specification
        
        Args:
            file_path: Path for the new file
            template_spec: Specification for the template
            
        Returns:
            Path to created file
        """
        content = self.generate_code(template_spec)
        return self.create_file(file_path, content)

    def execute_plan(self, objective: str) -> dict:
        """
        Execute a full plan for an objective
        
        Args:
            objective: The objective to achieve
            
        Returns:
            Dictionary with results
        """
        plan = self.plan_tasks(objective)
        results = []
        
        for step in plan:
            result = self.generate_code(step)
            results.append({"step": step, "result": result})
        
        return {
            "objective": objective,
            "plan": plan,
            "results": results
        }

    # MCP Server integration
    def call_mcp_tool(self, tool_name: str, tool_args: dict) -> str:
        """Call an MCP tool directly"""
        return self.mcp_server.handle_tool_call(tool_name, tool_args)

    def get_mcp_tools(self) -> list[dict]:
        """Get list of available MCP tools"""
        return self.mcp_server.get_tools_definition()


import json
