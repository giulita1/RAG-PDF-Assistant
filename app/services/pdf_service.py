from langchain_community.document_loaders import PyPDFLoader
from app.utils.text_splitter import split_documents
from app.services.pinecone_service import get_vector_store

def procesar_subir_pdf(file_path: str):

    loader = PyPDFLoader(file_path)
    pags = loader.load()

    docs = split_documents(pags)

    vector_store = get_vector_store()
    vector_store.add_documents(docs)

    return True

