from flask import Blueprint, jsonify, request
from api.common import format_docs, run_chain, get_prompt_template
from api.retrieval import retriever

formatted_retrieval_blueprint = Blueprint('formatted_retrieval', __name__)

@formatted_retrieval_blueprint.route('/formatted_retrieve', methods=['POST'])
def formatted_retrieve():
    """
    Endpoint to retrieve and format specific information from documents based on a query.
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        specific_info = data.get("specific_info", "time complexity")
        query = data.get("query", f"Provide the {specific_info}.")

        results = retriever.get_relevant_documents(query)
        context = format_docs(results)
        
        if not context:
            return jsonify({"formatted_info": f"No {specific_info} found in the context."})

        inputs = {"context": context, "specific_info": specific_info}
        prompt_template = get_prompt_template("formatted_retrieval")
        formatted_info = run_chain(prompt_template, inputs)
        
        return jsonify({"query": query, "formatted_info": formatted_info})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
