from langchain_groq import ChatGroq
from app.config import groq_api_key
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def get_llm():

    llm = ChatGroq(model="llama-3.3-70b-versatile",
               temperature=0,
               api_key=groq_api_key)
    
    return llm

def build_rag_chain(retriever):

    llm = get_llm()

    prompt = ChatPromptTemplate.from_template("""Responde la pregunta usando solo el siguiente contexto.
                                Contexto: {context}
                                Pregunta: {question}""")
    
    rag_chain = ({"context":retriever,
                  "question":RunnablePassthrough()} 
                  | prompt | llm | StrOutputParser())
    
    return rag_chain

