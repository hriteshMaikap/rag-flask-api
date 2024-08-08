import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = "question_answer_collection"
    MODEL_NAME = "mistral"
    DEBUG = os.getenv("DEBUG", "False").lower() in ['true', '1', 't']

config = Config()
