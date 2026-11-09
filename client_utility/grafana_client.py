# ================================================================
# CLIENT INTERAZIONE CON GRAFANA - ALERT
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

## Funzione interna per costruzione url
def _build_url_rule(uid=None) -> str:
    base_url = os.getenv("GRAFANA_URL", "http://localhost:3000/grafana/api/v1/provisioning/alert-rules").rstrip('/')
    return f"{base_url}/{uid}" if uid else base_url


### Invio regola da json su grafana
def send_alert_rule(json_payload):
    """Invia un payload generico di una regola a Grafana tramite API POST."""
    response = requests.post(os.getenv("GRAFANA_URL","http://localhost:3000/grafana/api/v1/provisioning/alert-rules"), headers=headers, json=json_payload)
    if response.status_code in (200, 201):
        data = response.json()
        print(f" OK: Regola '{data.get('title')}' creata con successo! (UID: {data.get('uid')})")
        return data
    else:
        print(f" ERROR ({response.status_code}) per '{json_payload.get('title')}': {response.text}")
        return None

### Richiesta di regola da grafana tramite uid - ritorna un json
def get_alert_rule(uid):
    url = _build_url_rule(uid)
    response_get = requests.get(url, headers=headers)
    if response_get.status_code in (200,201):
        return response_get.json()
    else:
        print(f" ERROR ({response_get.status_code}) per richiesta regola con uid:{uid}")
        return None


def remove_alert_rule(uid):
    url = _build_url_rule(uid)
    response_delete = requests.delete(url, headers=headers)
    if response_delete.status_code == 204:
        print(f"Regola con uid {uid} eliminata correttamente")
    else:
        print(f" ERROR ({response_delete.status_code}) per richiesta regola con uid:{uid}")
    return None
