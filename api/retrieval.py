from flask import Blueprint, jsonify, request
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
from config import config

retrieval_blueprint = Blueprint('retrieval', __name__)

qdrant_client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
embeddings = FastEmbedEmbeddings()
vector_store = QdrantVectorStore(client=qdrant_client, collection_name=config.COLLECTION_NAME, embedding=embeddings)

retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 3, "score_threshold": 0.5})

@retrieval_blueprint.route('/retrieve', methods=['POST'])
def retrieve():
    """
    Endpoint to retrieve relevant documents from Qdrant based on a query.
    """
    data = request.get_json()
    query = data.get("query", "What is the purpose of this document?")
    results = retriever.get_relevant_documents(query)
    
    serialized_results = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in results]
    
    return jsonify({"query": query, "results": serialized_results})
