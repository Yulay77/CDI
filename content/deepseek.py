from utils.api_prompt import getDeepSeekResponse

def generateStack(content):
   
    system_prompt = [
        "L'utilisateur va t'envoyer la description d'une offre d'emploi. Tu dois analyser celle-ci et retourner au format texte brut la stack du poste. Retourne uniquement la stack, pas d'autre texte, pas de mise en forme."
    ]

    
    try:
        response = getDeepSeekResponse(system_prompt, content)
        print("[DEBUG] Réponse de l'API reçue :", response)
        return response
    except Exception as e:
        print(f"[ERROR] Erreur lors de la génération de la lettre de motivation : {e}")
        return None

def finalCheck(content):
   
    system_prompt = [
        "L'utilisateur va t'envoyer la description d'une offre d'emploi. Tu dois analyser celle-ci et la comparer avec le CV que je vais te joindre. Tu dois exclure les postes demandant + de trois ans d'expérience. Retourne True si le poste est valide, sinon retourne False. Retourne uniquement True ou False, pas d'autre texte, pas de mise en forme."
        "Pour l'expérience, aie une légère tolérance vu que j'ai 3 ans d'expérience en alternance en chef de projet digital principalement. Si le poste de product owner convient à un junior ou ancien alternant tu peux l'inclure, tu peux accepter les offres nécessitant un peu + d'expérience pour le poste de chef de projet digital mais exclue les postes senior ou trop confirmés."
        "Voici le résumé de mon CV :",
        """
        ## Profil       
        Tom SERAYET est un Product Owner et chef de projet digital avec plusieurs expériences dans le digital. Passionné par l'innovation et la création de valeur pour les utilisateurs, il a développé une expertise en gestion de produits digitaux, notamment chez Renault Group. Son parcours diversifié en alternance et en freelance lui a permis d'acquérir une vision à 360° des enjeux digitaux, alliant compétences stratégiques et opérationnelles.

        ## Parcours professionnel
        Chez Retail Renault Group, Tom a assuré la maintenance et l'évolution de multiples sites web, tout en conduisant des projets d'UX Research et d'AB Testing. Il a également mené diverses missions en freelance pour des clients comme Lectra, BedBoat et Repairs!75, démontrant sa capacité à s'adapter à différents environnements et problématiques business. Son expérience couvre la gestion de projet digital, l'UX/UI design et l'analyse des comportements utilisateurs.

        ## Expertise
        Sa double compétence en gestion de produit et en expérience utilisateur lui permet d'orchestrer efficacement des projets digitaux. Certifié Scrum Master PSM 1, il maîtrise les méthodologies agiles, l'analyse de données (KPIs, GA4), la priorisation stratégique et la communication avec les parties prenantes. Tom se distingue également par son expertise en automatisation des processus avec n8n et par sa maîtrise des agents d'intelligence artificielle, permettant d'optimiser les workflows et d'augmenter la productivité des équipes. Son expertise en UX Design et sa connaissance des outils d'analyse comportementale (ContentSquare, Kameleoon) complètent son profil polyvalent.

        ## Formation
        Actuellement en Master Manager de l'innovation du numérique à Web School Factory, Tom possède également une expérience internationale avec une formation en design, marketing et team management en Corée du Sud. Bilingue français-anglais (C1), il allie vision stratégique et aptitudes opérationnelles, avec un fort attrait pour l'optimisation continue des expériences digitales.
        """     
    ]

    
    try:
        response = getDeepSeekResponse(system_prompt, content)
        print("[DEBUG] Réponse de l'API reçue :", response)
        return response
    except Exception as e:
        print(f"[ERROR] Erreur lors de la génération de la lettre de motivation : {e}")
        return None
   

def generateLettreDeMotiv(content):
    """
    Génère une lettre de motivation à partir du contenu fourni.
    
    :param content: Le contenu à utiliser pour générer la lettre de motivation.
    :return: La lettre de motivation générée.
    """
    system_prompt = [
        "Tu es un expert en rédaction de lettres de motivation.",
        "Ton rôle est de rédiger une nouvelle lettre de motivation répondant au descriptif d'offre d'emploi que va t'envoyer l'utilisateur."
        "Base-toi sur ce modèle de lettre de motivation et sur le résumé de mon CV, la lettre de motivation doit respecter le style d'écriture du modèle d'origine en faisant en sorte de lier les éléments de mon CV à l'offre, faire en sorte que je corresponde.",
        "Je candidate soit en tant que product owner, soit en tant que chef de projet digital"
        "Retourne uniquement la lettre de motivation, sans autre texte.",
        "Ne pas faire de mise en forme, juste du texte brut.",
        "Rédige la lettre de motivation dans la langue de l'offre."
        "Voici un exemple de lettre de motivation :",
        """
        Objet : Candidature au poste de Product Owner
        Fort de plusieurs d'expérience à la croisée de la gestion de produit et de l'expérience utilisateur, je souhaite mettre mes compétences à votre service en tant que Product Owner Digital.

        Passionné par l'optimisation des parcours utilisateurs et la création de valeur business, j'ai développé une expertise en méthodologie Agile (certifié Scrum Master PSM 1) et en automatisation des workflows avec n8n et des agents IA. Mon expérience chez Renault Group m'a permis de piloter l'évolution de plusieurs sites web, d'implémenter des stratégies d'AB Testing et de conduire des projets d'UX Research via ContentSquare, me rendant rapidement opérationnel sur des environnements complexes.

        Je serais ravi de contribuer au développement et à l'optimisation de vos produits digitaux, en alignant parfaitement les besoins utilisateurs avec vos objectifs stratégiques.

        Je vous remercie par avance pour l'attention portée à ma candidature et reste disponible pour un entretien afin d'échanger sur ma motivation.
        """,
        "Voici le résumé de mon CV :",
        """
        ## Profil       
        Tom SERAYET est un Product Owner et chef de projet digital avec plusieurs expériences dans le digital. Passionné par l'innovation et la création de valeur pour les utilisateurs, il a développé une expertise en gestion de produits digitaux, notamment chez Renault Group. Son parcours diversifié en alternance et en freelance lui a permis d'acquérir une vision à 360° des enjeux digitaux, alliant compétences stratégiques et opérationnelles.

        ## Parcours professionnel
        Chez Retail Renault Group, Tom a assuré la maintenance et l'évolution de multiples sites web, tout en conduisant des projets d'UX Research et d'AB Testing. Il a également mené diverses missions en freelance pour des clients comme Lectra, BedBoat et Repairs!75, démontrant sa capacité à s'adapter à différents environnements et problématiques business. Son expérience couvre la gestion de projet digital, l'UX/UI design et l'analyse des comportements utilisateurs.

        ## Expertise
        Sa double compétence en gestion de produit et en expérience utilisateur lui permet d'orchestrer efficacement des projets digitaux. Certifié Scrum Master PSM 1, il maîtrise les méthodologies agiles, l'analyse de données (KPIs, GA4), la priorisation stratégique et la communication avec les parties prenantes. Tom se distingue également par son expertise en automatisation des processus avec n8n et par sa maîtrise des agents d'intelligence artificielle, permettant d'optimiser les workflows et d'augmenter la productivité des équipes. Son expertise en UX Design et sa connaissance des outils d'analyse comportementale (ContentSquare, Kameleoon) complètent son profil polyvalent.

        ## Formation
        Actuellement en Master Manager de l'innovation du numérique à Web School Factory, Tom possède également une expérience internationale avec une formation en design, marketing et team management en Corée du Sud. Bilingue français-anglais (C1), il allie vision stratégique et aptitudes opérationnelles, avec un fort attrait pour l'optimisation continue des expériences digitales."""
    ]

    
    try:
        response = getDeepSeekResponse(system_prompt, content)
        return response
    except Exception as e:
        print(f"[ERROR] Erreur lors de la génération de la lettre de motivation : {e}")
        return None