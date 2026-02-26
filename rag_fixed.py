import os
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class RAGChatbot:
    def __init__(self, docs_path: str, hf_token: str):
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = None
        self.chain = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
        self.docs_path = docs_path
        
    def load_documents(self):
        loader = DirectoryLoader(self.docs_path, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        return len(splits)
    
    def setup_chain(self):
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            temperature=0.7,
            max_new_tokens=512,
            huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"]
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=True
        )
    
    def chat(self, question: str):
        response = self.chain({"question": question})
        return response["answer"], response["source_documents"]
    
    def reset_memory(self):
        self.memory.clear()

def main():
    HF_TOKEN = "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"
    DOCS_PATH = "./documents"
    
    chatbot = RAGChatbot(docs_path=DOCS_PATH, hf_token=HF_TOKEN)
    
    print("Loading documents...")
    num_chunks = chatbot.load_documents()
    print(f"Loaded {num_chunks} document chunks")
    
    print("Setting up RAG chain...")
    chatbot.setup_chain()
    print("Chatbot ready!\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            chatbot.reset_memory()
            print("Memory cleared!")
            continue
        
        answer, sources = chatbot.chat(user_input)
        print(f"\nBot: {answer}\n")

if __name__ == "__main__":
    main()
