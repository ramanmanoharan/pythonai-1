# RAG Chatbot Web Deployment

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements_web.txt
```

2. Run the server:
```bash
python app.py
```

3. Open browser: http://localhost:8000

## Deploy to PythonAnywhere

1. Sign up at https://www.pythonanywhere.com (free tier available)

2. Upload files:
   - app.py
   - requirements_web.txt
   - documents/ folder
   - static/ folder

3. In PythonAnywhere console:
```bash
pip install --user -r requirements_web.txt
```

4. Create Web App:
   - Go to Web tab
   - Add new web app
   - Choose Manual configuration
   - Python 3.10

5. Configure WSGI file:
```python
import sys
path = '/home/yourusername/yourproject'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

6. Reload web app

## Deploy to Render/Railway

1. Create account on Render.com or Railway.app

2. Connect GitHub repo or upload files

3. Set start command:
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

4. Deploy!

## Environment Variables

For production, use environment variables:
```python
GROQ_API_KEY=your_key_here
```
