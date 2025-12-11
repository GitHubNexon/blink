# 🚀 Blink MCP Server

**MCP (Model Context Protocol) Server** for the Blink AI Agent - Enables Claude to autonomously access files, explore projects, and understand code structure.

## What is MCP?

MCP is a protocol that lets AI models (Claude) call tools/functions to interact with external systems. Instead of just sending text, Claude can:

- ✅ Read files when it needs context
- ✅ Explore project structure
- ✅ Search for related code
- ✅ Understand file metadata

## Architecture

```
User Input
    ↓
CLI (simplified_cli.py)
    ↓
EnhancedCodeAgent (with MCP)
    ↓
BlinkMCPServer (provides tools)
    ↓
Claude API (uses tools autonomously)
    ↓
Generated Code (TypeScript/Python/etc)
```

## Available MCP Tools

### 1. `read_file`

Read the full contents of a file

```
Tool: read_file
Input: {"path": "src/services/sensor.ts"}
Output: {
  "success": true,
  "language": "TypeScript",
  "size": 1024,
  "lines": 45,
  "content": "..."
}
```

### 2. `list_directory`

List files and folders in a path

```
Tool: list_directory
Input: {"path": "src/modules"}
Output: {
  "success": true,
  "directories": ["sensors", "controllers"],
  "files": ["index.ts", "config.ts"],
  "file_count": 2,
  "dir_count": 2
}
```

### 3. `search_files`

Search for files matching a pattern

```
Tool: search_files
Input: {"pattern": "sensor", "directory": "src"}
Output: {
  "success": true,
  "matches": ["src/services/temperature-sensor.ts", "src/services/ph-sensor.ts"],
  "count": 2
}
```

### 4. `get_file_info`

Get metadata without reading full content

```
Tool: get_file_info
Input: {"path": "src/services/sensor.ts"}
Output: {
  "success": true,
  "language": "TypeScript",
  "size": 1024,
  "size_kb": 1.0,
  "lines": 45,
  "extension": ".ts"
}
```

### 5. `get_project_structure`

Get overview of project organization

```
Tool: get_project_structure
Input: {"max_depth": 3}
Output: {
  "success": true,
  "structure": {
    "src/": {
      "services/": {...},
      "models/": {...}
    }
  }
}
```

## How It Works

### Before MCP (Old Way):

1. You tell the CLI: "Create pH sensor from temperature sensor"
2. CLI reads temperature-sensor.ts, embeds full content in prompt
3. Claude receives: "Here's the full file... generate code..."
4. Problem: Claude doesn't know it's TypeScript, generates Python

### With MCP (New Way):

1. You tell the CLI: "Create pH sensor from temperature sensor"
2. CLI tells Claude about MCP tools available
3. Claude intelligently calls `read_file` to examine the temperature-sensor.ts
4. Claude sees it's TypeScript, understands the patterns
5. Claude generates TypeScript code that matches the original

## Benefits

✅ **Context-aware** - Claude reads what it needs, when it needs it
✅ **Language-aware** - Claude understands file types and generates correct language
✅ **Token-efficient** - Only reads relevant parts, saves API costs
✅ **Scalable** - Works with large codebases
✅ **Smart** - Claude can explore dependencies and related files

## Usage

### Using the MCP Server Directly:

```python
from src.enhanced_agent import EnhancedCodeAgent

agent = EnhancedCodeAgent()

# Get tools available
tools = agent.get_mcp_tools()

# Call a tool directly
result = agent.call_mcp_tool("read_file", {"path": "src/app.ts"})
```

### Through the CLI:

```bash
python main.py
```

Then use `generate::` command as usual:

```
generate:: create pH sensor version from "src/temperature-sensor.ts" like "src/ph-sensor.ts"
```

The CLI will:

1. Use MCP to get file info
2. Pass enhanced instruction to Claude with MCP tools
3. Claude uses tools to examine files
4. Generate correct TypeScript code

## Implementation Files

- **`src/mcp_server.py`** - BlinkMCPServer class with all tools
- **`src/enhanced_agent.py`** - EnhancedCodeAgent that uses MCP
- **`src/simplified_cli.py`** - Updated CLI with MCP integration

## Testing

```bash
# Test MCP server
python test_mcp.py

# Use enhanced CLI
python main.py
```

## Next Steps

The MCP server is fully functional and integrated. Claude now:

- ✅ Has tools to autonomously access files
- ✅ Understands project structure
- ✅ Generates code in the correct language
- ✅ Uses context intelligently

Just use `python main.py` as normal - the MCP magic happens behind the scenes!
