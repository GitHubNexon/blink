"""Example usage of the AI Agent"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import CodeAgent


def example_basic_operations():
    """Example 1: Basic file operations"""
    print("\n" + "="*60)
    print("Example 1: Basic File Operations")
    print("="*60 + "\n")
    
    agent = CodeAgent()
    
    # Create a simple file
    print("Creating a simple Python file...")
    agent.create_file("hello.py", 'print("Hello from AI Agent!")')
    
    # Read the file
    print("Reading the file back...")
    content = agent.read_file("hello.py")
    print(f"File content:\n{content}\n")
    
    # List files
    print("Files in workspace:")
    files = agent.list_files(".")
    for f in files:
        print(f"  - {f}")
    print()


def example_code_generation():
    """Example 2: Code generation"""
    print("\n" + "="*60)
    print("Example 2: Code Generation")
    print("="*60 + "\n")
    
    agent = CodeAgent()
    
    spec = """Create a Python function that:
    - Takes a list of numbers as input
    - Returns a dictionary with sum, average, min, and max values
    - Handles empty lists gracefully"""
    
    print(f"Specification:\n{spec}\n")
    print("Generating code...")
    
    code = agent.generate_code(spec)
    
    print(f"\nGenerated code:\n")
    print(code)
    
    # Save the generated code
    agent.create_file("stats_function.py", code)
    print("\n✅ Code saved to stats_function.py")


def example_code_analysis():
    """Example 3: Code analysis"""
    print("\n" + "="*60)
    print("Example 3: Code Analysis and Improvement")
    print("="*60 + "\n")
    
    agent = CodeAgent()
    
    # Create a simple file with basic code
    original_code = """def calc(x, y):
    return x + y

def process(data):
    result = []
    for i in data:
        result.append(i * 2)
    return result"""
    
    print(f"Original code:\n{original_code}\n")
    
    agent.create_file("basic_code.py", original_code)
    
    print("Analyzing and improving code...")
    
    improved = agent.analyze_code(
        original_code,
        "Add type hints, docstrings, make it more Pythonic using list comprehensions"
    )
    
    print(f"\nImproved code:\n")
    print(improved)
    
    # Save improved version
    agent.modify_file("basic_code.py", improved)
    print("\n✅ Improved code saved to basic_code.py")


def example_task_planning():
    """Example 4: Task planning"""
    print("\n" + "="*60)
    print("Example 4: Task Planning")
    print("="*60 + "\n")
    
    agent = CodeAgent()
    
    objective = "Build a simple web scraper using Python"
    
    print(f"Objective: {objective}\n")
    print("Creating a plan...\n")
    
    plan = agent.execute_plan(objective)
    
    print("\n✅ Plan created successfully!")


def example_full_workflow():
    """Example 5: Full workflow"""
    print("\n" + "="*60)
    print("Example 5: Full Workflow - Data Analysis Tool")
    print("="*60 + "\n")
    
    agent = CodeAgent()
    
    # Step 1: Plan
    print("📋 Step 1: Planning the project...")
    objective = "Create a data analysis module that reads CSV files and provides statistics"
    plan = agent.execute_plan(objective)
    
    # Step 2: Generate code
    print("\n🔨 Step 2: Generating main module...")
    spec = """Create a Python module 'data_analyzer.py' with a DataAnalyzer class that:
    - Loads CSV files using pandas
    - Provides statistical summaries (mean, median, std dev)
    - Can filter data by column values
    - Has a method to export results to JSON"""
    
    code = agent.generate_code(spec)
    agent.create_file("data_analyzer.py", code)
    print("✅ Generated data_analyzer.py")
    
    # Step 3: Create a test file
    print("\n🧪 Step 3: Creating test examples...")
    test_code = """# Example usage of DataAnalyzer
# Place sample CSV file in workspace and run:
# 
# from data_analyzer import DataAnalyzer
# 
# analyzer = DataAnalyzer('data.csv')
# print(analyzer.get_statistics())
# filtered = analyzer.filter_by('category', 'A')
# analyzer.export_results('results.json')
"""
    agent.create_file("test_example.py", test_code)
    print("✅ Created test_example.py")
    
    # Step 4: List all created files
    print("\n📁 Step 4: Project files created:")
    files = agent.list_files(".")
    for f in files:
        print(f"  ✓ {f}")
    
    print("\n" + "="*60)
    print("✅ Workflow completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("\n🤖 AI Agent Examples\n")
    
    try:
        # Uncomment examples to run them
        
        # Basic operations
        example_basic_operations()
        
        # Code generation
        example_code_generation()
        
        # Code analysis
        example_code_analysis()
        
        # Task planning
        example_task_planning()
        
        # Full workflow
        # example_full_workflow()
        
        print("\n✅ All examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
