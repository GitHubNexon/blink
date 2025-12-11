"""Enhanced command-line interface for the AI Agent with Copilot-like behavior"""

import sys
from pathlib import Path
from src.agent import CodeAgent
from src.config import WORKSPACE_ROOT


class EnhancedCLI:
    """Enhanced CLI with confirmation prompts, history, and Copilot-like behavior"""

    def __init__(self):
        """Initialize the enhanced CLI"""
        self.agent = CodeAgent()
        self.pending_action = None
        self.pending_details = None

    def print_header(self):
        """Print CLI header"""
        print("\n" + "=" * 70)
        print("🤖 AI AGENT - Enhanced CLI (Copilot-like)")
        print("   With conversation memory and confirmation prompts")
        print("=" * 70 + "\n")

    def print_help(self):
        """Print help message with new command format"""
        print("""
📋 COMMAND FORMAT (with double colon):
════════════════════════════════════════════════════════════════════

read::              <file>
create::            <file>
modify::            <file>
list::              [directory]
generate::          <specification>
analyze::           <file> <task>
plan::              <objective>
refactor::          <file> <rules>
memory::            [summary|clear|export|history]
compare::           <file1> <file2>
extend::            <file> <with_file> <description>
help::              Show this help message
exit::              Exit the CLI

📝 EXAMPLES:
════════════════════════════════════════════════════════════════════

read:: src/models/user.ts
  → Shows file contents

create:: new_file.py
  → Opens editor to create new file

generate:: Create a version of temperature-sensor.service.ts for pH water monitoring
  → AI generates code with preview before execution

plan:: Build a REST API with authentication
  → Creates step-by-step plan with confirmation

memory:: summary
  → Shows conversation summary

memory:: history
  → Shows recent conversation

compare:: file1.ts file2.ts
  → Compare two files side-by-side

extend:: temperature-sensor.ts pH-sensor.ts about pH water monitoring
  → Create pH sensor code based on temperature sensor template

✨ KEY FEATURES:
════════════════════════════════════════════════════════════════════
✓ Confirmation prompts before execution (like Copilot)
✓ Preview of AI-generated code before saving
✓ Accept (y) or Undo (u) changes
✓ Conversation memory - remembers context
✓ Command history stored automatically
✓ Double colon "::" command format
✓ File path context from previous commands
        """)

    def format_code_preview(self, code: str, max_lines: int = 20) -> str:
        """Format code for preview display"""
        lines = code.split("\n")
        if len(lines) > max_lines:
            preview = "\n".join(lines[:max_lines])
            preview += f"\n... ({len(lines) - max_lines} more lines)"
            return preview
        return code

    def confirm_action(self, action: str, preview: str = None) -> bool:
        """
        Ask user to confirm an action (like GitHub Copilot)
        
        Returns:
            True if confirmed, False if denied
        """
        print("\n" + "─" * 70)
        print(f"🔮 PROPOSED ACTION: {action}")
        print("─" * 70)
        
        if preview:
            print("\n📄 PREVIEW:")
            print("─" * 70)
            print(self.format_code_preview(preview))
            print("─" * 70)
        
        while True:
            response = input("\n✓ Accept (y/yes) | ✗ Reject (n/no) | 📝 Edit (e/edit) | ↶ Undo (u/undo): ").strip().lower()
            
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                print("❌ Action cancelled.")
                return False
            elif response in ["e", "edit"]:
                print("📝 Edit mode not yet implemented. Coming soon!")
                return False
            elif response in ["u", "undo"]:
                print("↶ Undo - reverting to last state...")
                return False
            else:
                print("⚠️  Please respond with: y, n, e, or u")

    def handle_read_command(self, file_path: str):
        """Handle read command"""
        print(f"\n📖 Reading file: {file_path}")
        
        content = self.agent.read_file(file_path)
        if not content:
            print(f"❌ File not found: {file_path}\n")
            return
        
        # Record in memory
        self.agent.memory.add_message("user", f"Read file: {file_path}", "read")
        self.agent.memory.add_context("last_read_file", file_path)
        
        # Show preview
        print("\n" + "─" * 70)
        print(self.format_code_preview(content))
        print("─" * 70)
        
        self.agent.memory.add_message("assistant", f"File content shown (first 20 lines)", "read")

    def handle_create_command(self, file_path: str):
        """Handle create command"""
        print(f"\n✨ Creating file: {file_path}")
        print("Enter file content (type END on a new line to finish):\n")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        
        content = "\n".join(lines)
        
        # Ask for confirmation
        if self.confirm_action(f"Create file: {file_path}", content):
            result = self.agent.create_file(file_path, content)
            print(f"✅ File created: {result}\n")
            
            self.agent.memory.add_message("user", f"Create file: {file_path}", "create")
            self.agent.memory.add_context("last_created_file", file_path)
            self.agent.memory.add_message("assistant", f"File created: {result}", "create")
        else:
            print("File creation cancelled.\n")

    def handle_generate_command(self, specification: str):
        """Handle generate command with confirmation"""
        print(f"\n🔄 Generating code for: {specification}\n")
        print("⏳ Please wait, AI is thinking...\n")
        
        # Get context from memory for better results
        context = self.agent.memory.get_conversation_context(limit=5)
        last_files = self.agent.memory.get_last_file_paths()
        
        try:
            # Generate code
            code = self.agent.generate_code(specification)
            
            # Record in memory
            self.agent.memory.add_message("user", f"Generate: {specification}", "generate")
            
            # Ask for confirmation with preview
            if self.confirm_action("Accept generated code?", code):
                # Ask where to save
                file_path = input("\n💾 Save to file (or press Enter to skip): ").strip()
                
                if file_path:
                    if self.confirm_action(f"Save to: {file_path}"):
                        self.agent.create_file(file_path, code)
                        print(f"✅ Code saved to: {file_path}\n")
                        self.agent.memory.add_context("last_created_file", file_path)
                    else:
                        print("File save cancelled.\n")
                        self.agent.memory.add_message("assistant", "Code generated but not saved", "generate")
                else:
                    print("\n📋 Code generated but not saved.\n")
                    self.agent.memory.add_message("assistant", f"Generated code preview shown", "generate")
            else:
                print("Code generation cancelled.\n")
                self.agent.memory.add_message("assistant", "Code generation rejected", "generate")
                
        except Exception as e:
            print(f"❌ Error: {e}\n")
            self.agent.memory.add_message("assistant", f"Error during generation: {e}", "generate")

    def handle_analyze_command(self, file_path: str, task: str):
        """Handle analyze command with confirmation"""
        print(f"\n🔍 Analyzing: {file_path}")
        print(f"Task: {task}\n")
        print("⏳ Analyzing code...\n")
        
        try:
            code = self.agent.read_file(file_path)
            if not code:
                print(f"❌ File not found: {file_path}\n")
                return
            
            result = self.agent.analyze_code(code, task)
            
            # Record in memory
            self.agent.memory.add_message("user", f"Analyze {file_path}: {task}", "analyze")
            
            # Ask for confirmation
            if self.confirm_action("Accept improvements?", result):
                if input("\n💾 Overwrite original file? (y/n): ").strip().lower() in ["y", "yes"]:
                    self.agent.modify_file(file_path, result)
                    print(f"✅ File updated: {file_path}\n")
                    self.agent.memory.add_context("last_modified_file", file_path)
                    self.agent.memory.add_message("assistant", f"File updated: {file_path}", "analyze")
                else:
                    new_file = input("Save to new file (or press Enter to skip): ").strip()
                    if new_file:
                        self.agent.create_file(new_file, result)
                        print(f"✅ Saved to: {new_file}\n")
                        self.agent.memory.add_message("assistant", f"Analysis saved to: {new_file}", "analyze")
            else:
                print("Analysis rejected.\n")
                
        except Exception as e:
            print(f"❌ Error: {e}\n")

    def handle_plan_command(self, objective: str):
        """Handle plan command with confirmation"""
        print(f"\n📋 Planning: {objective}\n")
        print("⏳ Creating plan...\n")
        
        try:
            plan = self.agent.execute_plan(objective)
            steps = plan["steps"]
            
            # Record in memory
            self.agent.memory.add_message("user", f"Plan: {objective}", "plan")
            
            # Format plan for confirmation
            plan_preview = "\n".join([f"{i}. {step}" for i, step in enumerate(steps, 1)])
            
            if self.confirm_action("Accept plan?", plan_preview):
                print("\n✅ Plan accepted!\n")
                print("Next steps:")
                for i, step in enumerate(steps, 1):
                    print(f"  {i}. {step}")
                print()
                self.agent.memory.add_message("assistant", f"Plan created with {len(steps)} steps", "plan")
            else:
                print("Plan rejected.\n")
                
        except Exception as e:
            print(f"❌ Error: {e}\n")

    def handle_memory_command(self, action: str = "summary"):
        """Handle memory/history commands"""
        if action == "summary":
            print(self.agent.memory.get_summary())
        
        elif action == "history":
            print("\n📜 Recent Conversation History:")
            print("─" * 70)
            recent = self.agent.memory.conversation_history[-5:]
            for msg in recent:
                role = "👤 User" if msg["role"] == "user" else "🤖 Agent"
                print(f"{role}: {msg['content'][:80]}...")
            print()
        
        elif action == "clear":
            if input("🗑️  Clear all conversation history? (y/n): ").strip().lower() in ["y", "yes"]:
                self.agent.memory.clear_session()
                print("✅ Session cleared.\n")
        
        elif action == "export":
            exported = self.agent.memory.export_conversation()
            print(f"✅ Conversation exported to: {exported}\n")

    def handle_extend_command(self, base_file: str, reference_file: str, description: str):
        """
        Handle extend command - create new file based on template
        Example: extend:: temperature-sensor.ts ph-sensor.ts about pH water monitoring
        """
        print(f"\n🔗 Extending {base_file} for: {description}\n")
        print("⏳ Reading template and generating new version...\n")
        
        try:
            base_code = self.agent.read_file(base_file)
            if not base_code:
                print(f"❌ Base file not found: {base_file}\n")
                return
            
            # Generate based on template
            spec = f"""Create a new version of this code:
            
Original (template):
{base_code}

Make it about: {description}

Keep the same structure and patterns as the original but adapt it for the new context."""
            
            code = self.agent.generate_code(spec)
            
            self.agent.memory.add_message("user", f"Extend {base_file} for {description}", "extend")
            
            if self.confirm_action(f"Accept extended code?", code):
                file_path = input("\n💾 Save to file: ").strip()
                if file_path:
                    if self.confirm_action(f"Save to: {file_path}"):
                        self.agent.create_file(file_path, code)
                        print(f"✅ File created: {file_path}\n")
                        self.agent.memory.add_context("last_created_file", file_path)
                        self.agent.memory.add_message("assistant", f"Extended file created: {file_path}", "extend")
        
        except Exception as e:
            print(f"❌ Error: {e}\n")

    def handle_compare_command(self, file1: str, file2: str):
        """Handle compare command"""
        print(f"\n🔍 Comparing: {file1} vs {file2}\n")
        
        try:
            content1 = self.agent.read_file(file1)
            content2 = self.agent.read_file(file2)
            
            if not content1:
                print(f"❌ File not found: {file1}\n")
                return
            if not content2:
                print(f"❌ File not found: {file2}\n")
                return
            
            print("─" * 70)
            print(f"FILE 1: {file1}")
            print("─" * 70)
            print(self.format_code_preview(content1))
            print("\n" + "─" * 70)
            print(f"FILE 2: {file2}")
            print("─" * 70)
            print(self.format_code_preview(content2))
            print("\n")
            
            self.agent.memory.add_message("user", f"Compare {file1} and {file2}", "compare")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")

    def parse_command(self, user_input: str) -> tuple:
        """Parse command with double colon format"""
        if "::" not in user_input:
            return None, None, None
        
        parts = user_input.split("::", 1)
        command = parts[0].strip()
        args = parts[1].strip() if len(parts) > 1 else ""
        
        return command, args, None

    def main(self):
        """Main CLI loop"""
        self.print_header()
        print(f"Workspace: {WORKSPACE_ROOT}\n")
        print("Type 'help::' for available commands or 'exit::' to quit.\n")
        
        while True:
            try:
                user_input = input("blink> ").strip()
                
                if not user_input:
                    continue
                
                # Parse command with double colon
                command, args, _ = self.parse_command(user_input)
                
                if not command:
                    print("⚠️  Format: command:: <args>  (with double colon)\n")
                    continue
                
                command = command.lower()
                
                if command == "exit":
                    # Save session before exit
                    self.agent.memory.save_to_all_history()
                    print("\n✅ Session saved. Goodbye! 👋\n")
                    break
                
                elif command == "help":
                    self.print_help()
                
                elif command == "read":
                    if not args:
                        print("❌ Usage: read:: <file>\n")
                        continue
                    self.handle_read_command(args)
                
                elif command == "create":
                    if not args:
                        print("❌ Usage: create:: <file>\n")
                        continue
                    self.handle_create_command(args)
                
                elif command == "list":
                    directory = args if args else "."
                    files = self.agent.list_files(directory)
                    dirs = self.agent.list_directories(directory)
                    
                    print(f"\n📁 Contents of {directory}:\n")
                    for d in dirs:
                        print(f"  📂 {d}/")
                    for f in files:
                        print(f"  📄 {f}")
                    print()
                
                elif command == "generate":
                    if not args:
                        print("❌ Usage: generate:: <specification>\n")
                        continue
                    self.handle_generate_command(args)
                
                elif command == "analyze":
                    parts = args.split(maxsplit=1)
                    if len(parts) < 2:
                        print("❌ Usage: analyze:: <file> <task>\n")
                        continue
                    self.handle_analyze_command(parts[0], parts[1])
                
                elif command == "plan":
                    if not args:
                        print("❌ Usage: plan:: <objective>\n")
                        continue
                    self.handle_plan_command(args)
                
                elif command == "memory":
                    action = args if args else "summary"
                    self.handle_memory_command(action)
                
                elif command == "extend":
                    parts = args.split(maxsplit=2)
                    if len(parts) < 3:
                        print("❌ Usage: extend:: <base_file> <reference_file> <description>\n")
                        continue
                    self.handle_extend_command(parts[0], parts[1], parts[2])
                
                elif command == "compare":
                    parts = args.split(maxsplit=1)
                    if len(parts) < 2:
                        print("❌ Usage: compare:: <file1> <file2>\n")
                        continue
                    self.handle_compare_command(parts[0], parts[1])
                
                elif command == "modify":
                    parts = args.split(maxsplit=1)
                    if len(parts) < 2:
                        print("❌ Usage: modify:: <file> <new_content>\n")
                        continue
                    # This would need interactive input like create
                    print("⚠️  Use 'generate::' and 'analyze::' instead for modifications.\n")
                
                else:
                    print(f"❌ Unknown command: {command}\n")
                    print("Type 'help::' for available commands\n")
            
            except KeyboardInterrupt:
                print("\n\nSession saved. Goodbye! 👋")
                self.agent.memory.save_to_all_history()
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")


def main():
    """Entry point for enhanced CLI"""
    cli = EnhancedCLI()
    cli.main()


if __name__ == "__main__":
    main()
