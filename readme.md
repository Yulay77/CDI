# Automatisation des Offres d'Emploi

Ce projet permet d'automatiser la récupération, l'analyse et le traitement des offres d'emploi à partir de sites comme Welcome to the Jungle. Il utilise Selenium pour le scraping, Airtable pour le stockage des données, et DeepSeek pour l'analyse des contenus.

## Prérequis Généraux

1. **Python 3.14** ou version supérieure.
2. **Google Chrome** et le **ChromeDriver** correspondant à votre version de Chrome.
3. **Docker** (si vous souhaitez utiliser le déploiement via Docker).
4. **Airtable** avec une base configurée pour stocker les données.
5. **DeepSeek API** pour l'analyse des contenus.
6. **Fichier `.env`** contenant les clés API nécessaires.

---

## Setup Airtable

### Base Airtable
Vous devez créer une base Airtable avec les tables suivantes :

1. **Table `Liste`** :
   - Champs nécessaires :
     - `Entreprise` (Texte)
     - `Poste` (Texte)
     - `URL` (Texte)
     - `Type de taf` (Texte)
     - `Salaire minimum (k)` (Nombre)
     - `Salaire maximum (k)` (Nombre)
     - `Posté le` (Date)
     - `Stack` (Texte)
     - `LettreMotiv` (Texte)
     - `Descriptif` (Texte)
     - `Expérience` (Texte)

2. **Table `Banlist`** :
   - Champs nécessaires :
     - `Entreprise` (Texte)
     - `Poste` (Texte)

### Token Airtable
- Créez un **token API Airtable** avec les permissions `read/write` pour accéder à votre base.
- Ajoutez ce token dans le fichier `.env` sous la clé `AIRTABLE_TOKEN`.

---

## Setup DeepSeek

1. Créez un compte sur [DeepSeek](https://api.deepseek.com).
2. Générez une clé API et ajoutez-la dans le fichier `.env` sous la clé `DEEPSEEK_API_KEY`.
3. Assurez-vous que votre clé API a les permissions nécessaires pour utiliser les modèles de complétion.

---

## Configuration Personnalisée

### Objet `find` dans `index.py`
L'objet `find` contient les URLs et les paramètres de recherche pour les offres d'emploi. Vous pouvez personnaliser les valeurs suivantes :
- `url` : URL de recherche sur Welcome to the Jungle. Faites en sorte de fournir une url de recherche avec des filtres pour affiner les résultats.
- `Type` : Type de poste (ex. "Dev", "GDP" ou tout autre valeur  que vous rajoutez dans la colonne "Type de taf" dans votre base).
- `Exp` : Niveau d'expérience (ex. "0-1", "1-3").

Exemple :
```python
find = [
    {
        "url": "https://www.welcometothejungle.com/fr/jobs?query=d%C3%A9veloppeur%20ful...",
        "Type": "Dev",
        "Exp": "0-1"
    },
    ...
]
```

### Mots-clés dans `jobInfos.py` et `pageDescription.py`
Les mots-clés utilisés pour exclure certaines offres ou pour générer des informations spécifiques sont définis dans les fonctions correspondantes. Vous pouvez les personnaliser selon vos besoins.

Exemple dans jobInfos.py :
```python
keywords = ["Java", "JavaScript", "Python", "C++", "senior", "8 ans d'expérience", "full-stack", "remote", "CDI", "freelance"]
```

Exemple dans `pageDescription.py` :
```python
exclude_keywords = ["stage", "alternance", "freelance", "non rémunéré", ...]
```

### Prompts DeepSeek
Les prompts utilisés pour interagir avec l'API DeepSeek sont définis dans `content/deepseek.py`. Vous pouvez les adapter pour répondre à vos besoins spécifiques.

Exemple :
```python
system_prompt = [
    "L'utilisateur va t'envoyer la description d'une offre d'emploi. Tu dois analyser celle-ci et retourner au format texte brut la stack du poste. ..."
]
```

---

## Installation et Lancement

1. Clonez le dépôt :
   ```bash
   git clone <url_du_dépôt>
   cd scarp-wtj
   ```

2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez le fichier `.env` :
   ```env
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   AIRTABLE_TOKEN=pat-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. Lancez le script principal :
   ```bash
   python index.py
   ```

## Fonctionnement du Script

Le script est conçu pour automatiser la récupération, l'analyse et le traitement des offres d'emploi à partir de sites comme Welcome to the Jungle. Voici une explication détaillée de son fonctionnement :

### 1. **Initialisation**
- Le script commence par importer les bibliothèques nécessaires, comme `selenium` pour le scraping, et configure un navigateur Chrome en mode headless pour exécuter les tâches en arrière-plan.
- Une liste d'objets `find` est définie, contenant les URLs des recherches d'offres d'emploi, le type de poste (`Type`) et le niveau d'expérience (`Exp`).

### 2. **Récupération des Offres**
- La fonction principale `getJobsInfos` parcourt chaque URL dans la liste `find` :
  - Elle ouvre la page de recherche d'offres d'emploi.
  - Elle identifie les blocs d'offres sur la page en utilisant des sélecteurs CSS.
  - Elle filtre les offres déjà présentes dans Airtable ou celles qui contiennent des mots-clés exclus.

### 3. **Analyse des Offres**
- Pour chaque offre, les informations suivantes sont extraites :
  - **Entreprise** : Nom de l'entreprise.
  - **Poste** : Titre du poste.
  - **Ville** : Localisation.
  - **Lien** : URL de l'offre.
  - **Salaire** : Fourchette de salaire (si disponible).
  - **Date** : Date de publication de l'offre.
- Les offres sont ensuite analysées pour exclure celles qui ne correspondent pas aux critères définis (par exemple, mots-clés exclus ou date dépassée).

### 4. **Analyse du Contenu avec DeepSeek**
- Si une offre passe les filtres initiaux, son contenu est analysé en détail :
  - La fonction `generateStackAndLetter` extrait le contenu de la page de l'offre.
  - Une **stack technique** est générée à l'aide de l'API DeepSeek.
  - Une **lettre de motivation personnalisée** est également générée en fonction du contenu de l'offre et du résumé du CV.

### 5. **Envoi des Données**
- Les offres valides sont envoyées à Airtable via l'API Airtable.
- Les offres exclues (par exemple, celles sans lettre de motivation ou stack) sont ajoutées à une liste de bannissement pour éviter de les traiter à nouveau.

### 6. **Planification des Tâches**
- La fonction `schedule_jobs` exécute le script automatiquement toutes les 2 heures entre 9h et 19h, jusqu'à une date limite (31 juillet 2025).
- En dehors de cette plage horaire, le script reste en veille.

### 7. **Logs et Débogage**
- Des messages de débogage (`[DEBUG]`) sont affichés tout au long du script pour suivre son exécution et identifier les éventuels problèmes.

---

### Exemple de Flux d'Exécution
1. Le script ouvre une URL de recherche d'offres d'emploi.
2. Il identifie et filtre les offres déjà présentes ou non valides.
3. Il analyse le contenu des offres restantes avec DeepSeek.
4. Les offres valides sont envoyées à Airtable, et les autres sont ajoutées à la liste de bannissement.
5. Le script attend 2 heures avant de relancer le processus.

