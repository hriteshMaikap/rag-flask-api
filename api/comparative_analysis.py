from flask import Blueprint, jsonify, request
from api.common import format_docs, run_chain, get_prompt_template
from api.retrieval import retriever

comparative_blueprint = Blueprint('comparative', __name__)

@comparative_blueprint.route('/compare', methods=['POST'])
def compare():
    """
    Endpoint to perform a comparative analysis using retrieved documents and a language model.
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        comparison_query = data.get("comparison_query", "Compare Binary Search and Linear Search")
        
        results = retriever.get_relevant_documents(comparison_query)
        context = format_docs(results)
        
        if not context:
            return jsonify({"comparison": "I don't have enough information to perform a comparison."})

        inputs = {"context": context, "comparison_query": comparison_query}
        prompt_template = get_prompt_template("comparative")
        comparison = run_chain(prompt_template, inputs)
        
        return jsonify({"comparison_query": comparison_query, "comparison": comparison})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
