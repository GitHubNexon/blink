"""Command-line interface for the AI Agent"""

import sys
from pathlib import Path
from src.agent import CodeAgent
from src.config import WORKSPACE_ROOT


def print_header():
    """Print CLI header"""
    print("\n" + "=" * 60)
    print("🤖  AI Agentic Code Generator")
    print("   Powered by Replicate.com")
    print("=" * 60 + "\n")


def print_help():
    """Print help message"""
    print("Available Commands:")
    print("  read <file>              - Read a file from workspace")
    print("  create <file>            - Create a new file")
    print("  list [directory]         - List files in directory")
    print("  generate <spec>          - Generate code from specification")
    print("  analyze <file> <task>    - Analyze and modify code")
    print("  plan <objective>         - Create a task plan")
    print("  refactor <file> <rules>  - Refactor code in file")
    print("  help                     - Show this help message")
    print("  exit                     - Exit the CLI")
    print()


def main():
    """Main CLI loop"""
    print_header()
    print(f"Workspace: {WORKSPACE_ROOT}\n")
    
    agent = CodeAgent()
    
    print("Type 'help' for available commands or 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("blink> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else None
            
            if command == "exit":
                print("\nGoodbye! 👋")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "read":
                if not args:
                    print("❌ Please specify a file path")
                    continue
                
                content = agent.read_file(args)
                if content:
                    print(f"\n📄 Contents of {args}:\n")
                    print(content)
                    print()
                else:
                    print(f"❌ File not found: {args}\n")
            
            elif command == "create":
                if not args:
                    print("❌ Please specify a file path")
                    continue
                
                print("Enter file content (type END on a new line to finish):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                
                content = "\n".join(lines)
                result = agent.create_file(args, content)
                print(f"✅ File created: {result}\n")
            
            elif command == "list":
                directory = args if args else "."
                files = agent.list_files(directory)
                dirs = agent.list_directories(directory)
                
                print(f"\n📁 Contents of {directory}:\n")
                for d in dirs:
                    print(f"  📂 {d}/")
                for f in files:
                    print(f"  📄 {f}")
                print()
            
            elif command == "generate":
                if not args:
                    print("❌ Please specify code specification")
                    continue
                
                print("\n🔄 Generating code...\n")
                code = agent.generate_code(args)
                print("Generated code:")
                print("-" * 60)
                print(code)
                print("-" * 60)
                
                save = input("\nSave to file? (y/n): ").strip().lower()
                if save == "y":
                    file_path = input("Enter file path: ").strip()
                    agent.create_file(file_path, code)
                    print(f"✅ Saved to {file_path}\n")
                else:
                    print()
            
            elif command == "analyze":
                parts = args.split(maxsplit=1) if args else []
                if len(parts) < 2:
                    print("❌ Usage: analyze <file> <task>")
                    continue
                
                file_path, task = parts[0], parts[1]
                print(f"\n🔄 Analyzing {file_path}...\n")
                
                result = agent.analyze_code(agent.read_file(file_path), task)
                print("Analysis result:")
                print("-" * 60)
                print(result)
                print("-" * 60)
                print()
            
            elif command == "plan":
                if not args:
                    print("❌ Please specify an objective")
                    continue
                
                print("\n🔄 Creating plan...\n")
                plan = agent.execute_plan(args)
                print(f"\n✅ Plan created with {len(plan['steps'])} steps\n")
            
            elif command == "refactor":
                parts = args.split(maxsplit=1) if args else []
                if len(parts) < 2:
                    print("❌ Usage: refactor <file> <rules>")
                    continue
                
                file_path, rules = parts[0], parts[1]
                print(f"\n🔄 Refactoring {file_path}...\n")
                
                result = agent.refactor_code(file_path, rules)
                print("Refactored code:")
                print("-" * 60)
                print(result)
                print("-" * 60)
                print(f"\n✅ File updated: {file_path}\n")
            
            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
