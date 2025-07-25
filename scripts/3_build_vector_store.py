import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def build_vector_store():
    """
    Builds a FAISS vector store from the scraped gut health knowledge using HuggingFace embeddings.
    """
    print("Loading text data...")

    loader = TextLoader("data/gut_health_knowledge.txt", encoding='utf-8')
    documents = loader.load()
    
    print(f"Loaded {len(documents)} document(s)")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks")

    print("Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"  
    )

    print("Building FAISS vector store...")
    vectorstore = FAISS.from_documents(texts, embeddings)

    vectorstore.save_local("faiss_index")
    print("Vector store saved to 'faiss_index/'")

    return vectorstore

if __name__ == "__main__":
    vectorstore = build_vector_store()
    print("Done! Vector store is ready.")
