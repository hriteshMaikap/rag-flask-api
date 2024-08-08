from flask import Blueprint, jsonify, request
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from api.retrieval import retriever
from config import config

generation_blueprint = Blueprint('generation', __name__)

model = ChatOllama(model=config.MODEL_NAME)

prompt_template = """
<s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
maximum and keep the answer concise. [/INST] </s> 
[INST] Question: {question} 
Context: {context} 
Answer: [/INST]
"""
prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

def format_docs(docs):
    """
    Formats the documents into a single string for context.
    """
    return "\n\n".join(doc.page_content for doc in docs)

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

        chain = RunnablePassthrough() | prompt | model | StrOutputParser()

        answer = chain.invoke(inputs)
        return jsonify({"query": query, "answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
