# PythonAnywhere Deployment - Lightweight Version

## Problem Solved
The original app.py with sentence-transformers and PyTorch requires 915MB+ storage, exceeding PythonAnywhere's free tier 512MB limit.

This lightweight version removes:
- ❌ sentence-transformers (PyTorch dependency)
- ❌ FAISS vector store
- ❌ RAG document retrieval

Keeps all other features:
- ✅ Groq AI chat (llama-3.3-70b)
- ✅ JWT authentication
- ✅ SQLite database
- ✅ Chat history
- ✅ All UI pages

## Deployment Steps

### 1. Upload Files
Upload to `/home/velloreai/vellore-ai/`:
- `app_lite.py` (rename to `app.py` on server)
- `requirements_lite.txt` (rename to `requirements.txt`)
- `wsgi.py`
- `static/` folder (all HTML/CSS/JS files)

### 2. Install Dependencies
```bash
cd /home/velloreai/vellore-ai
pip3 install --user -r requirements.txt
```

Total size: ~50MB (fits free tier!)

### 3. WSGI Configuration
Already configured in `wsgi.py`:
```python
import sys
sys.path.insert(0, '/home/velloreai/vellore-ai')
from app import app as application
```

### 4. Web App Settings
- Source code: `/home/velloreai/vellore-ai`
- Working directory: `/home/velloreai/vellore-ai`
- WSGI file: `/var/www/velloreai_pythonanywhere_com_wsgi.py`
- Static files: URL `/static/` → Directory `/home/velloreai/vellore-ai/static`

### 5. Reload Web App
Click "Reload" button in PythonAnywhere dashboard

## Testing
- Homepage: `https://velloreai.pythonanywhere.com/`
- Chat: `https://velloreai.pythonanywhere.com/chat.html`
- Login: `https://velloreai.pythonanywhere.com/login.html`

## What Changed
**Before (app.py):**
- RAG with document retrieval
- sentence-transformers embeddings
- FAISS vector search
- 915MB+ dependencies

**After (app_lite.py):**
- Direct Groq AI chat
- No document retrieval
- No embeddings
- ~50MB dependencies

## Future Upgrades
To add RAG back, upgrade to PythonAnywhere paid plan ($5/month) with 1GB+ storage.
