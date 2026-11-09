# ================================================================
# CLIENT INTERAZIONE CON GRAFANA - DASHBOARD
# ================================================================
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Individua la cartella root del progetto (risale di un livello rispetto a client_utility/)
BASE_DIR = Path(__file__).resolve().parent.parent
# prendo la path del file .env
env_path = BASE_DIR / ".env"

# Carica il file .env se presente
load_dotenv(dotenv_path=env_path)

"""Costruisco gli headers"""
headers = {
    'Authorization': f'Bearer {os.getenv("GRAFANA_TOKEN")}',
    "Content-Type": "application/json"
}

##Funzione interna per costruzione base url
def _base_url() -> str:
    return os.getenv("GRAFANA_URL_DASHBOARD","http://localhost:3000/api/dashboard").rstrip('/')

def _dashboard_url(uid: str = None, save_db: bool = False) -> str:
    base_url = _base_url()
    if uid:
        return f"{base_url}/{uid}"
###DA COMPLETARE