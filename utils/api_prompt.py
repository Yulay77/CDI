from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

def getDeepSeekResponse(system_prompt, content):
    print("Début de la fonction getDeepSeekResponse")
        
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("La clé API 'DEEPSEEK_API_KEY' n'est pas définie dans les variables d'environnement ou le fichier .env.")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    system_messages = [{"role": "system", "content": prompt} for prompt in system_prompt]

    messages = system_messages + [{"role": "user", "content": content}]

    response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )

    content = response.choices[0].message.content.strip()

    print("Fin de la fonction getDeepSeekResponse")
    return content
