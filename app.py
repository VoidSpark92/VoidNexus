import os
from google import genai

client = genai.Client()

def ask_void_nexus(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    print("--- VoidNexus AI System Online ---")
    user_query = input("Ask VoidNexus: ")
    reply = ask_void_nexus(user_query)
    print(f"\nVoidNexus: {reply}")
