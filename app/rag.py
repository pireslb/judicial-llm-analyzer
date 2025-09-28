import re
from .policy import POLICY_RULES

def search_policy(query, max_results=3):
    """
    Busca trechos relevantes da política usando correspondência de palavras-chave.
    Retorna lista de pares (id, texto).
    """
    results = []
    keywords = re.findall(r'\w+', query.lower())
    for pol_id, pol_text in POLICY_RULES.items():
        score = sum(1 for kw in keywords if kw in pol_text.lower())
        if score > 0:
            results.append((pol_id, pol_text, score))
    results.sort(key=lambda x: -x[2])
    return [(x[0], x[1]) for x in results[:max_results]]

def enrich_prompt_with_policy(query, base_policy=None):
    """
    Retorna política base + trechos mais relevantes para o input do LLM.
    """
    highlights = search_policy(query)
    highlight_text = "\n".join([f"{pid}: {txt}" for pid, txt in highlights])
    if base_policy is None:
        base_policy = "\n".join([f"{k}: {v}" for k, v in POLICY_RULES.items()])
    return base_policy + "\n\nTrechos mais relevantes:\n" + highlight_text