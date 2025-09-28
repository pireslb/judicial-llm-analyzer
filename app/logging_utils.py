import logging
import json
from datetime import datetime
import os

def setup_logger(log_file="app/logs/app.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("processo_verifier")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

from datetime import datetime

def convert_datetimes(obj):
    if isinstance(obj, dict):
        return {k: convert_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetimes(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def log_decision(logger, processo, result, latency, prompt_version):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "numeroProcesso": processo.get("numeroProcesso"),
        "decision": result.get("decision"),
        "rationale": result.get("rationale"),
        "citations": result.get("citations"),
        "latency": latency,
        "prompt_version": prompt_version,
        "input": processo,
        "output": result
    }
    logger.info(json.dumps(entry, ensure_ascii=False, default=default_serializer))