# VELLORE AI - Intelligent Coding Assistant

![VELLORE AI](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-teal)
![License](https://img.shields.io/badge/License-MIT-yellow)

An intelligent AI-powered coding assistant built with FastAPI, Groq AI, and modern web technologies.

## 🚀 Features

- 💬 **AI Chat Assistant** - Powered by Groq's Llama 3.3 70B model
- 🔐 **User Authentication** - JWT-based secure login system
- 💾 **Chat History** - Save and retrieve conversation history
- 🎨 **Modern UI** - Dark/Light theme with responsive design
- 📱 **Mobile Friendly** - Works seamlessly on all devices
- ⚡ **Fast & Lightweight** - Optimized for performance

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- Groq AI (Llama 3.3 70B)
- SQLAlchemy + SQLite
- JWT Authentication
- Python 3.10+

**Frontend:**
- HTML5, CSS3, JavaScript
- Font Awesome Icons
- Responsive Design

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/ramandeveloper24x7-pixel/pythonai.git
cd pythonai

# Install dependencies
pip install -r requirements_lite.txt

# Run application
python app_lite.py
```

Access at: `http://localhost:8000`

## 🌐 Deployment

### Vercel
```bash
vercel --prod
```

### Render.com
1. Connect GitHub repository
2. Select Python environment
3. Build: `pip install -r requirements_lite.txt`
4. Start: `uvicorn app_lite:app --host 0.0.0.0 --port $PORT`

### Railway.app
1. Connect GitHub repository
2. Auto-deploys on push

## 📁 Project Structure

```
pythonai/
├── app_lite.py           # Main FastAPI application
├── requirements_lite.txt # Python dependencies
├── static/              # Frontend files
│   ├── index.html       # Landing page
│   ├── chat.html        # Chat interface
│   ├── login.html       # Authentication page
│   ├── style.css        # Main styles
│   ├── chat.css         # Chat styles
│   └── login.css        # Login styles
├── vercel.json          # Vercel configuration
└── README.md            # Documentation
```

## 🔑 Environment Variables

Create `.env` file (optional):
```
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

## 👨‍💻 Developer

**Raman Manoharan**
- Senior Full Stack Developer
- 9+ years experience in IT
- Specializes in Python, Angular, Node.js

**Connect:**
- Portfolio: [ramanfullstackdeveloper.rf.gd](https://ramanfullstackdeveloper.rf.gd/?i=1)
- LinkedIn: [raman-manoharan](https://www.linkedin.com/in/raman-manoharan-2b4142126)

## 📄 License

MIT License - feel free to use for personal and commercial projects.

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## ⭐ Support

If you find this project helpful, please give it a star!

---

Built with ❤️ by Raman Manoharan
