from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from content.jobInfos import getJobInfos, findLink, findEntreprise, findTitre, findDejaVu
from utils.db import getAirTableDatas, getAirTableBanList, delete_from_airtable
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import threading

import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


find = [{
    "url": "https://www.welcometothejungle.com/fr/jobs?query=product%20owner&refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bexperience_level_minimum%5D%5B%5D=0-1&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France",
    "Type": "PO",
    "Exp": "0-1"
    },
    {
    "url": "https://www.welcometothejungle.com/fr/jobs?query=chef%20de%20projet%20digital&refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bexperience_level_minimum%5D%5B%5D=0-1&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France",
    "Type": "GDP",
    "Exp": "0-1"
    },
    {
        "url": "https://www.welcometothejungle.com/fr/jobs?query=product%20owner&refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bexperience_level_minimum%5D%5B%5D=1-3&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France",
        "Type": "PO",
        "Exp": "1-3"
    },
    {
    "url": "https://www.welcometothejungle.com/fr/jobs?query=chef%20de%20projet%20digital&refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bexperience_level_minimum%5D%5B%5D=1-3&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France",
    "Type": "GDP",
    "Exp": "1-3"
    },
    {
    "url":"https://www.welcometothejungle.com/fr/jobs?query=proxy%20product%20owner&refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bexperience_level_minimum%5D%5B%5D=0-1&refinementList%5Bexperience_level_minimum%5D%5B%5D=1-3&refinementList%5Bexperience_level_minimum%5D%5B%5D=3-5&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France",
    "Type": "Proxy PO",
    "Exp": "1-5"
    },
    {
    "url":"https://www.welcometothejungle.com/fr/jobs?query=project%20manager&refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bexperience_level_minimum%5D%5B%5D=0-1&refinementList%5Bexperience_level_minimum%5D%5B%5D=1-3&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France",
    "Type": "PM",
    "Exp": "1-5"
    },
]   
def getJobsInfos():
    for idx, i in enumerate(find):
        try:
            print(f"Lancement de la recherce des offres pour la {idx+1}e URL")
            driver = webdriver.Chrome(options=options)
            time.sleep(3)  # Attendre 3 secondes avant de charger la page
            url=i["url"]
            jobType = i["Type"]
            exp = i["Exp"]
            driver.get(url)

            print("Lancement de la récupération et filtrage des blocs")
            offer_blocks = countAndGetOfferBlocks(driver)
            
            if not offer_blocks:
                print("[DEBUG] Aucun bloc d'offres trouvé après le filtrage.")
                driver.quit()
                continue
            else :

                results = []
            
                gotAllJobs = False
                for idx, block in enumerate(offer_blocks):
                    time.sleep(2)  
                    print(f"[DEBUG] Traitement du bloc {idx+1}/{len(offer_blocks)}")
                    job = getJobInfos(block, idx, driver, jobType, exp)
                    results.append(job)
                    if idx == len(offer_blocks) - 1:
                        gotAllJobs = True
                        print("[DEBUG] Tous les blocs d'offres ont été traités.")

                        break
                
                if gotAllJobs:
                    print("[DEBUG] Tous les blocs d'offres ont été traités.")
                    driver.quit()
 

        except Exception as e:
            print(f"[DEBUG] Erreur lors de la récupération des informations sur les offres : {e}")
            break

      

def countAndGetOfferBlocks(driver):
    print("[DEBUG] Début de la fonction countAndGetOfferBlocks.")
    airtableInfos = getAirTableDatas()
    banlistInfos = getAirTableBanList()
    
    try:
        offer_blocks = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="search-results-list-item-wrapper"]')
        print(f"[DEBUG] Nombre de blocs d'offres trouvés avant clean : {len(offer_blocks)}")
        
        if not offer_blocks:
            print("[DEBUG] Aucun bloc d'offres trouvé. Fin de la fonction countAndGetOfferBlocks.")
            return []
        else:
            filtered_blocks = []

            for idx, motherBlock in enumerate(offer_blocks):
                block = motherBlock.find_element(By.CSS_SELECTOR, 'div[mode="grid"]')
                print(f"[DEBUG] Traitement du bloc {idx+1}/{len(offer_blocks)}")
                dejaVu = findDejaVu(block)
                if dejaVu:
                    print("[DEBUG] Bloc déjà vu, exclusion.")
                    continue
                else:
                    entreprise = findEntreprise(block)
                    print(f"[DEBUG] Entreprise trouvée : {entreprise}")
                    poste = findTitre(block)
                    if not entreprise or not poste:
                        print("[DEBUG] Informations manquantes dans le bloc, exclusion.")
                        continue
                    else:
                        print(f"[DEBUG] Poste trouvé : {poste}")
                        infos = {
                            "Entreprise": entreprise,
                            "Poste": poste,
                        }
                        print(f"[DEBUG] Infos du bloc : {infos}")

                        if not any(
                            infos["Entreprise"] == entry["Entreprise"] and infos["Poste"] == entry["Poste"]
                            for entry in airtableInfos + banlistInfos
                        ):
                            print(f"[DEBUG] Bloc ajouté à la liste filtrée : {infos}")
                            filtered_blocks.append(block)  # Ajoutez le bloc à la liste filtrée
                        else:
                            print(f"[DEBUG] Bloc exclu : {infos}")

            print(f"[DEBUG] Nombre de blocs d'offres trouvés après clean : {len(filtered_blocks)}")
            return filtered_blocks

    except Exception as e:
        print(f"[DEBUG] Erreur lors de la récupération des blocs d'offres : {e}")
        return []


def schedule_jobs():
    while True:
        print("CRON initialisé")
        # Obtenir l'heure actuelle
        now = datetime.now()
        current_hour = now.hour


        # Vérifier si la date actuelle est après le 31 juillet 2025
        end_date = datetime(2025, 7, 31, 23, 59, 59)
        if now > end_date:
            print(f"[DEBUG] Arrêt de schedule_jobs car la date limite est atteinte : {now}")
            break

        # Vérifier si l'heure actuelle est entre 9h et 19h
        if 9 <= current_hour <= 19:
            print(f"[DEBUG] Exécution de getJobsInfos à {now}")
            getJobsInfos()
        else:
            print(f"[DEBUG] En dehors de la plage horaire (9h-19h). Heure actuelle : {now}")
        
        print(f"Prochain démarrage de getJobsInfos dans 2 heures à {now + timedelta(hours=2)}")

        time.sleep(2 * 60 * 60)  # 2 heures en secondes

def getJobsInfosForUrl(url_data):
    """Fonction wrapper pour appeler getJobsInfos avec une URL spécifique."""
    try:
        print(f"[THREAD-{threading.current_thread().name}] Lancement pour l'URL : {url_data['url']}")
        driver = webdriver.Chrome(options=options)
        time.sleep(3)  # Attendre 3 secondes avant de charger la page
        url = url_data["url"]
        jobType = url_data["Type"]
        exp = url_data["Exp"]
        driver.get(url)

        print(f"[THREAD-{threading.current_thread().name}] Lancement de la récupération et filtrage des blocs")
        offer_blocks = countAndGetOfferBlocks(driver)

        if not offer_blocks:
            print(f"[THREAD-{threading.current_thread().name}] Aucun bloc d'offres trouvé après le filtrage.")
        else:
            results = []
            for idx, block in enumerate(offer_blocks):
                time.sleep(2)
                print(f"[THREAD-{threading.current_thread().name}] Traitement du bloc {idx+1}/{len(offer_blocks)}")
                job = getJobInfos(block, idx, driver, jobType, exp)
                results.append(job)

            print(f"[THREAD-{threading.current_thread().name}] Tous les blocs d'offres ont été traités.")
        driver.quit()
    except Exception as e:
        print(f"[THREAD-{threading.current_thread().name}] Erreur : {e}")

def runJobsInParallel():
    """Exécute getJobsInfos en parallèle pour chaque URL."""
    with ThreadPoolExecutor(max_workers=len(find)) as executor:
        executor.map(getJobsInfosForUrl, find)

if __name__ == "__main__":
    print("Choisissez une option :")
    print("1 - Exécution sans multithreading")
    print("2 - Exécution avec multithreading")
    choice = input("Entrez votre choix (1 ou 2) : ")

    if choice == "1":
        print("Exécution sans multithreading...")
        getJobsInfos()
    elif choice == "2":
        print("Exécution avec multithreading...")
        runJobsInParallel()
    else:
        print("Choix invalide. Veuillez relancer le script et entrer 1 ou 2.")