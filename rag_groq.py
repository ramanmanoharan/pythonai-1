import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from groq import Groq

class RAGChatbot:
    def __init__(self, docs_path: str, groq_api_key: str):
        self.groq_client = Groq(api_key=groq_api_key)
        self.docs_path = docs_path
        self.embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
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
        
        messages = [{"role": "system", "content": "You are a helpful assistant. Use the provided context to answer questions."}]
        
        for h in self.chat_history[-3:]:
            messages.append({"role": "user", "content": h['user']})
            messages.append({"role": "assistant", "content": h['bot']})
        
        messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"})
        
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )
        
        answer = response.choices[0].message.content
        self.chat_history.append({"user": question, "bot": answer})
        return answer
    
    def reset_memory(self):
        self.chat_history = []

def main():
    GROQ_API_KEY = "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"  # Get free key from https://console.groq.com
    DOCS_PATH = "./documents"
    
    print("Initializing chatbot...")
    chatbot = RAGChatbot(docs_path=DOCS_PATH, groq_api_key=GROQ_API_KEY)
    
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
