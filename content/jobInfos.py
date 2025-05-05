from selenium.webdriver.common.by import By
import sys
sys.path.append('/c:/Users/charl/Documents/Dev/scarp wtj')
from content.pageDescription import generateStackAndLetter
from utils.db import post_to_airtable, post_to_airtable_banlist
import os
import json
from datetime import datetime
import time 

def finEntrepriseOrJobDiv(block, elementToFind):
    elements_divs = block.find_elements(By.CSS_SELECTOR, 'div[mode="grid"]')
    if not elements_divs:
        print("[DEBUG] Aucun div trouvé avec le sélecteur spécifié.")
        return None
    
    if elementToFind == "entreprise":
        div = elements_divs[0]
        print("Div trouvée et retournée")
    else : 
        div = elements_divs[1]
        print("Div trouvée et retournée")

    return div

def findEntreprise(block):
    try:
        entreprise_div = finEntrepriseOrJobDiv(block, "entreprise")
        entreprise_elem = entreprise_div.find_element(By.TAG_NAME, 'span')
        entreprise_text = entreprise_elem.get_attribute('innerText').replace(".", "")
        print (f"[DEBUG] Entreprise trouvée dans l'html: {entreprise_text}")
    except Exception as e:
        entreprise_text = ""
        print(f"[DEBUG] ENTREPRISE non trouvée. Erreur : {e}")
    return entreprise_text

def findTitre(block):
    try:
        job_div = finEntrepriseOrJobDiv(block, "job")
        titre_elem = job_div.find_element(By.TAG_NAME, 'h4')
        titre_text = titre_elem.get_attribute('innerText').strip()
        print (f"[DEBUG] Poste trouvé dans l'html: {titre_text}")
    except:
        titre_text = ""
        print("[DEBUG] POSTE: Non trouvé")
    return titre_text

def findSpans(block):
    try:
        # Récupérer tous les éléments <span> dans le bloc
        spans = block.find_elements(By.TAG_NAME, 'span')
        if not spans:
            print("[DEBUG] Aucun élément <span> trouvé dans le bloc.")
            return False
        return spans
    except Exception as e:
        print(f"[DEBUG] Erreur dans findSpans : {e}")
        return False

def findDejaVu(block):
    try:
        # Récupérer tous les éléments <span> dans le bloc
        spans = findSpans(block)

        # Vérifier si l'un des <span> contient le texte "Déjà vu"
        for span in spans:
            if "Déjà vu" in span.get_attribute('innerText'):
                print("[DEBUG] 'Déjà vu' trouvé dans un <span>.")
                return True

        print(f"[DEBUG] 'Déjà vu' non trouvé dans les {len(spans)} <span>.")
       
        return False

    except Exception as e:
        print(f"[DEBUG] Erreur dans findDejaVu : {e}")
       
        return False
    

def findVille(block):
    try:
        job_div = finEntrepriseOrJobDiv(block, "job")

        spans = findSpans(job_div)
        if not spans:
            print("Aucun span trouvé dans la div job")
            return False
        for span in spans:
            print(f"[DEBUG] span trouvé : {span.get_attribute('innerText')}")

        ville_text = spans[0].get_attribute('innerText')
        print(f"[DEBUG] Ville trouvée dans l'html: {ville_text}")
            
    except:
        ville_text = ""
        print("[DEBUG] VILLE: Non trouvé")
    return ville_text

def findLink(block):
    try:
        links = block.find_elements(By.XPATH, './/a[@href]')
        link = links[0].get_attribute('href')
        print(f"[DEBUG] Lien trouvé dans l'html: {link}")
    except:
        link = ""
        print("[DEBUG] LINK: Non trouvé")
    return link

def findSalaire(block):
    try:
        spans = findSpans(block)
        salaire_text = None
        for span in spans:
            if "€" in span.get_attribute('innerText'):
                print("[DEBUG] Salaire trouvé dans un <span>.")
                salaire_text= span.get_attribute('innerText')
    except:
        salaire_text = "Non spécifié"
        print("[DEBUG] SALAIRE: Non trouvé")

    return salaire_text
def findDate(block):
    try:

        time_value = block.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
        print(f"[DEBUG] Date trouvée dans l'html: {time_value}")
    except:
        time_value = ""
        print("[DEBUG] Date: Non trouvé")
    return time_value

def exludeIfKeyWords(titre_text, DontSave):
    for keyword in ["Java,", "Java ", "Java.", "C++", "senior",  "8 ans d'expérience", "7 ans d'expérience", "6 ans d'expérience", "5 ans d'exp", "4 ans d'exp", "CRM"]:
        if keyword in titre_text:
            print(f"[DEBUG] Poste filtré en raison du mot-clé exclu : {keyword}")
            return True
    if DontSave:
        print("[DEBUG] Poste filtré en raison de la variable DontSave.")
        return True
    return False

def excludeIfDatePassed(time_value):
    try:
        job_date = datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%SZ")
        today = datetime.utcnow()
        if (today - job_date).days > 15:
            print("[DEBUG] Offre exclue : date dépassant J-15.")
            return True
        return False
    except Exception as e:
        print(f"[DEBUG] Erreur lors de la vérification de la date : {e}")
        return False
    
def getJobInfos(block, idx, driver, jobType, exp):
    time.sleep(1)
    print(f"\n=== Bloc {idx+1} ===")
    DontSave = False
    entreprise = findEntreprise(block)
    print(f"[DEBUG] Entreprise trouvée : {entreprise}")
    titre = findTitre(block)
    print(f"[DEBUG] Poste trouvé : {titre}")
    ville = findVille(block)
    link = findLink(block)
    salaire_text = findSalaire(block)
    time_value = findDate(block)

    excludeKeyWords = exludeIfKeyWords(titre, DontSave)
    excludeWithDate = excludeIfDatePassed(time_value)
    missingInfos = not entreprise or not titre or not ville or not link  or not time_value

    if excludeKeyWords :
        print("[DEBUG] Offre exclue : mots-clés trouvés.")
        post_to_airtable_banlist(entreprise, titre)
    elif excludeWithDate:
        print("[DEBUG] Offre exclue : date dépassée.")
        post_to_airtable_banlist(entreprise, titre)
    elif missingInfos:
        print("[DEBUG] Problème avec la récupération des infos. (bloc non trouvé)")
        post_to_airtable_banlist(entreprise, titre)
    else:
        lettre_de_motiv = ""
        stack = ""
        descriptif = ""

        if link:
            generatedContent = generateStackAndLetter(link, driver)
            if generatedContent:
                lettre_de_motiv = generatedContent.get("lettre de motiv", "")
                stack = generatedContent.get("stack", "")
                descriptif = generatedContent.get("descriptif", "")

                # Si lettre_de_motiv est vide, exclure l'offre
                if not lettre_de_motiv:
                    print("[DEBUG] Offre exclue : mots clefs dans le descriptif de l'offre.")
                    post_to_airtable_banlist(entreprise, titre)
                    return None
            else:
                print("[DEBUG] Offre exclue : contenu généré invalide.")
                post_to_airtable_banlist(entreprise, titre)

                return None

        # Extraction du salaire minimum et maximum
        salaire_min, salaire_max = 0, 0
        if "à" in salaire_text:
            try:
                salaire_parts = salaire_text.split("à")
                salaire_min = salaire_parts[0].strip().replace("K", "").replace("€", "").strip()
                salaire_min = float(salaire_min)
                salaire_max = salaire_parts[1].strip().replace("K", "").replace("€", "").strip()
                salaire_max = float(salaire_max)
            except:
                print("[DEBUG] Erreur lors de l'extraction des salaires.")
        elif "K" in salaire_text:
            try:
                salaire_min = salaire_text.replace("K", "").replace("€", "").strip()
                salaire_min = float(salaire_min)
                salaire_max = salaire_min
            except:
                print("[DEBUG] Erreur lors de l'extraction du salaire.")

        print(f"[DEBUG] Salaire minimum: {salaire_min}, Salaire maximum: {salaire_max}")
        try:
            time_value = datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            print(f"[DEBUG] Date formatée: {time_value}")
        except Exception as e:
            print(f"[DEBUG] Erreur lors du formatage de la date: {e}")

        # Stockage de l'objet
        if lettre_de_motiv and stack and descriptif:
            job = {
                "Poste": titre,
                "Entreprise": entreprise,
                "Lieu": ville,
                "URL": link,
                "Type de taf": jobType,
                "Salaire minimum (k)": salaire_min,
                "Salaire maximum (k)": salaire_max,
                "Posté le": time_value,
                "Stack": stack,
                "LettreMotiv": lettre_de_motiv,
                "Descriptif": descriptif,
                "Expérience": exp,
            }
            post_to_airtable(job)
            print("[DEBUG] Objet job envoyé à Airtable.")
            time.sleep(2)
        else:
            print("[DEBUG] Offre exclue : contenu incomplet.")
            post_to_airtable_banlist(entreprise, titre)

            return None