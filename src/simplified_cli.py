"""Simplified AI Agent CLI - 6 essential commands only - WITH MCP SERVER"""

import sys
from pathlib import Path
from src.enhanced_agent import EnhancedCodeAgent
from src.robust_file_handler import RobustFileHandler
from src.config import WORKSPACE_ROOT


class SimplifiedCLI:
    """Simplified CLI with 6 core commands + MCP Server integration"""

    def __init__(self):
        """Initialize the CLI"""
        self.agent = EnhancedCodeAgent()
        self.file_handler = RobustFileHandler(WORKSPACE_ROOT)

    def print_header(self):
        """Print CLI header"""
        print("\n" + "=" * 70)
        print("[AI AGENT] - Code Generation & Analysis Platform")
        print("=" * 70 + "\n")

    def print_help(self):
        """Print help with only essential commands"""
        print("""
COMMAND REFERENCE (use :: delimiter)
------------------------------------------------------------------------

read::          Read a file (workspace or absolute path)
create::        Create a new empty file
list::          List files and folders (directory listing)
generate::      AI code generation - analyze, extend, improve, create
history::       Show conversation history
clear::         Clear session and conversation history (with confirmation)
help::          Show this help message
exit::          Exit and save session

------------------------------------------------------------------------
USAGE EXAMPLES:
------------------------------------------------------------------------

1. READ FILE (local or external):
   blink> read:: myfile.ts
   blink> read:: r"C:\path\to\external\file.ts"

2. CREATE EMPTY FILE:
   blink> create:: new-service.ts

3. LIST DIRECTORY:
   blink> list:: .
   blink> list:: src/modules

4. GENERATE CODE:
   blink> generate:: Create a sensor service in TypeScript
   blink> generate:: "C:\\path\\to\\file.ts" Add error handling
   blink> generate:: Create variant from "C:\\path\\temp.ts" for pH

   Capabilities:
   - Generate new code from specifications
   - Improve existing code
   - Analyze and refactor
   - Create variants/extensions
   - Plan project tasks
   - All in one powerful command

5. VIEW HISTORY:
   blink> history::

6. CLEAR SESSION:
   blink> clear::
   (Clears current session with confirmation prompt)

7. HELP:
   blink> help::

8. EXIT:
   blink> exit::

------------------------------------------------------------------------
        """)

    def handle_read_command(self, file_path: str):
        """Handle read command"""
        # Strip quotes if present
        file_path = file_path.strip('"\'')
        
        print(f"\n[READ] {file_path}\n")
        
        content = self.agent.read_file(file_path)
        if not content:
            print(f"[ERROR] File not found: {file_path}\n")
            return
        
        self.agent.memory.add_message("user", f"read:: {file_path}", "read")
        self.agent.memory.add_context("last_read_file", file_path)
        
        print("─" * 70)
        print(content)
        print("─" * 70)
        print()
        
        self.agent.memory.add_message("assistant", f"Read {len(content)} characters", "read")

    def handle_create_command(self, file_path: str):
        """Handle create command - creates empty file"""
        print(f"\n[CREATE] {file_path}\n")
        
        result = self.agent.create_file(file_path, "")
        print(f"[OK] File created: {result}\n")
        
        self.agent.memory.add_message("user", f"create:: {file_path}", "create")
        self.agent.memory.add_context("last_created_file", file_path)
        self.agent.memory.add_message("assistant", f"Empty file created: {file_path}", "create")

    def handle_list_command(self, directory: str = "."):
        """Handle list command - works like 'dir'"""
        print(f"\n[LIST] {directory}\n")
        
        files = self.agent.list_files(directory)
        dirs = self.agent.list_directories(directory)
        
        if dirs:
            print("  [DIRECTORIES]")
            for d in dirs:
                print(f"    {d}/")
        
        if files:
            if dirs:
                print()
            print("  [FILES]")
            for f in files:
                print(f"    {f}")
        
        if not files and not dirs:
            print("  (empty directory)")
        
        print()

    def handle_generate_command(self, instruction: str):
        """Handle generate command - all-in-one AI power with full context"""
        print(f"\n[PROCESSING] {instruction[:60]}...\n")
        print("[READING] Files and building context...\n")
        
        try:
            # Extract file paths from instruction
            import re
            paths = re.findall(r'"([^"]+)"', instruction)
            
            # Show which files are being read
            if paths:
                for path in paths:
                    try:
                        file_info = self.agent.call_mcp_tool("get_file_info", {"path": path})
                        import json
                        info = json.loads(file_info)
                        if info.get("success"):
                            language = info.get("language", "Unknown")
                            lines = info.get("lines", 0)
                            print(f"[FILE] {path} ({language}, {lines} lines)")
                    except:
                        pass
            
            print("[ANALYZING] Generating with full context...\n")
            
            # Use the new full context method
            result = self.agent.generate_code_with_full_context(instruction, paths)
            
            # Show result
            print("─" * 70)
            print(result)
            print("─" * 70)
            print()
            
            # Ask to save - with validation
            while True:
                save = input("[SAVE] Write to file? (y/n): ").strip().lower()
                if save in ["y", "yes"]:
                    file_path = input("[PATH] Enter file path: ").strip()
                    
                    if file_path:
                        # Use robust file handler
                        result_dict = self.file_handler.save_file(file_path, result)
                        
                        if result_dict.get("success"):
                            print(f"\n[OK] SAVED")
                            print(f"     Path: {result_dict.get('path')}")
                            print(f"     Size: {result_dict.get('size')} bytes\n")
                            self.agent.memory.add_context("last_created_file", result_dict.get('path'))
                        else:
                            print(f"\n[ERROR] {result_dict.get('error')}\n")
                            print("[TIP] Try using just the filename like 'ph-sensor.ts'\n")
                            continue
                    else:
                        print("[WARN] No file path provided\n")
                        continue
                    break
                elif save in ["n", "no"]:
                    print()
                    break
                else:
                    print("[WARN] Please enter 'y' or 'n'\n")
            
            self.agent.memory.add_message("user", f"generate:: {instruction}", "generate")
            self.agent.memory.add_message("assistant", f"Generated {len(result)} characters", "generate")
            
        except Exception as e:
            print(f"[ERROR] {e}\n")
            self.agent.memory.add_message("assistant", f"Error: {e}", "generate")

    def handle_history_command(self):
        """Handle history command - show conversations"""
        print("\n" + "-" * 70)
        print("[HISTORY] CONVERSATION LOG")
        print("-" * 70 + "\n")
        
        history = self.agent.memory.conversation_history
        
        if not history:
            print("No conversation history yet.\n")
            return
        
        # Show summary first
        user_messages = [m for m in history if m["role"] == "user"]
        print(f"Total messages: {len(history)}")
        print(f"Your commands: {len(user_messages)}\n")
        
        # Show recent conversations
        print("Recent interactions:\n")
        for msg in history[-10:]:
            role = "[USER]" if msg["role"] == "user" else "[ASSISTANT]"
            content = msg["content"][:60] + "..." if len(msg["content"]) > 60 else msg["content"]
            print(f"{role}: {content}")
        
        print("\n" + "-" * 70 + "\n")

    def handle_clear_command(self):
        """Handle clear command - clear session and history with confirmation"""
        import os
        
        print("\n[WARN] Clear current session?\n")
        print("This will:")
        print("  - Delete conversation history")
        print("  - Clear all commands from this session")
        print("  - Cannot be undone\n")
        
        try:
            confirm = input("[CONFIRM] Are you sure? (yes/no): ").strip().lower()
        except EOFError:
            print("[CANCEL] Clear cancelled.\n")
            return
        
        if confirm in ["yes", "y"]:
            try:
                # Clear current session file
                history_dir = self.agent.workspace_root / ".agent_history"
                current_session_file = history_dir / "current_session.json"
                
                if current_session_file.exists():
                    current_session_file.unlink()
                    
                    # Create empty session file
                    with open(current_session_file, 'w') as f:
                        f.write('{"history": [], "context": {}}')
                    
                    # Clear terminal-like
                    os.system('cls' if os.name == 'nt' else 'clear')
                    
                    print("[OK] Session cleared.\n")
                    
                    # Reinitialize memory
                    from src.conversation_memory import ConversationMemory
                    self.agent.memory = ConversationMemory(self.agent.workspace_root)
                else:
                    print("[WARN] No active session to clear.\n")
                    
            except Exception as e:
                print(f"[ERROR] Could not clear session: {e}\n")
        else:
            print("[CANCEL] Clear cancelled.\n")


    def parse_command(self, user_input: str) -> tuple:
        """Parse command with double colon format"""
        if "::" not in user_input:
            return None, None
        
        parts = user_input.split("::", 1)
        command = parts[0].strip()
        args = parts[1].strip() if len(parts) > 1 else ""
        
        return command, args

    def main(self):
        """Main CLI loop"""
        self.print_header()
        print(f"Workspace: {WORKSPACE_ROOT}\n")
        print("Type 'help::' for commands or 'exit::' to quit.\n")
        
        while True:
            try:
                user_input = input("blink> ").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                command, args = self.parse_command(user_input)
                
                if not command:
                    print("[WARN] Format: command:: <args>  (use double colon)\n")
                    continue
                
                command = command.lower()
                
                if command == "exit":
                    print("\n[CONFIRM] Exit and save session? (yes/no): ", end="")
                    confirm = input().strip().lower()
                    if confirm in ["yes", "y"]:
                        try:
                            self.agent.memory.save_to_all_history()
                            print("[OK] Session saved.\n")
                        except Exception as e:
                            print(f"[WARN] Error saving session: {e}\n")
                        break
                    else:
                        print("[CANCEL] Exit cancelled.\n")
                        continue
                
                elif command == "clear":
                    self.handle_clear_command()
                
                elif command == "help":
                    self.print_help()
                
                elif command == "read":
                    if not args:
                        print("[ERROR] Usage: read:: <file>\n")
                        continue
                    self.handle_read_command(args)
                
                elif command == "create":
                    if not args:
                        print("[ERROR] Usage: create:: <file>\n")
                        continue
                    self.handle_create_command(args)
                
                elif command == "list":
                    directory = args if args else "."
                    self.handle_list_command(directory)
                
                elif command == "generate":
                    if not args:
                        print("[ERROR] Usage: generate:: <instruction>\n")
                        continue
                    self.handle_generate_command(args)
                
                elif command == "history":
                    self.handle_history_command()
                
                else:
                    print(f"[ERROR] Unknown command: {command}\n")
                    print("Type 'help::' for available commands\n")
            
            except KeyboardInterrupt:
                print("\n\n[EXIT] Session saved.")
                try:
                    self.agent.memory.save_to_all_history()
                except:
                    pass
                break
            except EOFError:
                # Handle EOF gracefully (piped input)
                break
            except Exception as e:
                print(f"[ERROR] {e}\n")


def main():
    """Entry point"""
    try:
        cli = SimplifiedCLI()
        cli.main()
    finally:
        # Clear API token from memory when exiting
        from src.token_manager import clear_api_token
        clear_api_token()


if __name__ == "__main__":
    main()
