import os
from google import genai

client = genai.Client()

def ask_void_nexus(prompt: str) -> str:
    # Pehle 3.8-flash try karega, busy hone par standard model pe switch hoga
    models_to_try = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return f"[{model_name}] {response.text}"
        except Exception as e:
            last_error = e
            continue
            
    raise last_error

if __name__ == "__main__":
    print("--- VoidNexus AI System Online ---")
    user_query = input("Ask VoidNexus: ")
    reply = ask_void_nexus(user_query)
    print(f"\nVoidNexus: {reply}")
