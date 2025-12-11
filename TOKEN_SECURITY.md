# Blink - Token Handling Guide

## How Token Security Works

When you run Blink (either EXE or Python), here's exactly what happens with your API token:

```
┌─────────────────────────────────────────────────────────┐
│  1. APP STARTS                                          │
│     Blink loads (no token yet)                          │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  2. PROMPT FOR TOKEN                                    │
│     "Enter your REPLICATE_API_TOKEN:"                   │
│     [Your Token Here]                                   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  3. VALIDATE TOKEN                                      │
│     Makes test API call to Replicate                    │
│     [VALIDATING] Checking token...                      │
│     [OK] Token validated!                               │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  4. APP RUNS                                            │
│     Token stored in memory (RAM)                        │
│     Used for API calls to Replicate                     │
│     blink> [Ready for your commands]                    │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  5. EXIT                                                │
│     blink> exit::                                       │
│     [INFO] API token cleared from memory.               │
│     App closes                                          │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  6. TOKEN GONE                                          │
│     Token is COMPLETELY cleared                         │
│     Next app start requires entering token again        │
└─────────────────────────────────────────────────────────┘
```

## Why This Approach?

### 🔒 Security Benefits

1. **No Token Storage** - Token never touches disk
2. **Validated Every Time** - Bad tokens caught immediately
3. **Auto-Cleared** - Token gone when you exit
4. **Memory-Only** - RAM gets wiped when process ends
5. **Safe to Share** - Can distribute EXE without token exposure

### 👤 User Benefits

1. **Simple** - Just run app, enter token
2. **Safe** - No worrying about token storage
3. **Explicit** - You see it being validated
4. **No Secrets in Code** - Token never in source code
5. **Fresh Start** - Each session starts clean

## Common Questions

### Q: Where is my token stored?

**A:** Only in RAM (memory) while the app is running. When the app exits, the memory is cleared. Your token never touches the disk.

### Q: What if I close the app without exiting properly?

**A:** That's fine! The token will be cleared from memory anyway. Next time you run the app, you'll enter a new token.

### Q: Can I use the same token multiple times?

**A:** Yes! Your Replicate token never expires. You can use the same token every time you run Blink.

### Q: What if I want to save my token?

**A:** You can create a `.env` file in the same folder as `Blink.exe`:

```env
REPLICATE_API_TOKEN=your_token_here
```

If the app finds this file, it will use the token automatically and skip the prompt. But it's optional - the app works fine without it.

### Q: Can I run multiple instances of Blink?

**A:** Yes! Each instance will prompt for its token independently. Tokens are kept separate in each instance's memory.

### Q: Is my token safe with this approach?

**A:** Yes! It's actually safer than many alternatives because:

- It never touches disk
- It's validated immediately
- It's cleared automatically
- The source code never has a hardcoded token

## For Developers

If you're building from source:

### Using Token Manager

```python
from src.token_manager import get_api_token, clear_api_token

# Get token (prompts if not available)
token = get_api_token()

# Later, clear token from memory
clear_api_token()
```

### Environment Variable Alternative

If you want to skip the prompt (for development):

```bash
# Windows
set REPLICATE_API_TOKEN=your_token
python main.py

# macOS/Linux
export REPLICATE_API_TOKEN=your_token
python main.py
```

Or create a `.env` file:

```env
REPLICATE_API_TOKEN=your_token
MODEL=anthropic/claude-4.5-sonnet
```

## Distribution

When you release Blink EXE:

1. Build it with `python build_exe.py`
2. Release just the `Blink.exe` file (NO TOKEN EMBEDDED!)
3. Users download and run `Blink.exe`
4. They enter their own token
5. Everyone is secure! ✅

No tokens in releases, no security risks, no exposure!

---

**Summary:** This approach gives you the best of both worlds - ease of use AND security. Users don't need to know about tokens, and their tokens stay private and secure.
