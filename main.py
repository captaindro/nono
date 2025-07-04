import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    print("=== Démarrage du bot NONO ===")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant pour un bot de sniping Solana."},
                {"role": "user", "content": "Démarre la session."}
            ]
        )
        print("OpenAI response:", response.choices[0].message.content)
    except Exception as e:
        print("Erreur OpenAI:", e)

if __name__ == "__main__":
    main()
