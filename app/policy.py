# Política interna estruturada para consulta e citação pelo LLM/RAG

POLICY_RULES = {
    "POL-1": "Só compramos crédito de processos transitados em julgado e em fase de execução.",
    "POL-2": "Exigir valor de condenação informado.",
    "POL-3": "Valor de condenação < R$ 1.000,00 → não compra.",
    "POL-4": "Condenações na esfera trabalhista → não compra",
    "POL-5": "Óbito do autor sem habilitação no inventário → não compra",
    "POL-6": "Substabelecimento sem reserva de poderes → não compra",
    "POL-7": "Informar honorários contratuais, periciais e sucumbenciais quando existirem.",
    "POL-8": "Se faltar documento essencial (ex.: trânsito em julgado não comprovado) → incomplete.",
}