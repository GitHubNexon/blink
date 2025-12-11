"""Conversation memory and history management"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


class ConversationMemory:
    """Manages conversation history and context for the AI agent"""

    def __init__(self, workspace_root: Path):
        """
        Initialize conversation memory
        
        Args:
            workspace_root: Root directory for storing conversation history
        """
        self.workspace_root = Path(workspace_root)
        self.history_dir = self.workspace_root / ".agent_history"
        self.history_dir.mkdir(exist_ok=True)
        
        self.current_session_file = self.history_dir / "current_session.json"
        self.all_history_file = self.history_dir / "all_history.json"
        
        self.conversation_history: List[Dict[str, Any]] = []
        self.context_variables: Dict[str, Any] = {}
        
        self.load_or_create_session()

    def load_or_create_session(self):
        """Load existing session or create a new one"""
        if self.current_session_file.exists():
            try:
                with open(self.current_session_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        self.conversation_history = data.get("history", [])
                        self.context_variables = data.get("context", {})
                    else:
                        self.conversation_history = []
                        self.context_variables = {}
            except Exception as e:
                print(f"Warning: Could not load session: {e}")
                self.conversation_history = []
                self.context_variables = {}
        else:
            self.conversation_history = []
            self.context_variables = {}

    def add_message(self, role: str, content: str, command: Optional[str] = None, metadata: Optional[Dict] = None):
        """
        Add a message to conversation history
        
        Args:
            role: "user" or "assistant"
            content: Message content
            command: Command type (generate, analyze, etc.)
            metadata: Additional metadata
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "command": command,
            "metadata": metadata or {}
        }
        self.conversation_history.append(message)
        self.save_session()

    def add_context(self, key: str, value: Any):
        """Add context variable (file paths, previous results, etc.)"""
        self.context_variables[key] = value
        self.save_session()

    def get_context(self, key: str) -> Optional[Any]:
        """Get context variable"""
        return self.context_variables.get(key)

    def get_conversation_context(self, limit: int = 10) -> str:
        """
        Get recent conversation context as string for AI
        
        Args:
            limit: Number of recent messages to include
            
        Returns:
            Formatted conversation context
        """
        recent = self.conversation_history[-limit:]
        context_str = "Previous conversation:\n"
        
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_str += f"\n{role}: {msg['content'][:200]}...\n" if len(msg['content']) > 200 else f"\n{role}: {msg['content']}\n"
        
        return context_str

    def get_last_file_paths(self) -> Dict[str, str]:
        """Get recently mentioned file paths from context"""
        return {
            "last_read": self.context_variables.get("last_read_file"),
            "last_created": self.context_variables.get("last_created_file"),
            "last_modified": self.context_variables.get("last_modified_file"),
        }

    def save_session(self):
        """Save current session to file"""
        data = {
            "session_start": datetime.now().isoformat(),
            "history": self.conversation_history,
            "context": self.context_variables
        }
        
        with open(self.current_session_file, "w") as f:
            json.dump(data, f, indent=2)

    def save_to_all_history(self):
        """Archive current session to all history"""
        try:
            if not self.all_history_file.exists():
                all_history = []
            else:
                with open(self.all_history_file, "r") as f:
                    content = f.read().strip()
                    all_history = json.loads(content) if content else []
            
            session_data = {
                "session_date": datetime.now().isoformat(),
                "conversation": self.conversation_history,
                "context": self.context_variables
            }
            all_history.append(session_data)
            
            with open(self.all_history_file, "w") as f:
                json.dump(all_history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save to history: {e}")

    def clear_session(self):
        """Clear current session"""
        self.conversation_history = []
        self.context_variables = {}
        self.save_session()

    def get_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        user_messages = [m for m in self.conversation_history if m["role"] == "user"]
        commands_used = {}
        
        for msg in user_messages:
            cmd = msg.get("command", "unknown")
            commands_used[cmd] = commands_used.get(cmd, 0) + 1
        
        summary = f"\nSession Summary:\n"
        summary += f"Total messages: {len(self.conversation_history)}\n"
        summary += f"User queries: {len(user_messages)}\n"
        summary += f"Commands used: {commands_used}\n"
        summary += f"Context variables: {len(self.context_variables)}\n"
        
        return summary

    def export_conversation(self, filename: str = "conversation_export.md") -> str:
        """Export conversation as markdown file"""
        export_path = self.workspace_root / filename
        
        with open(export_path, "w") as f:
            f.write("# Agent Conversation History\n\n")
            f.write(f"Exported: {datetime.now().isoformat()}\n\n")
            
            for msg in self.conversation_history:
                role = "👤 User" if msg["role"] == "user" else "🤖 Agent"
                timestamp = msg["timestamp"]
                content = msg["content"]
                
                f.write(f"## {role} ({timestamp})\n")
                if msg.get("command"):
                    f.write(f"*Command: {msg['command']}*\n\n")
                f.write(f"{content}\n\n")
                f.write("---\n\n")
        
        return str(export_path)
