
---

# 📚 Retrieval-Augmented Generation (RAG) Flask API

Welcome to the **RAG Flask API**! This project implements a Retrieval-Augmented Generation model using Flask, Qdrant Cloud DB, and various AI-driven tools. The API enables you to ingest data from documents, retrieve relevant information based on queries, and generate concise answers using a language model.

## 🌟 Features

- **Data Ingestion**: Ingest data from PDF documents and store it in Qdrant Cloud DB.
- **Information Retrieval**: Retrieve relevant information using vector search in Qdrant based on the user's query.
- **Answer Generation**: Generate concise answers by augmenting the retrieved context with a language model.
- **Modular Design**: Each component of the RAG model is encapsulated in its own Flask blueprint, ensuring a clean and maintainable codebase.
- **Easy Deployment**: Ready-to-deploy with environment configurations for different setups.

## 📂 Project Structure

```bash
project_root/
├── api/
│   ├── __init__.py           # Flask blueprint initialization
│   ├── ingestion.py          # Handles data ingestion into Qdrant
│   ├── retrieval.py          # Handles information retrieval
│   ├── generation.py         # Handles answer generation
├── data/
│   └── Question_Answer.pdf   # Sample PDF document for ingestion
├── config.py                 # Configuration file for Flask app
├── venv/                     # Virtual environment directory
├── app.py                    # Main Flask application entry point
├── ingest_data.py            # Script to ingest data into Qdrant
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation (this file)
└── .env                      # Environment variables configuration
```

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rag-flask-api.git
cd rag-flask-api
```

### 2. Set Up the Environment

* Create and activate a virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate  # On Linux use `venv\bin\activate`
```

* Install the dependencies:

```bash
pip install -r requirements.txt
```

* Create a `.env` file in the project root with your configurations:

```bash
# .env
QDRANT_URL=<Your-Qdrant-URL>
QDRANT_API_KEY=<Your-Qdrant-API-Key>
DEBUG=True
```

### 3. Ingest Data

Run the `ingest_data.py` script to ingest data into Qdrant:

```bash
python ingest_data.py
```

### 4. Run Flask App

```bash
python app.py
```

### 5. Use the Endpoints

**Data Retrieval**

* Endpoint: `/api/retrieve`
* Method: `POST`
* Request:

```json
{
  "query": "Your sample query here"
}
```

**Answer Generation**

* Endpoint: `/api/generate`
* Method: `POST`
* Request:

```json
{
  "query": "Your sample query here"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or improvements.

---