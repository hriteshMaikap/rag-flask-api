# common.py
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from api.retrieval import retriever
from config import config

# Initialize Groq model with API key
groq_chat = ChatGroq(groq_api_key=config.GROQ_API_KEY, model_name=config.MODEL_NAME)

def format_docs(docs):
    """
    Formats the documents into a single string for context.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def run_chain(prompt_template, inputs):
    """
    Runs the prompt chain with the given prompt template and inputs.
    """
    chain = RunnablePassthrough() | prompt_template | groq_chat | StrOutputParser()
    return chain.invoke(inputs)

# Define prompt templates
def get_prompt_template(use_case):
    if use_case == "generation":
        return PromptTemplate(
            input_variables=["context", "question"],
            template="""
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
            maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )
    elif use_case == "comparative":
        return PromptTemplate(
            input_variables=["context", "comparison_query"],
            template="""
            <s> [INST] You are an assistant for comparative analysis tasks. Use the following retrieved context 
            to compare and contrast the specified topics. Try using numbers to explain the comparison. Provide a concise comparison in five sentences maximum. [/INST] </s> 
            [INST] Comparison Request: {comparison_query} 
            Context: {context} 
            Comparison: [/INST]
            """
        )
