import os
from typing import List, Tuple

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

ROOT = os.path.dirname(os.path.dirname(__file__))
VSTORE_DIR = os.getenv("VECTORSTORE_PATH", os.path.join(ROOT, "vectorstore"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
HF_MODEL = os.getenv("HUGGINGFACE_MODEL", "google/flan-t5-large")


class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]] = []


app = FastAPI(title="Production RAG Chatbot")


def load_vectorstore():
    if not os.path.exists(VSTORE_DIR):
        raise RuntimeError(f"Vectorstore not found at {VSTORE_DIR}; run ingest first")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = FAISS.load_local(VSTORE_DIR, embeddings)
    return vectordb


def get_llm():
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise RuntimeError("Missing HUGGINGFACEHUB_API_TOKEN environment variable")
    llm = HuggingFaceHub(repo_id=HF_MODEL, huggingfacehub_api_token=token, model_kwargs={"temperature": 0.0, "max_new_tokens": 512})
    return llm


@app.on_event("startup")
def startup():
    global VECTORDB, CHAIN
    VECTORDB = load_vectorstore()
    llm = get_llm()
    retriever = VECTORDB.as_retriever(search_kwargs={"k": 4})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    CHAIN = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory, return_source_documents=True)


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = CHAIN({"question": req.question, "chat_history": req.chat_history})
        answer = result.get("answer")
        docs = result.get("source_documents", [])
        sources = [ {"page_content": d.page_content, "metadata": getattr(d, "metadata", {})} for d in docs ]
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
