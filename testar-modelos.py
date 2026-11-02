
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

chave = os.getenv("GEMINI_API_KEY")

if not chave:
    raise ValueError("Chave GEMINI_API_KEY não encontrada no .env")

cliente = genai.Client(
    api_key=chave,
    http_options=types.HttpOptions(timeout=10000)
)

print("Consultando os modelos do Google...", flush=True)

for modelo in cliente.models.list():
    if "generateContent" in (modelo.supported_actions or []):
        print(modelo.name, flush=True)
