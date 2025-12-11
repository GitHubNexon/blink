# Blink - Developer & Distribution Guide

This guide is for developers who want to build, customize, and distribute Blink.

---

## Building the EXE

### Prerequisites

- Python 3.8 or higher
- All dependencies installed: `pip install -r requirements.txt`
- PyInstaller (auto-installed with requirements.txt)

### Quick Build

**Windows (Recommended):**

```bash
build_exe.bat
```

**All Platforms (Python):**

```bash
python build_exe.py
```

### What Gets Built?

```
dist/
└── Blink.exe  (~40-50 MB, includes Python runtime)
```

The executable includes:

- ✅ Python 3.X runtime
- ✅ All dependencies (requests, pathvalidate, python-dotenv)
- ✅ All source code (src/ folder)
- ✅ MCP server and agent logic
- ✅ CLI interface

### Build Options

Edit `build_exe.py` or `build_exe.bat` to customize:

```python
# Add icon (create blink.ico first)
--icon=blink.ico

# Add console window
--console  # Remove --windowed

# Create installer instead
# (Use Inno Setup or NSIS)
```

---

## Distribution Formats

### 1. Single Executable

**Best for:** Most users

```
Release Package:
├── Blink.exe
└── .env.example
```

**Distribution:**

1. Build: `python build_exe.py`
2. Copy `dist/Blink.exe` to release folder
3. Create sample `.env.example`:
   ```env
   REPLICATE_API_TOKEN=your_token_here
   ```
4. Upload to GitHub Releases

**User Instructions:**

```
1. Download Blink.exe
2. Create .env file next to Blink.exe
3. Add: REPLICATE_API_TOKEN=your_token
4. Run Blink.exe
```

### 2. ZIP Package

**Best for:** Distributing with documentation

```
Release Package:
├── Blink.exe
├── .env.example
├── README.md
├── INSTALLATION.md
└── QUICKSTART.md
```

**Distribution:**

```bash
# Create the zip
7z a Blink-v1.0.0.zip dist/Blink.exe .env.example README.md INSTALLATION.md

# Or on Windows
# Right-click → Send to → Compressed (zipped) folder
```

### 3. Portable Package

**Best for:** USB drives, no installation needed

```
Release Package:
├── Blink.exe
├── workspace/        (pre-created empty folder)
├── .env
└── README.txt
```

---

## GitHub Release Process

### 1. Prepare Release

```bash
# Make sure everything is committed
git status

# Tag the version
git tag v1.0.0

# Push to GitHub
git push origin main
git push origin v1.0.0
```

### 2. Build Executable

```bash
python build_exe.py
```

### 3. Create GitHub Release

1. Go to: https://github.com/yourusername/blink/releases
2. Click "Draft a new release"
3. Set tag: `v1.0.0`
4. Title: `Blink v1.0.0 - Your Vibe Coder Agent Buddy`
5. Description:

   ```markdown
   # Blink v1.0.0

   ## What's New

   - Feature 1
   - Feature 2
   - Bug fixes

   ## Download

   ### For Most Users (EXE)

   - **[Blink.exe](...)** - Standalone executable, no Python needed
   - Just download, set up `.env` with API token, run!

   ### For Developers (Source)

   - Clone: `git clone https://github.com/yourusername/blink.git`
   - Follow setup in README.md

   ## Setup

   1. Download `Blink.exe`
   2. Create `.env` file next to it:
   ```

   REPLICATE_API_TOKEN=your_api_token_here

   ```
   3. Run `Blink.exe`

   See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

   ## Requirements
   - Windows 10 or higher
   - Internet connection
   - Replicate API token (free at replicate.com)
   ```

6. Upload files:

   - Drag & drop `dist/Blink.exe`
   - Optionally add `.env.example` and `README.md`

7. Click "Publish release"

---

## Advanced Distribution

### Create Windows Installer

Using Inno Setup (free):

1. **Install Inno Setup** from `https://jrsoftware.org/isdl.php`

2. **Create `blink-installer.iss`:**

   ```ini
   [Setup]
   AppName=Blink
   AppVersion=1.0.0
   DefaultDirName={pf}\Blink
   DefaultGroupName=Blink
   OutputDir=.\installer
   OutputBaseFilename=BlinkInstaller-1.0.0

   [Files]
   Source: "dist\Blink.exe"; DestDir: "{app}"
   Source: ".env.example"; DestDir: "{app}"; DestName: ".env"
   Source: "README.md"; DestDir: "{app}"

   [Icons]
   Name: "{group}\Blink"; Filename: "{app}\Blink.exe"
   ```

3. **Build installer:**

   ```bash
   iscc blink-installer.iss
   ```

4. **Distribute:**
   - Upload `installer/BlinkInstaller-1.0.0.exe` to GitHub Releases

### Create Portable Version

Just the EXE with no installation:

```bash
# Copy files
mkdir Blink-Portable
copy dist\Blink.exe Blink-Portable\
copy .env.example Blink-Portable\
copy README.md Blink-Portable\

# Create zip
7z a Blink-Portable-1.0.0.zip Blink-Portable\

# Upload to GitHub Releases
```

---

## Customization

### Change App Name

Edit `build_exe.py` or `build_exe.bat`:

```python
--name MyAppName
```

### Add Custom Icon

1. Create or find an icon: `blink.ico` (256x256 pixels)
2. Place in project root
3. Build script will auto-detect and use it

### Exclude Files

Edit `build_exe.py`:

```python
--exclude-module=test
--exclude-module=pytest
```

### Add Files to Distribution

```python
--add-data "workspace;workspace"
--add-data "examples;examples"
```

---

## Troubleshooting Build Issues

### "PyInstaller not found"

```bash
pip install pyinstaller>=6.0.0
```

### "Module not found" errors

Add to `build_exe.py`:

```python
--hidden-import=module_name
--collect-all=module_name
```

### EXE is too large (>100 MB)

Try building with UPX compression:

```bash
pip install upx
build_exe.py --upx-dir=path/to/upx
```

### EXE won't start

1. Check Windows Defender/antivirus (may be blocking)
2. Run from Command Prompt to see error
3. Ensure `.env` file exists
4. Check Python runtime compatibility

---

## Version Management

### Semantic Versioning

Use format: `MAJOR.MINOR.PATCH`

- `1.0.0` - Initial release
- `1.1.0` - New features
- `1.1.1` - Bug fixes

### Release Checklist

- [ ] Update `__version__` in code
- [ ] Update `CHANGELOG.md`
- [ ] Test all 3 versions (exe, raw python, source)
- [ ] Build executable
- [ ] Tag commit: `git tag v1.X.X`
- [ ] Push to GitHub
- [ ] Create release with assets
- [ ] Update website/documentation

---

## Monitoring & Updates

### Track Downloads

GitHub automatically shows release download statistics.

### Plan Updates

Keep users informed:

- Update README with new features
- Create release notes
- Pin latest release on GitHub

---

## Support

For distribution questions:

1. Check [INSTALLATION.md](INSTALLATION.md)
2. Review this guide
3. Open GitHub issue
4. Check PyInstaller docs: https://pyinstaller.org

---

Happy distributing! 🚀
