from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Processo
from app.verifier import verificar_processo

app = FastAPI(title="ML Processo Verifier", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/verify")
def verify_processo(processo: Processo):
    result = verificar_processo(processo.dict())
    return result