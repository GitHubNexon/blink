# 🚀 AI Agent - Quick Start Guide (Simplified)

## Initial Setup

### 1. Activate Virtual Environment

```bash
# On Windows (bash/git bash)
source venv/Scripts/activate

# On Windows (cmd)
venv\Scripts\activate.bat

# On macOS/Linux
source venv/bin/activate
```

### 2. Verify Configuration

Your `.env` file has your API token. Make sure it's set!

## Running the CLI

```bash
source venv/Scripts/activate
python main.py
```

## ✨ Simple Commands (6 Only!)

✅ **read::** - Read a file
✅ **create::** - Create empty file
✅ **list::** - List files/folders (like dir)
✅ **generate::** - AI does everything (code, analyze, extend, improve, etc.)
✅ **history::** - Show conversation
✅ **help::** - Show commands

## Simple Command Format

All commands use double colon `::`

````


```
read:: <file>
create:: <file>
list:: [directory]
generate:: <instruction or path>
history::
help::
exit::
```

## Quick Examples

### 1. Read a File

```
blink> read:: myfile.ts
```

Shows file contents.

### 2. Create Empty File

```
blink> create:: new-service.ts
```

Creates an empty file.

### 3. List Files (like dir)

```
blink> list:: .
blink> list:: src/modules
```

Shows folders and files.

### 4. Generate Code (Super Powerful!)

```
blink> generate:: Create a sensor service in TypeScript
blink> generate:: "C:\path\to\file.ts" Add error handling
blink> generate:: "C:\path\to\file1.ts" Create pH variant like "C:\path\to\file2.ts"
```

The `generate::` command can:
- ✅ Create new code from scratch
- ✅ Improve existing code
- ✅ Analyze and refactor
- ✅ Create variants/extensions
- ✅ Plan projects
- ✅ Everything in ONE command!

### 5. View Conversation

```
blink> history::
```

Shows all previous conversations.

### 6. Help

```
blink> help::
```

Shows all commands.

### 7. Exit

```
blink> exit::
```

Saves and exits.

## Available Commands

| Command      | Usage                  | Description                           |
| ------------ | ---------------------- | ------------------------------------- |
| `read::`     | `read:: <file>`        | Read a file                           |
| `create::`   | `create:: <file>`      | Create empty file                     |
| `list::`     | `list:: [directory]`   | List files/folders (like dir)         |
| `generate::` | `generate:: <anything>`| AI generates/improves/analyzes/plans |
| `history::`  | `history::`            | Show conversation history             |
| `help::`     | `help::`               | Show this help                        |
| `exit::`     | `exit::`               | Exit and save                         |

## How to Use generate::

The `generate::` command is powerful and flexible:

### Create new code:
```
blink> generate:: Create a function that validates phone numbers
```

### Improve existing code:
```
blink> generate:: "C:\path\to\file.ts" Add TypeScript strict mode and error handling
```

### Create variant:
```
blink> generate:: "C:\path\to\temperature-sensor.ts" Create pH water sensor version like "C:\path\to\ph-sensor.ts"
```

### Analyze project:
```
blink> generate:: "C:\path\to\folder" Create a complete API structure with all endpoints
```

The AI understands context and will:
- Read the path you provide
- Understand what you want
- Generate/improve/analyze accordingly
- Show results
- Ask if you want to save

## Files and Workspace

- **Workspace**: `workspace/` - Your project files
- **History**: `workspace/.agent_history/` - Conversation history
- **Source Code**: `src/` - Agent code

## Troubleshooting

### "Format: command:: <args> (with double colon)"
Use `::` not `:` - Example: `read:: file.py` (correct), not `read: file.py` (wrong)

### "File not found"
Use `list::` to see available files first

### "REPLICATE_API_TOKEN is not set"
Edit `.env` and add your API token

### "Module not found"
Activate venv: `source venv/Scripts/activate`

## Next Steps

1. Run: `python main.py`
2. Type: `help::`
3. Try: `generate:: Create a Python function that calculates factorial`
4. Try: `create:: test.py`
5. Try: `read:: test.py`
6. Try: `history::`

That's it! Simple and powerful. 🚀
````
