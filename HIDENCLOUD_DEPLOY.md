# Deploy VELLORE AI to HidenCloud

## Files to Upload

### 1. Main Application
- `app_lite.py` → rename to `app.py`
- `requirements_lite.txt` → rename to `requirements.txt`

### 2. Static Files (upload entire folder)
- `static/index.html`
- `static/chat.html`
- `static/login.html`
- `static/style.css`
- `static/chat.css`
- `static/login.css`

## Deployment Steps

### Step 1: Create Python App
1. Login to HidenCloud dashboard
2. Go to **Python App** section
3. Click **Create New App**
4. Select **Python 3.10+**
5. Set app name: `vellore-ai`

### Step 2: Upload Files
Via File Manager or FTP:
```
/home/your-username/vellore-ai/
├── app.py (renamed from app_lite.py)
├── requirements.txt (renamed from requirements_lite.txt)
└── static/
    ├── index.html
    ├── chat.html
    ├── login.html
    ├── style.css
    ├── chat.css
    └── login.css
```

### Step 3: Install Dependencies
Open **Terminal/SSH** and run:
```bash
cd ~/vellore-ai
pip install -r requirements.txt
```

### Step 4: Configure App
Create `startup.sh`:
```bash
#!/bin/bash
cd /home/your-username/vellore-ai
uvicorn app:app --host 0.0.0.0 --port 8000
```

Make executable:
```bash
chmod +x startup.sh
```

### Step 5: Set Environment Variables (Optional)
In HidenCloud dashboard → Environment Variables:
```
GROQ_API_KEY=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
SECRET_KEY=vellore-ai-secret-key-2024
```

### Step 6: Start Application
In dashboard:
- Set **Start Command**: `./startup.sh`
- Or: `uvicorn app:app --host 0.0.0.0 --port 8000`
- Click **Start/Restart**

### Step 7: Configure Domain
- Default: `your-app.hidencloud.com`
- Custom domain: Add in DNS settings

## Testing
- Homepage: `https://your-app.hidencloud.com/`
- Chat: `https://your-app.hidencloud.com/chat.html`
- Login: `https://your-app.hidencloud.com/login.html`

## Troubleshooting

### Port Issues
If port 8000 is blocked, try:
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Static Files Not Loading
Check app.py has:
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Database Permissions
```bash
chmod 666 vellore_ai.db
```

### Logs
```bash
tail -f ~/vellore-ai/logs/app.log
```

## Quick Deploy Commands
```bash
# Upload files
scp -r app_lite.py requirements_lite.txt static/ user@hidencloud.com:~/vellore-ai/

# SSH into server
ssh user@hidencloud.com

# Setup
cd ~/vellore-ai
mv app_lite.py app.py
mv requirements_lite.txt requirements.txt
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Features Included
✅ Groq AI Chat (llama-3.3-70b)
✅ User Authentication (JWT)
✅ SQLite Database
✅ Chat History
✅ Modern UI with Dark/Light Theme
✅ Mobile Responsive

## Resource Usage
- Storage: ~50MB
- RAM: ~200MB
- CPU: Minimal

Perfect for HidenCloud free/starter plans! 🚀
