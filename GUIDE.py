"""
🤖 ENHANCED AI AGENT - Complete Guide
====================================

This is an advanced AI code agent with Copilot-like behavior, conversation memory,
and confirmation prompts before execution.

NEW FEATURES (v2.0)
===================

1. ✅ COPILOT-LIKE CONFIRMATION PROMPTS
   - AI proposes action before execution
   - You review the preview
   - You decide: Accept (y), Reject (n), Edit (e), or Undo (u)

2. ✅ CONVERSATION MEMORY & HISTORY
   - Agent remembers all previous conversations
   - Tracks file paths and context
   - Can reference earlier commands in the same session
   - Exports conversation to markdown

3. ✅ NEW COMMAND FORMAT (Double Colon ::)
   - read:: <file>
   - create:: <file>
   - generate:: <specification>
   - analyze:: <file> <task>
   - plan:: <objective>
   - extend:: <base> <reference> <description>
   - compare:: <file1> <file2>
   - memory:: [summary|history|clear|export]
   - help::
   - exit::

4. ✅ NEW COMMANDS
   - extend:: - Create new file based on existing template
   - compare:: - Compare two files side-by-side
   - memory:: - Manage conversation history

INSTALLATION
============

1. Virtual Environment (already set up):
   source venv/Scripts/activate

2. Dependencies (already installed):
   - requests (for API calls)
   - python-dotenv (for .env loading)

3. Run:
   python main.py

COMMAND FORMAT
==============

OLD FORMAT (no longer supported):
  read file.py
  create file.py
  generate Create a function

NEW FORMAT (with double colon):
  read:: file.py
  create:: file.py
  generate:: Create a function

WHY DOUBLE COLON?
- Clearer command separation
- Easier to parse arguments
- Matches professional CLI tools
- Looks like a namespace operator

DETAILED COMMAND REFERENCE
===========================

1. READ:: - Read and display file contents
─────────────────────────────────────────
Usage: read:: <file_path>

Example:
  blink> read:: C:\path\to\temperature-sensor.service.ts
  
Output:
  📖 Reading file: temperature-sensor.service.ts
  [File contents displayed]
  
Saved in memory: last_read_file = temperature-sensor.service.ts

---

2. CREATE:: - Create new file with confirmation
─────────────────────────────────────────────────
Usage: create:: <file_path>

Example:
  blink> create:: new-sensor.service.ts
  Enter file content (type END on a new line to finish):
  [Your code here]
  END
  
  🔮 PROPOSED ACTION: Create file: new-sensor.service.ts
  📄 PREVIEW: [shows your code]
  ✓ Accept (y/yes) | ✗ Reject (n/no): y
  
  ✅ File created: new-sensor.service.ts

Saved in memory: last_created_file = new-sensor.service.ts

---

3. GENERATE:: - AI-powered code generation WITH PREVIEW
────────────────────────────────────────────────────────
Usage: generate:: <specification>

Example:
  blink> generate:: Create a pH water sensor service based on temperature sensor pattern
  
  ⏳ Please wait, AI is thinking...
  
  🔮 PROPOSED ACTION: Accept generated code?
  📄 PREVIEW:
  [Generated code shown here]
  
  ✓ Accept (y/yes) | ✗ Reject (n/no): y
  
  💾 Save to file (or press Enter to skip): ph-sensor.service.ts
  
  ✓ Accept (y/yes) | ✗ Reject (n/no): y
  ✅ Code saved to: ph-sensor.service.ts

Key differences from v1:
- Shows preview BEFORE saving
- You must confirm the generated code
- Option to skip saving
- Option to save to different file
- Remembers context from previous commands

---

4. ANALYZE:: - Analyze code WITH IMPROVEMENTS PREVIEW
───────────────────────────────────────────────────────
Usage: analyze:: <file> <improvement_task>

Example:
  blink> analyze:: temperature-sensor.service.ts Add TypeScript strict type hints and comprehensive error handling
  
  🔍 Analyzing: temperature-sensor.service.ts
  Task: Add TypeScript strict type hints and comprehensive error handling
  
  ⏳ Analyzing code...
  
  🔮 PROPOSED ACTION: Accept improvements?
  📄 PREVIEW: [Shows improved code]
  
  ✓ Accept (y/yes) | ✗ Reject (n/no): y
  
  💾 Overwrite original file? (y/n): y
  ✅ File updated: temperature-sensor.service.ts

---

5. EXTEND:: - Create variant of file (NEW!)
─────────────────────────────────────────────
Usage: extend:: <base_file> <reference_file> <description>

SPECIAL COMMAND FOR YOUR USE CASE!

Example:
  blink> extend:: C:\path\to\temperature-sensor.service.ts C:\path\to\ph-water-sensor.service.ts about pH water quality monitoring

What it does:
  1. Reads the temperature sensor code (template)
  2. Understands the pattern and structure
  3. AI creates pH water sensor version
  4. Keeps the same patterns but adapts for pH monitoring
  5. Shows preview before saving

  🔗 Extending temperature-sensor.service.ts for: about pH water quality monitoring
  
  ⏳ Reading template and generating new version...
  
  🔮 PROPOSED ACTION: Accept extended code?
  📄 PREVIEW: [pH sensor code based on temperature pattern]
  
  ✓ Accept (y/yes) | ✗ Reject (n/no): y
  
  💾 Save to file: new-ph-sensor.service.ts
  ✅ File created: new-ph-sensor.service.ts

---

6. COMPARE:: - Compare two files (NEW!)
──────────────────────────────────────────
Usage: compare:: <file1> <file2>

Example:
  blink> compare:: temperature-sensor.service.ts ph-water-sensor.service.ts
  
  🔍 Comparing: temperature-sensor.service.ts vs ph-water-sensor.service.ts
  
  ────────────────────────────────────────────────────────────────────
  FILE 1: temperature-sensor.service.ts
  ────────────────────────────────────────────────────────────────────
  [First 20 lines of FILE 1]
  
  ────────────────────────────────────────────────────────────────────
  FILE 2: ph-water-sensor.service.ts
  ────────────────────────────────────────────────────────────────────
  [First 20 lines of FILE 2]

---

7. PLAN:: - Break down objective WITH CONFIRMATION
─────────────────────────────────────────────────────
Usage: plan:: <objective>

Example:
  blink> plan:: Build a water quality monitoring system with temperature, pH, and dissolved oxygen sensors
  
  📋 Planning: Build a water quality monitoring system...
  
  ⏳ Creating plan...
  
  🔮 PROPOSED ACTION: Accept plan?
  
  PREVIEW:
  1. Create sensor service base class
  2. Implement temperature sensor service
  3. Implement pH water sensor service
  4. Implement dissolved oxygen sensor service
  5. Create sensor manager service
  6. Add real-time data aggregation
  ... (10 steps total)
  
  ✓ Accept (y/yes) | ✗ Reject (n/no): y
  ✅ Plan accepted!

---

8. MEMORY:: - Manage conversation (NEW!)
───────────────────────────────────────────
Usage: memory:: [summary|history|clear|export]

Example 1 - View summary:
  blink> memory:: summary
  
  Session Summary:
  Total messages: 12
  User queries: 6
  Commands used: {'read': 2, 'generate': 1, 'extend': 1, 'analyze': 1, 'compare': 1}
  Context variables: 7

Example 2 - View recent history:
  blink> memory:: history
  
  📜 Recent Conversation History:
  ────────────────────────────────────────────────────────────────────
  👤 User: read:: temperature-sensor.service.ts
  🤖 Agent: File content shown (first 20 lines)
  👤 User: generate:: Create pH water sensor...
  🤖 Agent: Generated code with 150 lines
  ...

Example 3 - Export to file:
  blink> memory:: export
  ✅ Conversation exported to: workspace/conversation_export.md
  
  Creates markdown file with full conversation history

Example 4 - Clear history:
  blink> memory:: clear
  🗑️  Clear all conversation history? (y/n): y
  ✅ Session cleared.

---

9. LIST:: - List files and directories
──────────────────────────────────────
Usage: list:: [directory]

Example:
  blink> list:: .
  
  📁 Contents of .:
  
    📂 models/
    📂 services/
    📂 sensors/
    📄 config.ts
    📄 index.ts

---

10. HELP:: - Show all commands
──────────────────────────────
Usage: help::

Shows complete command reference with examples.

---

11. EXIT:: - Exit the CLI (saves history)
───────────────────────────────────────────
Usage: exit::

Saves current session to history and exits.

RESPONSE OPTIONS
================

When AI proposes an action, you have 4 choices:

✓ YES (y / yes)
  - Accept the action
  - Confirms the proposed code/plan
  - Proceeds with execution

✗ NO (n / no)
  - Reject the action
  - Goes back to prompt
  - Nothing is saved/modified

📝 EDIT (e / edit)
  - Edit the proposed code
  - Coming in future version
  - Currently shows "not yet implemented"

↶ UNDO (u / undo)
  - Undo last action
  - Revert to previous state
  - Currently shows "coming soon"

WORKFLOW EXAMPLE
================

Scenario: Create pH water sensor based on temperature sensor

Step 1: Read template
──────────────────────
blink> read:: C:\Smart-Fishpond\server\src\modules\sensors\services\temperature-sensor.service.ts

Step 2: Extend it for pH
──────────────────────────
blink> extend:: C:\Smart-Fishpond\server\src\modules\sensors\services\temperature-sensor.service.ts C:\Smart-Fishpond\server\src\modules\sensors\services\ph-water-sensor.service.ts about pH water monitoring

[Confirms the generated pH sensor code]

Step 3: Analyze and improve
──────────────────────────────
blink> analyze:: ph-water-sensor.service.ts Add error handling and validation for pH values (0-14)

[Confirms the improved code]

Step 4: Compare them
─────────────────────
blink> compare:: temperature-sensor.service.ts ph-water-sensor.service.ts

[View both files side by side]

Step 5: Check memory
──────────────────────
blink> memory:: summary

[See what you've done in this session]

CONVERSATION MEMORY FEATURES
=============================

What the agent remembers:
✓ Every command you typed
✓ Every AI response
✓ File paths you've accessed
✓ Files you've created/modified
✓ Context variables

How it helps:
- References previous commands
- Suggests related files
- Remembers your preferences
- Provides context for better AI responses
- Learns what you're working on

Storage:
- Current session: workspace/.agent_history/current_session.json
- All history: workspace/.agent_history/all_history.json
- Export: workspace/conversation_export.md

ADVANCED TIPS
=============

1. Use full file paths with extend::
   blink> extend:: C:\project\src\old.ts C:\project\src\new.ts about new feature

2. Chain commands together
   - Read template
   - Extend it
   - Analyze improvements
   - Compare results
   - Check memory

3. Export conversation for documentation
   blink> memory:: export
   Then review the markdown file

4. Use clear specifications
   - BAD: "Create a sensor"
   - GOOD: "Create a pH water sensor service with real-time monitoring"

5. Reference previous context
   AI remembers what you talked about earlier
   You don't need to repeat file paths

TROUBLESHOOTING
===============

Issue: "Format: command:: <args> (with double colon)"
→ Use double colon :: not single colon :
→ Correct: read:: file.py
→ Wrong: read: file.py

Issue: Command not working
→ Make sure venv is activated
→ source venv/Scripts/activate

Issue: "File not found"
→ Use list:: to see available files
→ Use full file paths for extend::

Issue: API errors
→ Check .env file has valid token
→ Check internet connection
→ Check Replicate API status

Issue: Memory/history not saving
→ Make sure workspace/ directory exists
→ Check write permissions
→ Try: mkdir workspace/.agent_history

GETTING STARTED NOW
====================

1. Activate environment:
   source venv/Scripts/activate

2. Start CLI:
   python main.py

3. See all commands:
   help::

4. First command - read a file:
   read:: filename.py

5. Generate code:
   generate:: Create a function to reverse a list

6. View what you did:
   memory:: summary

7. Exit:
   exit::

QUICK REFERENCE
===============

Command        | Format                          | Purpose
────────────────────────────────────────────────────────────────
read::         | read:: <file>                   | View file contents
create::       | create:: <file>                 | Create new file
list::         | list:: [dir]                    | List files
generate::     | generate:: <spec>               | AI code generation
analyze::      | analyze:: <file> <task>         | AI code improvement
plan::         | plan:: <objective>              | Create task plan
extend::       | extend:: <base> <ref> <desc>    | Create variant file
compare::      | compare:: <file1> <file2>       | Compare two files
memory::       | memory:: [action]               | View conversation
help::         | help::                          | Show commands
exit::         | exit::                          | Exit and save

That's it! You now have a professional AI agent with Copilot-like behavior.

Happy coding! 🚀
"""

if __name__ == "__main__":
    print(__doc__)
