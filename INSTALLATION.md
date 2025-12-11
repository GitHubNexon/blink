# Blink - Installation & Deployment Guide

Welcome! This guide explains the 3 ways to use Blink:

1. **App Version (EXE)** - Standalone executable (recommended for most users)
2. **Raw Version** - Direct Python execution (for developers)
3. **Source Code** - Clone and contribute (for contributors)

---

## Quick Start (Choose Your Path)

### Option 1: App Version (EXE Executable) - RECOMMENDED

The easiest way - download and run!

#### What You Need

- Windows 10+ (or macOS/Linux if built from source)
- Internet connection
- Your Replicate API token (get free at https://replicate.com/signin)

#### How It Works

1. Download `Blink.exe` from [Releases](https://github.com/yourusername/blink/releases)
2. Double-click to run
3. Enter your API token when prompted
4. Token is validated
5. App starts!
6. When you exit, token is cleared from memory

**Security:**

- ✅ Token NEVER saved to disk
- ✅ Token ONLY in memory while running
- ✅ Token cleared on exit
- ✅ Token validated on startup

#### Steps

1. **Download `Blink.exe`** from Releases page

2. **Run the executable**

   - Windows: Double-click `Blink.exe`
   - A terminal window will open

3. **Enter API Token**

   ```
   [BLINK] API Token Configuration

   Enter your REPLICATE_API_TOKEN: [your_token_here]
   ```

4. **Token Validation**

   ```
   [VALIDATING] Checking token with Replicate API...
   [OK] Token validated successfully!
   ```

5. **Start Using Blink**
   ```
   blink> help::
   ```

#### Repeat Each Session

Every time you run `Blink.exe`, you'll need to enter your API token. This keeps your token secure!

---

### Option 2: Raw Version (Python Development)

macOS/Linux:

```bash
source venv/Scripts/activate
```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure API token**

   **EASIEST WAY** - Use the setup script:

   ```bash
   python setup.py
   ```

   This interactive script will guide you through token setup.

   **OR manually** - Edit `.env` file:

   ```env
   REPLICATE_API_TOKEN=your_actual_token_here
   MODEL=anthropic/claude-4.5-sonnet
   ```

   Get your free token from: https://replicate.com/signin

6. **Run Blink**
   ```bash
   python main.py
   ```

---

### Option 2: App Version (EXE Executable - Build It Yourself)

**Why build it yourself?**

- Never expose your API token ✅
- Your token stays on your computer ✅
- Full control over the executable ✅

#### Requirements

- Python 3.8+ (for building only)
- A few minutes to build
- Your own Replicate API token

#### Steps to Build EXE

1. **Clone the project**

   ```bash
   git clone https://github.com/yourusername/blink.git
   cd blink
   ```

2. **Set up Python environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

3. **Configure API token**

   ```bash
   python setup.py
   ```

   This will create your `.env` file with your token.

4. **Build the executable**

   ```bash
   python build_exe.py
   ```

5. **Find your executable**
   - Located at: `dist/Blink.exe`
   - File size: ~40-50 MB (includes Python runtime)
   - Ready to use!

#### Using Your Built EXE

1. **Copy the EXE** to wherever you want (Desktop, Documents, etc.)
2. **Copy the `.env` file** to the same folder as `Blink.exe`
3. **Double-click `Blink.exe`** to launch

⚠️ **Important:** Keep your `.env` file secure and don't share it!

#### Why This Approach?

- **Security:** Your API token never leaves your computer
- **Privacy:** Only you have access to the built EXE
- **Simplicity:** No pre-built binaries with exposed tokens
- **Trust:** You can inspect the source code before building

#### Quick Build with Batch Script (Windows)

If you prefer a one-click build:

```bash
build_exe.bat
```

Your EXE will be ready in `dist/Blink.exe`

---

## Command Reference

Once Blink is running, use these commands:

```bash
# Read a file from workspace or external path
read:: <file>
read:: "C:\path\to\external\file.ts"

# Create a new empty file
create:: <file>

# List directory contents
list:: [directory]

# Generate code with AI (main power command)
generate:: <instruction>

# View conversation history
history::

# Clear session and history
clear::

# Show all commands
help::

# Save session and exit
exit::
```

### Examples

```bash
blink> read:: src/main.ts

blink> read:: "C:\projects\myproject\file.ts"

blink> create:: new-service.ts

blink> list:: src/

blink> generate:: Add error handling to this function

blink> history::

blink> exit::
```

---

## Configuration

### Blink Workspace

Blink creates and uses a `workspace/` folder for:

- Project files
- Generated code
- Session history
- Conversation logs

### Environment Variables (.env)

```env
# Required: Your Replicate API token
REPLICATE_API_TOKEN=your_token_here

# Optional: Custom workspace location
WORKSPACE_ROOT=./workspace

# Optional: Debug mode
DEBUG=false
```

Get your API token from: https://replicate.com

---

## Troubleshooting

### "REPLICATE_API_TOKEN is not set"

**Solution:** Create `.env` file in the same directory as Blink with:

```env
REPLICATE_API_TOKEN=your_actual_token_here
```

### EXE won't launch

**Solutions:**

1. Check that `.env` file exists with valid API token
2. Ensure internet connection is active
3. Try running from Command Prompt to see error messages
4. Reinstall from the releases page

### API errors or rate limiting

**Solutions:**

1. Wait a few moments before retrying
2. Check your API token is correct
3. Visit https://replicate.com for quota info
4. Use free tier (has generous limits)

### File not found errors

**Solution:** When reading files:

- Use relative paths for workspace files: `read:: src/file.ts`
- Use absolute paths for external files: `read:: "C:\full\path\file.ts"`
- Wrap paths with quotes if they contain spaces

---

## Version Comparison

| Feature                 | Raw Python      | Built EXE       |
| ----------------------- | --------------- | --------------- |
| **Python Installation** | Required        | Not needed\*    |
| **Setup Time**          | ~3 min          | ~5 min (build)  |
| **Customization**       | Full access     | Limited         |
| **Performance**         | Slightly faster | Slightly slower |
| **File Size**           | ~2 MB (repo)    | ~50 MB (exe)    |
| **Portability**         | Requires Python | Fully portable  |
| **Security**            | Full control    | Full control    |
| **Token Exposure**      | Never           | Never           |

\*Note: Python required to BUILD the EXE, but not to RUN it

---

## Advanced: Building & Distributing

### Create Installer (Optional)

For even easier distribution, you can create a Windows installer:

```bash
pip install pyinstaller inno-setup
python build_exe.py
# Then use Inno Setup to create an installer
```

### GitHub Releases

1. Build the EXE: `python build_exe.py`
2. Compress: `dist/Blink.exe` → `Blink-v1.0.0.zip`
3. Go to GitHub Releases
4. Create new release
5. Upload the zip file

---

## Support & Issues

### Getting Help

1. Check the [README.md](README.md)
2. Run `help::` inside Blink
3. Check for error messages
4. Open an issue on GitHub

### Reporting Issues

When reporting issues, include:

- Which version you're using (raw, exe, etc.)
- Your OS and Python version (if applicable)
- The command you ran
- The error message
- Your `.env` file (without the actual API token!)

---

## Next Steps

- Read the [README.md](README.md) for features and examples
- Check [QUICKSTART.md](QUICKSTART.md) for quick tutorials
- Explore project structure in `src/`

Happy coding with Blink! 🚀
