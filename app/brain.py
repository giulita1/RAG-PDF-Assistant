from .services.pinecone_service import get_vector_store
from .services.llm_service import build_rag_chain

async def consultar_pinecone(pregunta):

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k":3})

    rag_chain = build_rag_chain(retriever)

    respuesta = await rag_chain.ainvoke(pregunta)

    return respuesta