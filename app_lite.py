from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

app = FastAPI()

# Groq API
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

# JWT Config
SECRET_KEY = "vellore-ai-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database
DATABASE_URL = "sqlite:///./vellore_ai.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Models
class ChatRequest(BaseModel):
    message: str
    username: str = None

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# VelloreAI Class (Lite - No RAG)
class VelloreAI:
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = """You are VELLORE AI, an intelligent coding assistant developed by Raman Manoharan.

ABOUT THE DEVELOPER:
VELLORE AI was created by Raman Manoharan, a highly skilled Senior Full Stack Developer with over 9 years of experience in the IT industry. He specializes in Python-based REST API development and modern web technologies. Raman currently works as a Full Stack Software Developer at eNoah I Solution, contributing to web and mobile application development using Angular (2+), Python, and CSS3.

Raman has strong expertise in:
- Frontend: Angular 2+/6+, ReactJS, HTML, CSS, JavaScript, jQuery, Bootstrap
- Backend: Python, Node.js (Express), PHP, Django, Laravel, CodeIgniter
- Databases: MySQL, MongoDB
- Full-cycle application development and REST APIs

Education:
- Bachelor of Engineering in Electrical and Electronics Engineering (EEE) from Anna University (2016)
- Diploma in EEE from R.I.T, Vellore (2013)

Raman is known for his strong problem-solving skills, clean coding practices, and passion for delivering high-quality, scalable, and reliable software solutions. He is passionate about democratizing AI and making advanced technology accessible to everyone.

Portfolio: https://ramanfullstackdeveloper.rf.gd/?i=1
LinkedIn: https://www.linkedin.com/in/raman-manoharan-2b4142126

YOUR CAPABILITIES:
- Code writing and debugging
- Technical explanations
- Best practices and optimization
- General programming questions

When asked about who developed you or who created VELLORE AI, always mention Raman Manoharan with his background and expertise. Be concise, accurate, and helpful."""

    def chat(self, user_message: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_message})
        
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history[-10:]
        
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        except Exception as e:
            return f"Error: {str(e)}"

    def reset(self):
        self.conversation_history = []

# Global AI instance
ai_instances = {}

def get_ai_instance(username: str = "guest"):
    if username not in ai_instances:
        ai_instances[username] = VelloreAI()
    return ai_instances[username]

# Routes
@app.post("/signup")
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        username=request.username,
        email=request.email,
        hashed_password=get_password_hash(request.password)
    )
    db.add(user)
    db.commit()
    
    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer", "username": request.username}

@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer", "username": request.username}

@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    username = request.username or "guest"
    ai = get_ai_instance(username)
    
    response = ai.chat(request.message)
    
    if username != "guest":
        user = db.query(User).filter(User.username == username).first()
        if user:
            history = ChatHistory(
                user_id=user.id,
                message=request.message,
                response=response
            )
            db.add(history)
            db.commit()
    
    return {"response": response}

@app.post("/reset")
async def reset_chat(request: ChatRequest):
    username = request.username or "guest"
    ai = get_ai_instance(username)
    ai.reset()
    return {"message": "Conversation reset"}

@app.get("/history/{username}")
async def get_history(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    history = db.query(ChatHistory).filter(ChatHistory.user_id == user.id).order_by(ChatHistory.timestamp.desc()).limit(50).all()
    return [{"message": h.message, "response": h.response, "timestamp": h.timestamp} for h in history]

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/chat.html")
async def chat_page():
    return FileResponse("static/chat.html")

@app.get("/login.html")
async def login_page():
    return FileResponse("static/login.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
