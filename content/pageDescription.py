
from selenium.webdriver.common.by import By
import sys
sys.path.append('/c:/Users/charl/Documents/Dev/scarp wtj')
from content.deepseek import generateLettreDeMotiv, generateStack, finalCheck
import time

def generateStackAndLetter(link, driver):
        try:
            driver.get(link)
            time.sleep(1)  # Attente pour chargement de la page
            print("URL actuelle :", driver.current_url)

            clicked_buttons = set()  # Ensemble pour suivre les boutons déjà cliqués

            while True:
                voirplusbuttons = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="view-more-btn"]')
                new_clicks = False  # Indicateur pour savoir si un nouveau clic a été effectué

                for button in voirplusbuttons:
                    if button in clicked_buttons:  # Vérifiez si le bouton a déjà été cliqué
                        continue

                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)  # Scroll to the button
                        time.sleep(0.5)  # Small delay to ensure visibility
                        driver.execute_script("arguments[0].click();", button)
                         # Attente pour chargement du contenu après le clic
                        clicked_buttons.add(button)  # Ajouter le bouton à l'ensemble des boutons cliqués
                        new_clicks = True  # Indiquer qu'un nouveau clic a été effectué
                    except Exception as e:
                        print(f"[DEBUG] Erreur lors du clic sur le bouton 'Voir plus' : {e}")

                if not new_clicks:  # Si aucun nouveau clic n'a été effectué, sortir de la boucle
                    print("[DEBUG] Aucun nouveau bouton 'Voir plus' à cliquer, sortie de la boucle.")
                    break

            target_divs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="job-section-description"], div[data-testid="job-section-experience"], div[data-testid="job-section-process"]')
            content_parts = []
            for div in target_divs:
                if div.tag_name == 'p' or div.tag_name == 'h3' or div.tag_name == 'h4':
                    content_parts.append(div.text)
                elif div.tag_name == 'ul':
                    # Récupérer les éléments de liste
                    li_elements = div.find_elements(By.TAG_NAME, 'li')
                    for li in li_elements:
                        content_parts.append(f"- {li.text}")  # Ajouter un tiret pour formater les listes
                
                else:
                    content_parts.append(div.text)  # Récupérer le texte des autres balises si nécessaire

            # Joindre tout le contenu récupéré
            page_content = "\n".join(content_parts)
    
            found_keywords = [keyword for keyword in ["Java,", "Java ", "Java.", "C++", "senior",  "8 ans d'expérience", "7 ans d'expérience", "6 ans d'expérience", "5 ans d'exp", "4 ans d'exp", "CRM"] if keyword in page_content]

            if found_keywords:
                print(f"[DEBUG] Offre exclue. Keywords trouvés : {', '.join(found_keywords)}")
                return {"lettre de motiv": "", "stack": ""}
            else:
                finalCheck_result = finalCheck(page_content)

                if finalCheck_result == "False":
                    print("[DEBUG] Offre exclue par Deepseek.")
                    return {"lettre de motiv": "", "stack": ""}
                
                else:
                    stack = generateStack(page_content)
                    lettredeMotiv = generateLettreDeMotiv(page_content)
                    return {"lettre de motiv": lettredeMotiv, "stack": stack, "descriptif": page_content}
        except Exception as e:
            print(f"[DEBUG] Erreur lors de l'accès à l'URL ou récupération du contenu : {e}")
        finally:
            driver.back()  # Retour à la page principale
            time.sleep(2)
