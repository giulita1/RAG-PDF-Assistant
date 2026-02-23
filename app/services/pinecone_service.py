from pinecone import Pinecone
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from app.config import pc_api_key


embeddings = PineconeEmbeddings(model="llama-text-embed-v2")

index_name = "rag-pdf-assistant-index"

def get_vector_store(namespace: str = "public"):

    pc = Pinecone(api_key=pc_api_key)
    index = pc.Index(index_name)

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace="public"
    )

    return vector_store

def limpiar_namespace(namespace: str):

    pc = Pinecone(api_key=pc_api_key)
    index = pc.Index(index_name)

    index.delete(delete_all=True, namespace=namespace)
