# VELLORE AI - PythonAnywhere Deployment Guide

## Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free account (Beginner account is sufficient)

## Step 2: Upload Files
1. Go to "Files" tab
2. Create a new directory: `/home/yourusername/vellore-ai`
3. Upload these files:
   - app.py
   - requirements_web.txt
   - static/ folder (with all HTML, CSS files)
   - documents/ folder

## Step 3: Install Dependencies
1. Go to "Consoles" tab
2. Start a new Bash console
3. Run these commands:

```bash
cd vellore-ai
pip3 install --user -r requirements_web.txt
```

## Step 4: Configure WSGI
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Click on WSGI configuration file link
6. Replace content with:

```python
import sys
path = '/home/yourusername/vellore-ai'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

## Step 5: Set Static Files
1. In "Web" tab, scroll to "Static files" section
2. Add:
   - URL: `/static/`
   - Directory: `/home/yourusername/vellore-ai/static`

## Step 6: Reload & Test
1. Click "Reload" button at top of Web tab
2. Visit: `yourusername.pythonanywhere.com`

## Important Notes:
- Free tier has limited CPU time
- Database file will be created automatically
- Update Groq API key in app.py if needed
- Check error logs in "Web" tab if issues occur

## Troubleshooting:
- If 502 error: Check WSGI file path
- If static files not loading: Verify static files mapping
- If dependencies fail: Use `pip3 install --user` for each package
