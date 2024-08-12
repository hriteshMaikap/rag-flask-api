from flask import Flask, jsonify, request
from api.retrieval import retrieval_blueprint, retriever
from api.generation import generation_blueprint
from api.comparative_analysis import comparative_blueprint # Import the new blueprint
from config import config

app = Flask(__name__)
app.config.from_object(config)

# Register the blueprints
app.register_blueprint(retrieval_blueprint, url_prefix="/api/retrieval")
app.register_blueprint(generation_blueprint, url_prefix="/api/generation")
app.register_blueprint(comparative_blueprint, url_prefix="/api/comparative")

@app.route('/api/query', methods=['POST'])
def query():
    """
    Route to handle user choice between retrieval-only, generalized query modes, comparative analysis, and formatted retrieval.
    """
    data = request.get_json()

    mode = data.get("mode", "retrieval").lower()
    query = data.get("query", "What is the purpose of this document?")

    if mode == "retrieval":
        results = retriever.get_relevant_documents(query)
        serialized_results = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in results]
        return jsonify({"mode": mode, "query": query, "results": serialized_results})

    elif mode == "generation":
        return app.test_client().post('/api/generation/generate', json={"query": query}).get_data(as_text=True)
    
    elif mode == "comparative":
        return app.test_client().post('/api/comparative/compare', json={"comparison_query": query}).get_data(as_text=True)
    else:
        return jsonify({"error": "Invalid mode selected. Choose 'retrieval', 'generation', 'comparative', or 'formatted_retrieval'."}), 400

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
