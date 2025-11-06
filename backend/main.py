# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from db import init_db, save_lead
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
init_db()  # Cria o banco e tabela se não existir

# Modelo de lead
class Lead(BaseModel):
    name: str
    email: str
    personal_phone: str
    score: int
    moves: int
    time: int

# Configuração CORS
origins = [
    "https://oxygame.netlify.app/",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Substitua aqui pela sua API Key do RD Station
RD_API_KEY = "d2364c686dcd0a66d8d286b153f425be "

# Endpoint para receber lead do front-end
@app.post("/api/lead")
async def create_lead(lead: Lead):
    print("Payload recebido:", lead.dict())

    # Salva no SQLite
    save_lead(lead.name, lead.email, lead.personal_phone, lead.score, lead.moves, lead.time)

    # Envia para o RD Station via API Key
    rd_url = f"https://api.rd.services/platform/conversions?api_key={RD_API_KEY}"
    rd_payload = {
        "event_type": "CONVERSION",
        "event_family": "CDP",
        "payload": {
            "conversion_identifier": "JogoDaMemoria2025",
            "name": lead.name,
            "email": lead.email,
            "personal_phone": lead.personal_phone,
            "tags": ["evento", "jogo da memória"],
            "available_for_mailing": True,
            "legal_bases": [
                {"category": "communications", "type": "consent", "status": "granted"}
            ]
        }
    }
    rd_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(rd_url, json=rd_payload, headers=rd_headers)
        print("Resposta RD Station:", response.status_code, response.text)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Erro RD Station:", e)
        # Não gera 500; apenas avisa que RD não recebeu
        return {
            "status": "warning",
            "message": "Lead salvo localmente, mas não enviado para RD Station",
            "error": str(e)
        }

    return {"status": "success", "message": "Lead salvo localmente e enviado para RD Station!"}
