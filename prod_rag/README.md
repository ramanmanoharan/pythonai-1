# Production RAG Chatbot

This folder contains a production-ready Retrieval-Augmented Generation (RAG) service using LangChain, FAISS, and Hugging Face models.

Requirements
- A Hugging Face Hub token: set `HUGGINGFACEHUB_API_TOKEN`
- A model repo id: set `HUGGINGFACE_MODEL` (default `google/flan-t5-large`)
- Documents to index in `documents/`

Quick start

1. Install deps:

```bash
pip install -r requirements.txt
```

2. Ingest documents (creates `vectorstore/`):

```bash
# optional: set models/tokens
export HUGGINGFACEHUB_API_TOKEN="<your-token>"
python prod_rag/ingest.py
```

3. Run the API:

```bash
export HUGGINGFACEHUB_API_TOKEN="<your-token>"
uvicorn prod_rag.app:app --host 0.0.0.0 --port 8000
```

4. Call the chat endpoint:

POST /chat
Body JSON: {"question": "Your question", "chat_history": []}

Notes
- This implementation uses `SentenceTransformerEmbeddings` for embeddings and `FAISS` for the vector index.
- Provide an appropriate `HUGGINGFACE_MODEL` compatible with text-generation (e.g., an instruction-tuned model).
- For production consider: batching ingestion, async workers, concurrency tuning, authentication, and monitoring.