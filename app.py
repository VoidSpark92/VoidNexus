import os
from google import genai
from google.genai import types

client = genai.Client()

# VoidNexus Custom Personality
SYSTEM_PROMPT = """
You are VoidNexus, an advanced and intelligent AI system created by VoidSpark92.
You are part of the VoidSpark92 ecosystem alongside VoidVisuals.
Always identify yourself as VoidNexus. Be confident, precise, and tech-savvy.
"""

def ask_void_nexus(prompt: str) -> str:
    models_to_try = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                ),
            )
            return response.text
        except Exception as e:
            last_error = e
            continue
            
    raise last_error

if __name__ == "__main__":
    print("--- VoidNexus AI System Online ---")
    user_query = input("Ask VoidNexus: ")
    reply = ask_void_nexus(user_query)
    print(f"\nVoidNexus: {reply}")
