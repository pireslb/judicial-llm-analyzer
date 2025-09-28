import streamlit as st
import requests
import json

st.set_page_config(page_title="Verificador ML de Processos")

st.title("Verificador de Processos Judiciais (LLM)")

st.write("Preencha os dados do processo judicial conforme exemplo.")

input_json = st.text_area("Dados do processo (JSON)", height=350, value="""
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
  "documentos": [],
  "movimentos": [],
  "valorCausa": 67592,
  "valorCondenacao": 67592,
  "honorarios": {
    "contratuais": 6000,
    "periciais": 1200,
    "sucumbenciais": 3000
  }
}
""")

api_url = st.text_input("URL da API", value="http://localhost:8000/verify")
#api_url = st.text_input("URL da API", value="http://host.docker.internal:8000/verify")
if st.button("Verificar"):
    try:
        processo = json.loads(input_json)
        res = requests.post(api_url, json=processo)
        st.markdown("### Decisão")
        st.json(res.json())
    except Exception as e:
        st.error(f"Erro: {e}")