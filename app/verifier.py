import os
import time
import json
from dotenv import load_dotenv
from openai import OpenAI
from .policy import POLICY_RULES
from .rag import enrich_prompt_with_policy
from .logging_utils import setup_logger, log_decision

# Função utilitária para converter datetime em string (ISO)
def convert_datetimes(obj):
    from datetime import datetime
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj

# Função para justificar incomplete
def get_incomplete_reason(processo):
    reasons = []
    if not processo.get("valorCondenacao"):
        reasons.append("Valor de condenação não informado (POL-2).")
    documentos = processo.get("documentos", [])
    if not any("Trânsito" in doc.get("nome", "") for doc in documentos):
        reasons.append("Trânsito em julgado não comprovado (POL-8).")
    if not documentos:
        reasons.append("Nenhum documento essencial incluído.")
    if not processo.get("honorarios"):
        reasons.append("Honorários não informados (POL-7).")
    if not reasons:
        reasons.append("Não foi possível validar todos os requisitos essenciais.")
    return " | ".join(reasons)

# Carregar variáveis de ambiente do .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v1.0")

logger = setup_logger()

def get_prompt():
    with open("app/prompts/main_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def ask_llm(processo_data, policy_text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = get_prompt().replace("{{policy}}", policy_text)
    input_data = json.dumps(processo_data, ensure_ascii=False)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_data}
        ],
        temperature=0
    )
    return completion.choices[0].message.content

def verificar_processo(processo):
    start = time.time()
    try:
        processo_serializado = convert_datetimes(processo)
        policy_text = enrich_prompt_with_policy(json.dumps(processo_serializado))
        llm_response = ask_llm(processo_serializado, policy_text)
        print("LLM response:", llm_response)  # Debug: veja no terminal
        result = json.loads(llm_response)
        # Se o LLM retornar incomplete, acrescente justificativa extra
        if result.get("decision") == "incomplete":
            extra_just = get_incomplete_reason(processo_serializado)
            result["rationale"] += f" | {extra_just}"
    except Exception as e:
        result = {
            "decision": "incomplete",
            "rationale": f"Erro: {str(e)} | {get_incomplete_reason(processo)}",
            "citations": ["POL-8"],
        }
    latency = time.time() - start
    log_decision(logger, processo_serializado, result, latency, PROMPT_VERSION)
    return result