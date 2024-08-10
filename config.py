import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = "question_answer_collection"
    #MODEL_NAME = "llama3-70b-8192"  # Related to the retrieval part
    DEBUG = os.getenv("DEBUG", "False").lower() in ['true', '1', 't']
    #GROQ_API_KEY = os.getenv("GROQ_API_KEY")

config = Config()
