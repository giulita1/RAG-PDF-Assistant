from .services.pinecone_service import get_vector_store
from .services.llm_service import build_rag_chain
import json
from datetime import datetime

def log_rag(question, context, answer):

    log = {
        "question": question,
        "context": context,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    }

    with open("rag_logs.json","a") as f:
        json.dump(log,f)
        f.write("\n")

async def consultar_pinecone(pregunta):

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k":3})

    docs = await retriever.ainvoke(pregunta)

    context = "\n".join([doc.page_content for doc in docs])

    rag_chain = build_rag_chain()

    respuesta = await rag_chain.ainvoke({
        "context": context,
        "question": pregunta
    })

    log_rag(pregunta, context, respuesta)

    return respuesta