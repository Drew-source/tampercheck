# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API account and API key

## Step-by-Step Installation

### 1. Navigate to Project Directory

```bash
cd tampercheck
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `colorama` - Cross-platform colored terminal output

### 3. Get OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

### 4. Configure Environment Variables

Create a `.env` file in the `tampercheck` directory:

**Option A: Copy from example**
```bash
cp .env.example .env
```

**Option B: Create manually**
```bash
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
```

**Option C: Use a text editor**
Create a file named `.env` with this content:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

⚠️ **Important**: Replace `sk-your-actual-key-here` with your real API key!

### 5. Verify Installation

Run the test script:

```bash
python tampercheck.py
```

If everything is set up correctly, you should see:
- Colored ASCII art header
- Analysis progress messages
- Color-coded token analysis results

## Troubleshooting

### "No module named 'openai'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "API key not found"

**Solution**: Check your `.env` file
1. Make sure `.env` file exists in `tampercheck/` directory
2. Make sure it contains `OPENAI_API_KEY=sk-...`
3. Make sure there are no extra spaces or quotes

### "Invalid API key"

**Solution**: Verify your API key
1. Go to https://platform.openai.com/api-keys
2. Check if your key is active
3. Copy the key again and update `.env`

### "Rate limit exceeded"

**Solution**: You're making too many requests
1. Wait a few minutes
2. Check your OpenAI usage limits
3. Consider upgrading your OpenAI plan

### "Module 'colorama' not found"

**Solution**: Install colorama
```bash
pip install colorama
```

### Windows Color Issues

If colors don't display correctly on Windows:

**Solution**: Colorama should handle this automatically, but if not:
1. Use Windows Terminal instead of cmd.exe
2. Or run: `pip install --upgrade colorama`

## Optional: Virtual Environment

For a cleaner installation, use a virtual environment:

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Verifying Your Setup

Run this quick test:

```bash
python -c "from tampercheck import TamperDetector; print('✓ Installation successful!')"
```

If you see `✓ Installation successful!`, you're ready to go!

## Next Steps

1. **Quick Start**: Read `QUICKSTART.md`
2. **Run Examples**: `python example_usage.py`
3. **Read Theory**: Check out `THEORY.md`
4. **Full Docs**: See `README.md`

## Uninstallation

To remove TamperCheck:

```bash
# Remove dependencies (if not used by other projects)
pip uninstall openai python-dotenv colorama

# Delete the directory
cd ..
rm -rf tampercheck
```

## Getting Help

If you encounter issues not covered here:

1. Check that Python 3.8+ is installed: `python --version`
2. Check that pip is working: `pip --version`
3. Verify your OpenAI API key is valid
4. Make sure you have internet connectivity
5. Check OpenAI's status page: https://status.openai.com/

## Security Notes

⚠️ **Never commit your `.env` file to git!**

The `.gitignore` file is already configured to exclude `.env`, but be careful:
- Don't share your API key
- Don't commit it to version control
- Don't post it in public forums
- Rotate your key if it's exposed

## Cost Considerations

Each analysis makes an API call to OpenAI:
- **GPT-3.5-turbo**: ~$0.001 per analysis (very cheap)
- **GPT-4**: ~$0.03 per analysis (more expensive)

Start with GPT-3.5-turbo for testing!

---

**Installation complete! Ready to detect tampering. 🔍**

