import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from huggingface_hub import InferenceClient

class SimpleRAGChatbot:
    def __init__(self, docs_path: str, hf_token: str):
        self.hf_token = hf_token
        self.docs_path = docs_path
        self.embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.client = InferenceClient(token=hf_token)
        self.documents = []
        self.index = None
        self.chat_history = []
        
    def load_documents(self):
        for filename in os.listdir(self.docs_path):
            if filename.endswith('.txt'):
                with open(os.path.join(self.docs_path, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    chunks = [content[i:i+1000] for i in range(0, len(content), 800)]
                    self.documents.extend(chunks)
        
        embeddings = self.embeddings_model.encode(self.documents)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))
        return len(self.documents)
    
    def retrieve(self, query: str, k: int = 3):
        query_embedding = self.embeddings_model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        return [self.documents[i] for i in indices[0]]
    
    def chat(self, question: str):
        relevant_docs = self.retrieve(question)
        context = "\n\n".join(relevant_docs)
        
        history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in self.chat_history[-3:]])
        
        prompt = f"""Use the following context to answer the question. If you don't know, say so.

Context: {context}

Chat History:
{history_text}

Question: {question}

Answer:"""
        
        response = self.client.text_generation(
            prompt,
            model="mistralai/Mistral-7B-Instruct-v0.3",
            max_new_tokens=512,
            temperature=0.7,
            base_url="https://api-inference.huggingface.co"
        )
        
        self.chat_history.append({"user": question, "bot": response})
        return response
    
    def reset_memory(self):
        self.chat_history = []

def main():
    HF_TOKEN = "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"
    DOCS_PATH = "./documents"
    
    print("Initializing chatbot...")
    chatbot = SimpleRAGChatbot(docs_path=DOCS_PATH, hf_token=HF_TOKEN)
    
    print("Loading documents...")
    num_chunks = chatbot.load_documents()
    print(f"Loaded {num_chunks} document chunks\n")
    print("Chatbot ready!\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            chatbot.reset_memory()
            print("Memory cleared!\n")
            continue
        
        print("\nBot: ", end="")
        answer = chatbot.chat(user_input)
        print(f"{answer}\n")

if __name__ == "__main__":
    main()
