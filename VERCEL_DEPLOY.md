# Deploy VELLORE AI to Vercel

## ⚠️ Important Note
Vercel has a **10-second timeout** for serverless functions on free tier. For production, consider **Render.com** or **Railway.app** instead.

## Quick Deploy Steps

### 1. Push to GitHub
```bash
cd e:\genaiopen
git init
git add .
git commit -m "Initial commit - VELLORE AI"
git remote add origin https://github.com/ramandeveloper24x7-pixel/pythonai.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Vercel

**Option A: Vercel Dashboard**
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click **"New Project"**
4. Import `pythonai` repository
5. Click **"Deploy"**

**Option B: Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### 3. Configure Environment Variables (Optional)
In Vercel Dashboard → Settings → Environment Variables:
```
GROQ_API_KEY=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
SECRET_KEY=vellore-ai-secret-key-2024
```

## Files Included

✅ `vercel.json` - Vercel configuration
✅ `.gitignore` - Ignore unnecessary files
✅ `README.md` - Project documentation
✅ `app_lite.py` - Main application
✅ `requirements_lite.txt` - Dependencies
✅ `static/` - Frontend files

## Access Your App

After deployment:
```
https://pythonai.vercel.app
```

## Limitations on Vercel

❌ 10-second timeout (may cause issues with long AI responses)
❌ SQLite database resets on each deployment
❌ Limited for stateful applications

## Better Alternatives

### 🏆 Render.com (RECOMMENDED)
```bash
# No timeout limits
# Persistent database
# Free tier: 512MB RAM
```

### Railway.app
```bash
# $5/month credit
# Better for FastAPI
# Persistent storage
```

## Troubleshooting

### Timeout Errors
- Reduce `max_tokens` in app_lite.py
- Use streaming responses
- Consider Render.com instead

### Database Issues
- Vercel resets SQLite on deploy
- Use PostgreSQL or external DB
- Or deploy to Render.com

### Static Files Not Loading
- Ensure `static/` folder is in root
- Check `vercel.json` routes

## Git Commands Reference

```bash
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy on Vercel
3. ✅ Test the application
4. 🔄 If timeout issues → Deploy to Render.com

---

**Recommendation**: Use **Render.com** for production deployment. Vercel is better suited for frontend/Next.js apps.
