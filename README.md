# Blink - Your Vibe Coder Agent Buddy

An AI-powered agentic command-based assistant that can read, create, and modify code files with intelligent assistance from Replicate's Claude models.

## 🚀 Quick Start (3 Ways to Use)

| Version          | How to Run                   | Best For      |
| ---------------- | ---------------------------- | ------------- |
| **EXE App**      | Download from Releases & run | ⭐ Most Users |
| **Python (Raw)** | `python main.py`             | Developers    |
| **Source Code**  | Clone & modify               | Contributors  |

👉 **New users?** Start with [INSTALLATION.md](INSTALLATION.md) for detailed setup guide

🔑 **Token handling:** The EXE prompts for your API token on startup, validates it, and clears it when you exit. Super secure!

## Features

✅ **Read Files** - Access project files directly (workspace or external paths)
✅ **Create Files** - Generate new files with AI assistance  
✅ **List Files** - Browse your project structure
✅ **Code Generation** - Create code from AI instructions with full context
✅ **Session History** - Track all conversations and commands
✅ **Session Management** - Clear and organize your workspace

## Setup

### Option 1: Download & Run EXE (Easiest!)

The best way for most users - just download and run!

1. **Download** `Blink.exe` from [Releases](https://github.com/yourusername/blink/releases)

2. **Double-click** `Blink.exe` to run

3. **Enter your API token** when prompted (one-time validation each run)

4. **Start using Blink!**

**How it works:**

- App prompts for your token on startup ✅
- Token is validated immediately ✅
- Token is cleared when you exit ✅
- Token NEVER saved to disk ✅
- Super secure! 🔒

### Option 2: Run as Python (For Developers)

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/blink.git
   cd blink
   ```

2. Create and activate virtual environment

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate.bat
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run Blink
   ```bash
   python main.py
   ```
   (Will prompt for API token)

Clone, install dependencies, and modify as you like!

## Usage

### Interactive CLI

```bash
python main.py
```

Available commands (all use `::` delimiter):

- `read:: <file>` - Read a file from workspace or external path
- `create:: <file>` - Create a new empty file
- `list:: [directory]` - List files and folders in directory
- `generate:: <instruction>` - AI code generation with full project context
- `history::` - Show conversation history from current session
- `clear::` - Clear current session and conversation history
- `help::` - Show help message
- `exit::` - Save session and exit the CLI

### Command Examples

```bash
# Read a local file
blink> read:: src/main.ts

# Read from external project
blink> read:: "C:\path\to\project\file.ts"

# Create a new file
blink> create:: new-service.ts

# List directory
blink> list:: src/

# Generate code with AI
blink> generate:: Create a TypeScript validator function

# View conversation history
blink> history::

# Clear session
blink> clear::

# Show all commands
blink> help::

# Exit
blink> exit::
```

## Project Structure

```
blink/
├── .env                    # API credentials (add your token here)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── main.py                      # CLI entry point
├── workspace/                   # Project workspace (created automatically)
└── src/
    ├── __init__.py
    ├── config.py                # Configuration management
    ├── robust_file_handler.py   # Cross-platform file operations
    ├── replicate_api.py         # Replicate API integration
    ├── enhanced_agent.py        # Main agent logic with MCP
    ├── mcp_server.py            # MCP server for autonomous tool access
    ├── conversation_memory.py   # Session memory and history
    └── simplified_cli.py        # Modern CLI interface
```

## Example Workflow

### 1. Read existing code

```
blink> read:: src/ph-sensor.service.ts
```

### 2. Generate code from specification

```
blink> generate:: Add error handling and logging to the sensor service
```

### 3. Create a new file with generated code

```
blink> create:: new-service.ts
(Then use generate:: to populate it with AI-generated code)
```

### 4. View conversation history

```
blink> history::
```

### 5. Save and exit

```
blink> exit::
```

## Requirements

- Python 3.8+
- Replicate API token (free tier available)
- Internet connection

## Models Supported

- `anthropic/claude-4.5-sonnet` (recommended) - Latest, most capable
- `anthropic/claude-3.5-sonnet` - Fast and efficient
- Other Replicate-hosted Claude models

## How Blink Works

**Agentic AI with MCP (Model Context Protocol)**

Blink uses an intelligent agent that:

- Reads files from your workspace and external projects
- Maintains conversation history across sessions
- Has access to your project structure via MCP tools
- Provides context-aware code generation
- Supports both relative and absolute file paths

## Troubleshooting

### "REPLICATE_API_TOKEN is not set"

Make sure you've added your token to the `.env` file:

```env
REPLICATE_API_TOKEN=your_actual_token_here
```

### API Rate Limits

If you hit rate limits, wait a moment before retrying. Free tier has limits on requests.

### File Not Found

Make sure file paths are relative to the workspace directory or use absolute paths.

## License

MIT

## Support

For issues or questions:

1. Check your API token in `.env`
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify internet connection for API calls
4. Use `help::` command within Blink for command reference
