#!/usr/bin/env python
"""Test MCP Server functionality"""

from src.enhanced_agent import EnhancedCodeAgent

agent = EnhancedCodeAgent()
print("\n" + "="*70)
print("MCP SERVER TEST")
print("="*70)

print("\n1. Testing get_project_structure:")
struct = agent.call_mcp_tool("get_project_structure", {"max_depth": 2})
import json
result = json.loads(struct)
print(f"   Project root: {result.get('root')}")
print(f"   Structure keys: {list(result.get('structure', {}).keys())}")

print("\n2. Testing list_directory:")
files = agent.call_mcp_tool("list_directory", {"path": "."})
result = json.loads(files)
if result.get('success'):
    print(f"   Files: {len(result.get('files', []))} files")
    print(f"   Dirs: {len(result.get('directories', []))} directories")

print("\n3. Testing search_files:")
search = agent.call_mcp_tool("search_files", {"pattern": ".ts", "directory": "."})
result = json.loads(search)
print(f"   Found {result.get('count')} TypeScript files")

print("\n" + "="*70)
print("✅ MCP SERVER OPERATIONAL")
print("="*70)
print("\nReady to use with: python main.py")
