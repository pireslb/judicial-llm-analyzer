from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Documento(BaseModel):
    id: str
    dataHoraJuntada: datetime
    nome: str
    texto: str

class Movimento(BaseModel):
    dataHora: datetime
    descricao: str

class Honorarios(BaseModel):
    contratuais: Optional[float] = None
    periciais: Optional[float] = None
    sucumbenciais: Optional[float] = None

class Processo(BaseModel):
    numeroProcesso: str
    classe: str
    orgaoJulgador: str
    ultimaDistribuicao: datetime
    assunto: str
    segredoJustica: bool
    justicaGratuita: bool
    siglaTribunal: str
    esfera: str
    documentos: List[Documento]
    movimentos: List[Movimento]
    valorCausa: Optional[float] = None
    valorCondenacao: Optional[float] = None
    honorarios: Optional[Honorarios] = None
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict)

class DecisionResult(BaseModel):
    decision: str
    rationale: str
    citations: List[str]