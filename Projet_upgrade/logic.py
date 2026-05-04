from datetime import date
from data import *

def login(email, password):
    for emp in charger_employes():
        if emp["email"] == email and emp["password"] == password:
            return emp
    return None


def soumettre_demande(emp_id, nom, d1, d2, motif=""):
    d1 = date.fromisoformat(d1)
    d2 = date.fromisoformat(d2)

    if d2 < d1:
        return None

    nb_jours = (d2 - d1).days + 1

    employes = charger_employes()
    for emp in employes:
        if emp["id"] == emp_id and nb_jours > emp["solde"]:
            return None

    demandes = charger_demandes()
    new_id = max([d["id"] for d in demandes], default=0) + 1

    demande = {
        "id": new_id,
        "employe_id": emp_id,
        "employe_nom": nom,
        "date_debut": str(d1),
        "date_fin": str(d2),
        "nb_jours": nb_jours,
        "motif": motif,
        "statut": "EN_ATTENTE"
    }

    demandes.append(demande)
    sauvegarder_demandes(demandes)

    return demande