import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Récupérer le token depuis une variable d'environnement
api_token = os.getenv("AIRTABLE_TOKEN")
if not api_token:
    raise ValueError("La variable d'environnement 'AIRTABLE_TOKEN' n'est pas définie.")

def post_to_airtable(data):

    """
    Envoie des données à Airtable via une requête POST.

    :param data: Dictionnaire contenant les données à transmettre.
    :return: Réponse de l'API Airtable.
    """
    # URL de l'API
    url = "https://api.airtable.com/v0/appIQLi5faaxf7dZM/Liste"
    print("Ajout d'une nouvelle offre à Airtable...")
    # En-têtes de la requête
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Effectuer la requête POST
    response = requests.post(url, headers=headers, json={"fields": data})

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        print("Offre ajoutée avec succès")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

    return response

def post_to_airtable_banlist(company,job):

    """
    Envoie des données à Airtable via une requête POST.

    :param data: Dictionnaire contenant les données à transmettre.
    :return: Réponse de l'API Airtable.
    """
    # URL de l'API
    url = "https://api.airtable.com/v0/appIQLi5faaxf7dZM/Banlist"
    print("Envoi de l'URL à la banlist...")
    # En-têtes de la requête
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    if not company or not job:
        print("[DEBUG] Impossible de poster dans la banlist, entreprise ou poste manquant.")
        return None
    else:
    # Effectuer la requête POST
        response = requests.post(url, headers=headers, json={"fields": {"Entreprise": company, "Poste": job}})

        # Vérifier le statut de la réponse
        if response.status_code == 200:
            print("Infos postées avec succès dans la banlist")
        else:
            print(f"Erreur {response.status_code}: {response.text}")

        return response

def getAirTableDatas():
    """
    Récupère les données depuis Airtable et retourne une liste d'entrées valides.

    :return: Liste de dictionnaires contenant les informations des offres.
    """
    # URL de l'API
    url_api = "https://api.airtable.com/v0/appIQLi5faaxf7dZM/Liste"
    print("Récupération des données depuis Airtable...")
    # En-têtes de la requête
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Effectuer la requête GET
    response = requests.get(url_api, headers=headers)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        data = response.json()
        infos = []

        # Parcourir les enregistrements
        for item in data.get("records", []):
            fields = item.get("fields", {})
            entreprise = fields["Entreprise"].strip()
            poste = fields["Poste"].strip()
            url = fields["URL"].strip()
            id = item["id"]
            # Vérifier que les champs nécessaires sont présents
            if entreprise and poste and url:
                object = {
                    "Entreprise": entreprise,
                    "Poste": poste,
                    "id": id,
                }
                print("Données Airtable récupérées")
                infos.append(object)
            else:
                print(f"[DEBUG] Enregistrement ignoré en raison de données incomplètes : {fields}")

        return infos
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return []

def delete_from_airtable(record_id):

    """
    Supprime un enregistrement d'Airtable via une requête DELETE.

    :param record_id: ID de l'enregistrement à supprimer.
    :return: Réponse de l'API Airtable.
    """
    # URL de l'API
    url = f"https://api.airtable.com/v0/appIQLi5faaxf7dZM/Liste/{record_id}"

    # En-têtes de la requête
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Effectuer la requête DELETE
    response = requests.delete(url, headers=headers)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        print("Enregistrement supprimé avec succès :", response.json())
    else:
        print(f"Erreur {response.status_code}: {response.text}")

    return response           
def getAirTableBanList():
    """
    Vérifie si une entrée avec un champ URL spécifique existe dans Airtable.

    :param url: L'URL à vérifier.
    :return: True si l'entrée existe, False sinon.
    """
    print("Récupération des données de la banlist depuis Airtable...")
    # URL de l'API
    url_api = "https://api.airtable.com/v0/appIQLi5faaxf7dZM/Banlist"

    # En-têtes de la requête
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Effectuer la requête GET
    response = requests.get(url_api, headers=headers)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        data = response.json()
        bandata = []
        for item in data.get("records", []):
            if "fields" in item and "Entreprise" in item["fields"] and "Poste" in item["fields"]:
                fields = item["fields"]
                object = {
                    "Entreprise": fields["Entreprise"].strip(),
                    "Poste": fields["Poste"].strip(),
                }
                bandata.append(object)

        
        print("Banlist reçue")
        return bandata
    else:
        print(f"Erreur {response.status_code}: {response.text}")

if __name__ == "__main__":
    url= "https://www.welcometothejungle.com/fr/companies/hello-watt/jobs/developpeur-se-full-stack-python-react-cdi_paris?q=fe02e64d18d037b19be783bf899bd8f5&o=8399de9f-8148-4ed2-a191-e93d3fd90745"
    print("URLs airtable")
    urls = getAirTableDatas()
    print(urls)
