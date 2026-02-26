from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from groq import Groq
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

SECRET_KEY = "vellore-ai-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

DATABASE_URL = "sqlite:///./vellore_ai.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(Text)
    is_user = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VELLORE AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    type: str = "text"
    mapUrl: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        return None

class VelloreAI:
    def __init__(self):
        self.groq_client = Groq(api_key="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")
        self.embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.documents = []
        self.index = None
        self.sessions = {}
        self.load_documents()
        
    def load_documents(self):
        docs_path = "./documents"
        if os.path.exists(docs_path):
            for filename in os.listdir(docs_path):
                if filename.endswith('.txt'):
                    with open(os.path.join(docs_path, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                        chunks = [content[i:i+1000] for i in range(0, len(content), 800)]
                        self.documents.extend(chunks)
            
            if self.documents:
                embeddings = self.embeddings_model.encode(self.documents)
                self.index = faiss.IndexFlatL2(embeddings.shape[1])
                self.index.add(np.array(embeddings).astype('float32'))
    
    def retrieve(self, query: str, k: int = 3):
        if not self.documents or self.index is None:
            return []
        query_embedding = self.embeddings_model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        return [self.documents[i] for i in indices[0]]
    
    def detect_intent(self, message: str):
        message_lower = message.lower()
        if any(word in message_lower for word in ['code', 'program', 'function', 'debug', 'error', 'python', 'javascript', 'java', 'c++', 'algorithm']):
            return 'coding'
        if any(word in message_lower for word in ['location', 'map', 'where is', 'directions', 'navigate', 'address', 'place', 'city', 'country']):
            return 'location'
        return 'general'
    
    def get_location_info(self, query: str):
        location = query.lower().replace('where is', '').replace('location of', '').replace('map of', '').strip()
        map_url = f"https://www.google.com/maps?q={location.replace(' ', '+')}&output=embed"
        return {'response': f"Here's the location information for {location}:", 'mapUrl': map_url, 'type': 'map'}
    
    def chat(self, message: str, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        intent = self.detect_intent(message)
        if intent == 'location':
            return self.get_location_info(message)
        
        relevant_docs = self.retrieve(message)
        context = "\n\n".join(relevant_docs) if relevant_docs else ""
        
        if intent == 'coding':
            system_prompt = """You are VELLORE AI, an expert coding assistant developed by Raman Manoharan.

ABOUT THE DEVELOPER:
VELLORE AI was created by Raman Manoharan, a highly skilled Senior Full Stack Developer with over 9 years of experience in the IT industry. He specializes in Python-based REST API development and modern web technologies. Raman currently works as a Full Stack Software Developer at eNoah I Solution.

Raman's expertise includes:
- Frontend: Angular 2+/6+, ReactJS, HTML, CSS, JavaScript, jQuery, Bootstrap
- Backend: Python, Node.js (Express), PHP, Django, Laravel, CodeIgniter
- Databases: MySQL, MongoDB
- Full-cycle application development and REST APIs

Education:
- Bachelor of Engineering in EEE from Anna University (2016)
- Diploma in EEE from R.I.T, Vellore (2013)

Raman is known for his strong problem-solving skills, clean coding practices, and passion for delivering high-quality, scalable software solutions.

Portfolio: https://ramanfullstackdeveloper.rf.gd/?i=1
LinkedIn: https://www.linkedin.com/in/raman-manoharan-2b4142126

Help with code, debugging, algorithms, and best practices. When asked about who developed VELLORE AI, always mention Raman Manoharan."""
        else:
            system_prompt = """You are VELLORE AI, a helpful and intelligent assistant developed by Raman Manoharan.

ABOUT THE DEVELOPER:
VELLORE AI was created by Raman Manoharan, a highly skilled Senior Full Stack Developer with over 9 years of experience in the IT industry. He specializes in Python-based REST API development and modern web technologies. Raman currently works as a Full Stack Software Developer at eNoah I Solution.

Raman's expertise includes:
- Frontend: Angular 2+/6+, ReactJS, HTML, CSS, JavaScript, jQuery, Bootstrap
- Backend: Python, Node.js (Express), PHP, Django, Laravel, CodeIgniter
- Databases: MySQL, MongoDB

Education:
- Bachelor of Engineering in EEE from Anna University (2016)
- Diploma in EEE from R.I.T, Vellore (2013)

Raman is passionate about democratizing AI and making advanced technology accessible to everyone.

Portfolio: https://ramanfullstackdeveloper.rf.gd/?i=1
LinkedIn: https://www.linkedin.com/in/raman-manoharan-2b4142126

Be friendly, accurate, and helpful. When asked about who developed VELLORE AI, always mention Raman Manoharan."""
        
        messages = [{"role": "system", "content": system_prompt}]
        for h in self.sessions[session_id][-4:]:
            messages.append({"role": "user", "content": h['user']})
            messages.append({"role": "assistant", "content": h['bot']})
        
        user_message = f"Context:\n{context}\n\nQuestion: {message}" if relevant_docs else message
        messages.append({"role": "user", "content": user_message})
        
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        answer = response.choices[0].message.content
        self.sessions[session_id].append({"user": message, "bot": answer})
        return {'response': answer, 'type': 'text'}

ai = VelloreAI()

@app.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = ai.chat(request.message, request.session_id)
        
        if current_user:
            user_msg = ChatMessage(user_id=current_user.id, message=request.message, is_user=True)
            bot_msg = ChatMessage(user_id=current_user.id, message=result['response'], is_user=False)
            db.add(user_msg)
            db.add(bot_msg)
            db.commit()
        
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).order_by(ChatMessage.created_at).limit(50).all()
    return {"messages": [{"message": msg.message, "is_user": msg.is_user} for msg in messages]}

@app.post("/reset/{session_id}")
async def reset_session(session_id: str):
    if session_id in ai.sessions:
        ai.sessions[session_id] = []
    return {"message": "Session reset"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "VELLORE AI"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting VELLORE AI Server...")
    print("📍 Access at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
