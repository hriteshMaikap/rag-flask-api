from flask import Blueprint, jsonify, request
from api.common import format_docs, run_chain, get_prompt_template
from api.retrieval import retriever

generation_blueprint = Blueprint('generation', __name__)

@generation_blueprint.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint to generate an answer using retrieved documents and a language model.
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        query = data.get("query", "What is the purpose of this document?")
        
        results = retriever.get_relevant_documents(query)
        context = format_docs(results)
        
        if not context:
            return jsonify({"answer": "I don't know the answer."})

        inputs = {"context": context, "question": query}
        prompt_template = get_prompt_template("generation")
        answer = run_chain(prompt_template, inputs)
        
        return jsonify({"query": query, "answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
