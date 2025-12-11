# Chat Command Guide

## Overview

The `chat::` command is a conversational AI interface that lets you interact naturally with the AI agent. Unlike `generate::` which is optimized for file-based code generation, `chat::` is perfect for:

- Multi-line conversations
- Pasting code examples and asking for improvements
- Asking questions about code patterns
- Iterative discussions about implementation

## Basic Usage

```bash
blink> chat:: <your initial request>
```

When you run the command, the AI will:

1. Show `[PROCESSING]` message
2. Wait for you to type your full message or paste code
3. Accept multi-line input
4. Show `end` to finish (type just `end` on a new line)
5. Display the AI's response
6. Offer to save the code if desired

## Examples

### Example 1: Create a Temperature Sensor Simulation

```bash
blink> chat:: Create a simulation of how temperature sensor works in python
[INFO] Type your message or paste code (type 'end' on new line when done):

[Paste Python code or additional instructions]

end
```

Output:

```
[PROCESSING] Analyzing your request...

─────────────────────────────────────────────────────────
[Generated code or explanation]
─────────────────────────────────────────────────────────

[SAVE?] Save generated code to file? (y/n):
```

### Example 2: Improve Existing Code

```bash
blink> chat:: Improve this function

[Paste the code you want improved]

end
```

### Example 3: Ask About Code Patterns

```bash
blink> chat:: How would you handle error handling in this REST API?

[Paste your API code]

end
```

## How It Works Internally

1. **Input Collection**

   - Initial request from command line
   - Multi-line input follows (until you type `end`)
   - All text is combined into a single message

2. **Processing**

   - Message sent to Claude with conversational context
   - AI understands this is a chat interaction (vs file-based operations)
   - Full context from your workspace is available

3. **Output**

   - AI response displayed with visual separators
   - Option to save code to a file
   - Conversation logged to session history

4. **Memory**
   - Entire chat logged to `workspace/.agent_history/current_session.json`
   - Accessible via `history::` command
   - Persists across sessions

## Command Dispatch

In `src/simplified_cli.py`, the chat command is handled by:

```python
elif command == "chat":
    if not args:
        print("[ERROR] Usage: chat:: <request>\n")
        continue
    self.handle_chat_command(args)
```

The `handle_chat_command()` method:

- Accepts initial request
- Collects multi-line input
- Calls `self.agent.client.generate()` with chat context
- Handles file saving
- Logs to conversation memory

## Difference from generate::

| Feature     | generate::              | chat::                     |
| ----------- | ----------------------- | -------------------------- |
| Input       | Single-line instruction | Multi-line, can paste code |
| Focus       | File operations         | Conversation               |
| Context     | File-based              | Free-form                  |
| Save Option | Built-in with prompts   | Available after generation |
| Use Case    | Quick code generation   | Discussion & iteration     |
| Memory      | Logged per command      | Full conversation logged   |

## Tips

1. **Multi-line Pasting**: Paste your entire code block, then type `end` on a new line
2. **File Context**: You can mention files from your workspace in the chat
3. **Save Generated Code**: When asked, save generated code to easily add it to your project
4. **Conversation Flow**: Each chat is logged separately in your session history
5. **No File Required**: Unlike `generate::`, you don't need to reference specific files

## Files Modified for This Feature

- `src/simplified_cli.py` - Added `handle_chat_command()` method and command dispatch
- `README.md` - Updated with chat command documentation
- `src/simplified_cli.py` - Updated `print_help()` with chat examples

## Testing the Command

```bash
# Activate your venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Blink
python main.py

# Try the chat command
blink> chat:: Create a simple Python class for managing user profiles
[Type more instructions or paste code]
end

# Should see AI response and save option
```

## Troubleshooting

**Q: Chat seems to hang after I type the initial command?**
A: The command waits for you to type your full message. Either type more lines or type `end` to finish.

**Q: My code wasn't analyzed properly?**
A: Make sure to paste the complete code block and type `end` on a new line after.

**Q: Where is my chat history saved?**
A: In `workspace/.agent_history/current_session.json`. View it with `history::` command.

**Q: Can I chat with code examples from external files?**
A: Yes! You can paste code from external files, or mention file paths in your chat request.
