from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
import os
from config import config

def ingest():
    """
    Ingests data from a PDF file into Qdrant Cloud DB.
    """
    pdf_file_path = os.path.join("data", "Question_Answer.pdf")
    
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"File {pdf_file_path} does not exist.")
    
    # Load documents from PDF
    docs = PyPDFLoader(file_path=pdf_file_path).load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    
    # Use FastEmbedEmbeddings for embedding
    embeddings = FastEmbedEmbeddings()

    # Ingest into Qdrant
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=config.COLLECTION_NAME,
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY
    )

    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.5,
        },
    )
