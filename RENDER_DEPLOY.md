# Deploy VELLORE AI to Render.com (FREE)

## Why Render?
✅ 512MB RAM (enough for app_lite.py)
✅ Auto-deploy from GitHub
✅ Free SSL certificate
✅ Easy setup (5 minutes)
✅ No credit card required

## Step 1: Prepare Files

### Create `render.yaml`
```yaml
services:
  - type: web
    name: vellore-ai
    env: python
    buildCommand: pip install -r requirements_lite.txt
    startCommand: uvicorn app_lite:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

### Update `requirements_lite.txt`
```
fastapi==0.115.0
uvicorn[standard]==0.32.1
groq==0.13.0
sqlalchemy==2.0.25
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.10.3
python-multipart==0.0.20
```

## Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/vellore-ai.git
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: vellore-ai
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements_lite.txt`
   - **Start Command**: `uvicorn app_lite:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. Click **"Create Web Service"**

## Step 4: Access Your App

Your app will be live at:
```
https://vellore-ai.onrender.com
```

## Important Notes

- **Cold Start**: Free tier sleeps after 15 min inactivity (first request takes 30s)
- **Rename Files**: 
  - `app_lite.py` → `app.py` OR
  - Update start command to: `uvicorn app_lite:app --host 0.0.0.0 --port $PORT`
- **Database**: SQLite persists on Render free tier
- **Logs**: Available in Render dashboard

## Alternative: Railway.app

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select repository
5. Railway auto-detects Python and deploys
6. Get URL: `https://your-app.up.railway.app`

## Alternative: Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch

# Deploy
fly deploy
```

## Troubleshooting

### Port Issues
Render uses `$PORT` environment variable. Ensure:
```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Static Files
Ensure `static/` folder is in repository root.

### Database
SQLite works on Render. For production, use PostgreSQL (free tier available).

## Cost Comparison

| Platform | Free Tier | Storage | RAM | Sleep |
|----------|-----------|---------|-----|-------|
| Render | ✅ Forever | 512MB | 512MB | 15min |
| Railway | $5/month credit | 1GB | 512MB | No |
| Fly.io | 3 VMs | 3GB | 256MB | No |
| Vercel | ✅ Forever | 512MB | 1GB | No |

## Recommendation

**Use Render.com** - Best balance of features and ease of use for your FastAPI app.
