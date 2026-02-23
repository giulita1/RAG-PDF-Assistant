from fastapi import FastAPI, UploadFile, File, Form
from .brain import consultar_pinecone
from fastapi.responses import JSONResponse
from .services.pinecone_service import limpiar_namespace
from contextlib import asynccontextmanager
from .services.pdf_service import procesar_subir_pdf
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("uploads", exist_ok=True)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def serve_frontend():
    return FileResponse("static/index.html")

@app.post('/chat')
async def chat(pregunta: str = Form(...),
               file: UploadFile = File(None)):
    try:
        if file:
            file_path = f"uploads/{file.filename}"

            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)

                procesar_subir_pdf(file_path)

                os.remove(file_path)

        respuesta = await consultar_pinecone(pregunta)

        return {"answer": respuesta}
    
    except Exception as e:
       
        return JSONResponse(
            status_code=500,
            content={"answer":f"Error en el servidor: {str(e)}"}
        )

@app.post('/reset')
async def reset():
    limpiar_namespace("public")
    return {"message": "conversación reiniciada"}

