import json
import sys
import argparse

from client_utility.grafana_client import send_alert_rule,get_alert_rule,remove_alert_rule
from liveness.grafana_rule_liveness_factory import build_liveness_payload,build_liveness_error_code_payload
from tomcat_memory.grafana_rule_memory_factory import build_tomcat_memory_payload

# ============================================================================================
# FUNZIONE - AGGIUNTA REGOLA
# ============================================================================================

def add_rule(args):
    """Gestisce la creazione delle regole per un cliente."""
    client=args.client_name
    host_tag=args.host_tag
    print(f"--- Avvio creazione regole Grafana per il cliente {client} con tag host {host_tag} ")

    #ID cartelle e datasource su grafana
    HTTP_FOLDER = "b2207f92-a819-41c6-98d7-1eb4976f17bc"
    HTTP_DATASOURCE = "b26118fc-5d80-49c7-8d38-4169f33a36bd"
    MEM_FOLDER = "f599e18f-fb8d-4c20-a807-3afaaf7777ed"
    MEM_DATASOURCE = "d1aa2e0c-8d38-4722-a27f-dac0e7a44605"

    #Definisco le regole da creare
    rules =[
        build_liveness_payload(client,HTTP_FOLDER,HTTP_DATASOURCE),
        build_liveness_error_code_payload(client,HTTP_FOLDER,HTTP_DATASOURCE),
        build_tomcat_memory_payload(client, host_tag, MEM_FOLDER, MEM_DATASOURCE)
    ]

    #Invio le regole su grafana
    for rule in rules:
        send_alert_rule(rule)

# ============================================================================================
# FUNZIONE - RIMOZIONE REGOLA
# ============================================================================================

def remove_rule(args):
    """Gestisce la rimozione di una regola tramite uid"""
    print(f"--- Rimuovo la regola con uid: {args.uid} da Grafana")
    remove_alert_rule(args.uid)

# ============================================================================================
# FUNZIONE - RICERCA REGOLA
# ============================================================================================

def get_rule(args):
    """Gestisce la get di una regola tramite uid"""
    print(f"--- Scarico la regola con uid: {args.uid} da Grafana")
    rule = get_alert_rule(args.uid)
    if rule:
        print(json.dumps(rule, indent=4))
    else:
        print(f"Impossibile recuperare i dati per regola con UID: {args.uid}")

# ============================================================================================
# MAIN - FUNZIONE PRINCIPALE
# ============================================================================================

def main():
    #Parser principale
    program_parser = argparse.ArgumentParser(
                                prog='Grafana rules management',
                                description='Grafana Alerting Tools - Management CLI for rule provisioning',
                                epilog='!!BEVI IN COPPA!!'
    )

    ##Definisco il subparser per la gestione dei comandi
    subparser = program_parser.add_subparsers(dest="command",required=True,help="Comandi disponibili")

    #Definisco l'aggiunta delle regole (addrule NOMECLIENTE HOSTTAG)
    add_rule_parser = subparser.add_parser("addrule",help="Consente di creare le regole su grafana per il cliente passato come parametro",)
    add_rule_parser.add_argument("client_name", help="Nome del cliente del container applicativo")
    add_rule_parser.add_argument("host_tag", help="Tag del cliente influx (es. DLITEPRIVAP1@6001")
    add_rule_parser.set_defaults(func=add_rule)

    #Definisco la rimozione di una regola (removerule UID)
    remove_rule_parser = subparser.add_parser("removerule", help="Consente di rimuovere una regola da grafana attraverso il suo uid")
    remove_rule_parser.add_argument("uid", help="Uid del regola da grafana")
    remove_rule_parser.set_defaults(func=remove_rule)

    #Definisco il recupero di una regola in json attraverso il suo UID (getrule UID)
    get_rule_parser = subparser.add_parser("getrule", help="Consente di ricevere il json completo di una regola attraverso il suo uid")
    get_rule_parser.add_argument("uid", help="Uid del regola da grafana")
    get_rule_parser.set_defaults(func=get_rule)

    #Verifico se non sono stati passati parametri, allora stampo l'help
    if len(sys.argv) == 1:
        program_parser.print_help()
        sys.exit(0)

    #Parsing argomenti da cli
    args = program_parser.parse_args()

    #Eseguo la funzione associata (definite sopra)
    args.func(args)

if __name__ == "__main__":
    main()