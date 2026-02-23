from dotenv import load_dotenv
import os

load_dotenv()

pc_api_key = os.getenv("PINECONE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
if not pc_api_key:
    raise ValueError("PINECONE API KEY no encontrada")