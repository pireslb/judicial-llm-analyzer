# ML Processo Verifier

Automatizar a análise de processos judiciais conforme política interna usando LLM.

## Como rodar localmente (Docker)

```bash
docker build -t processo-ml-verifier .
docker run -p 8000:8000 --env-file .env processo-ml-verifier
```

A interface visual pode ser executada separadamente:

```bash
streamlit run app/ui.py
```

## Endpoints da API

- `/health`: status da aplicação
- `/verify`: POST. Recebe dados do processo no schema, retorna decisão estruturada.

## Fluxo

1. Recebe dados do processo judicial via API/UI
2. Aplica regras via LLM (OpenAI)
3. Retorna decisão JSON padronizada
4. Disponibiliza via API e UI

## Uso de LLM

O LLM recebe o processo e a política, avalia e retorna JSON estruturado conforme regras citadas.

## .env

Crie um arquivo `.env` (NÃO subir no GitHub!) com:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PROMPT_VERSION=v1.0
```

## Estrutura de pastas

```
processo-ml-verifier/
├── app/
│   ├── api.py
│   ├── logging_utils.py
│   ├── models.py
│   ├── policy.py
│   ├── rag.py
│   ├── ui.py
│   ├── verifier.py
│   ├── prompts/
│   │   └── main_prompt.txt
│   └── logs/
├── Dockerfile
├── requirements.txt
├── README.md
├── .env
```

## Exemplo de chamada via curl

```bash
curl -X POST "http://localhost:8000/verify" -H "Content-Type: application/json" -d @exemplo_processo.json
```

## Exemplo de processo JSON

```json
{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "19ª VARA FEDERAL - SOBRAL/CE",
  "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
  "assunto": "Rural (Art. 48/51)",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF5",
  "esfera": "Federal",
  "documentos": [
    {
      "id": "DOC-1-1",
      "dataHoraJuntada": "2023-09-10T10:12:05.000",
      "nome": "Sentença de Mérito",
      "texto": "PODER JUDICIÁRIO\n19ª VARA FEDERAL – SOBRAL/CE\n\nProce..."
    }
  ],
  "movimentos": [
    {
      "dataHora": "2024-01-20T11:22:33.000",
      "descricao": "Iniciado cumprimento definitivo de sentença."
    }
  ],
  "valorCausa": 67592,
  "valorCondenacao": 67592,
  "honorarios": {
    "contratuais": 6000,
    "periciais": 1200,
    "sucumbenciais": 3000
  }
}
```
