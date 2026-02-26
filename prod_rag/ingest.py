import os
from pathlib import Path

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

ROOT = Path(__file__).resolve().parents[1]
DOCS_PATH = Path(os.getenv("DOCS_PATH", ROOT / "documents"))
VSTORE_DIR = Path(os.getenv("VECTORSTORE_PATH", ROOT / "vectorstore"))
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


def load_documents(directory: Path):
    docs = []
    for p in sorted(directory.rglob("*.txt")):
        loader = TextLoader(str(p), encoding="utf8")
        docs.extend(loader.load())
    return docs


def build_vectorstore():
    if not DOCS_PATH.exists():
        raise RuntimeError(f"Documents folder not found at {DOCS_PATH}")
    print("Loading documents...")
    documents = load_documents(DOCS_PATH)
    print(f"Loaded {len(documents)} documents")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBED_MODEL)
    print("Building FAISS index (this may take a while)...")
    index = FAISS.from_documents(docs, embeddings)
    VSTORE_DIR.mkdir(parents=True, exist_ok=True)
    index.save_local(str(VSTORE_DIR))
    print(f"Saved vectorstore to {VSTORE_DIR}")


if __name__ == "__main__":
    build_vectorstore()
