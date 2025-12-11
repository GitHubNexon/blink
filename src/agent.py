"""Main AI Agent module - orchestrates file operations and code generation"""

from pathlib import Path
from typing import Optional
from src.file_handler import FileHandler
from src.replicate_api import ReplicateClient
from src.conversation_memory import ConversationMemory


class CodeAgent:
    """AI Agent that can read, create, and modify files with AI assistance"""

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize the Code Agent
        
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

    def generate_code(self, specification: str) -> str:
        """Generate code based on specification"""
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
            Dictionary with plan and execution results
        """
        print(f"\n🤖 Planning objective: {objective}\n")
        
        # Step 1: Create plan
        steps = self.plan_tasks(objective)
        print(f"📋 Plan created with {len(steps)} steps:\n")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")
        
        return {
            "objective": objective,
            "steps": steps,
            "status": "planned"
        }
