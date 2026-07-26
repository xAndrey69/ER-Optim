import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def ask_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "Eroare: Cheia API lipsește din fișierul .env!"
    
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-flash-latest",
                
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        return f"A apărut o eroare la apelarea API-ului: {e}"

## asta doar pt test daca merge cheia si gemini
if __name__ == "__main__":
    print("Testăm conexiunea cu Gemini API...")
    test_prompt = "Explică-mi ce este un hackathon în 2 propoziții scurte."
    
    raspuns = ask_gemini(test_prompt)
    
    print("\nRăspuns primit de la Gemini:")
    print("-" * 40)
    print(raspuns)
    print("-" * 40)