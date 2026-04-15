import json
import os

FICHIER_EMPLOYES = "employes.json"
FICHIER_DEMANDES = "demandes.json"


def charger_employes():
    if not os.path.exists(FICHIER_EMPLOYES):
        return []
    with open(FICHIER_EMPLOYES, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_employes(employes):
    with open(FICHIER_EMPLOYES, "w", encoding="utf-8") as f:
        json.dump(employes, f, indent=4, ensure_ascii=False)


def charger_demandes():
    if not os.path.exists(FICHIER_DEMANDES):
        return []
    with open(FICHIER_DEMANDES, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_demandes(demandes):
    with open(FICHIER_DEMANDES, "w", encoding="utf-8") as f:
        json.dump(demandes, f, indent=4, ensure_ascii=False)