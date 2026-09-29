import os
import time
from google import genai

client = genai.Client()

SYSTEM_PROMPT = """You are VoidNexus, an advanced AI system created by VoidSpark92. 
You are part of the VoidSpark92 ecosystem alongside VoidVisuals. 
Always identify yourself as VoidNexus. Be confident, precise, and tech-savvy."""

def ask_void_nexus(prompt: str) -> str:
    # 2026 ke recommended models
    models = ["gemini-3.8-flash", "gemini-3.1-pro-preview"]
    
    for model_name in models:
        for attempt in range(3):  # Spike demand aane par 3 baar retry karega
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "temperature": 0.7,
                    }
                )
                return response.text
            except Exception as e:
                err_str = str(e)
                # Agar busy/demand spike ho, 2 sec wait karke retry
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    time.sleep(2)
                    continue
                # Agar 404 ho toh direct agla model try karega
                break

    return "VoidNexus is currently recalibrating systems. Please try again shortly."

if __name__ == "__main__":
    print("--- VoidNexus AI System Online ---")
    user_query = input("Ask VoidNexus: ")
    reply = ask_void_nexus(user_query)
    print(f"\nVoidNexus: {reply}")
