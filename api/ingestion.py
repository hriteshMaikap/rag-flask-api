from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
import os
from config import config

def create_collection_if_not_exists(client):
    """
    Creates the collection in Qdrant if it does not exist, or recreates it with the correct dimensionality.
    """
    try:
        collections = client.get_collections().collections
        if config.COLLECTION_NAME not in [col.name for col in collections]:
            client.create_collection(
                collection_name=config.COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"Collection `{config.COLLECTION_NAME}` created successfully.")
        else:
            print(f"Collection `{config.COLLECTION_NAME}` already exists.")
    except Exception as e:
        print(f"Failed to create collection: {e}")

def ingest():
    """
    Ingests new data from PDF files in the 'data' folder into Qdrant Cloud DB.
    """
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"Folder {data_folder} does not exist.")
    
    client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
    
    create_collection_if_not_exists(client)
    
    for pdf_file in os.listdir(data_folder):
        if pdf_file.endswith(".pdf"):
            pdf_file_path = os.path.join(data_folder, pdf_file)
            docs = PyPDFLoader(file_path=pdf_file_path).load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)
            
            embeddings = FastEmbedEmbeddings()

            vector_store = QdrantVectorStore.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=config.COLLECTION_NAME,
                url=config.QDRANT_URL,
                api_key=config.QDRANT_API_KEY,
                force_recreate=True  # Recreate the collection if dimensions don't match
            )
            print(f"Document {pdf_file} ingested successfully.")
    
    print("Ingestion process completed.")

    # Return the vector store retriever for querying purposes
    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.5,
        },
    )
