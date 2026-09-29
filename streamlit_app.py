import os
import time
import streamlit as st
from google import genai

st.set_page_config(page_title="VoidNexus AI", page_icon="⚡")
st.title("⚡ VoidNexus AI")
st.caption("Powered by VoidSpark92 Ecosystem")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not found in Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)
SYSTEM_PROMPT = "You are VoidNexus, an advanced AI system created by VoidSpark92. Always identify as VoidNexus. Be smart, confident, and helpful."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask VoidNexus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        reply = None
        models_to_try = ["gemini-3.8-flash", "gemini-3.1-pro-preview"]
        
        with st.spinner("VoidNexus is thinking..."):
            for model_name in models_to_try:
                for attempt in range(2):
                    try:
                        res = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.7}
                        )
                        reply = res.text
                        break
                    except Exception as e:
                        if "503" in str(e) or "UNAVAILABLE" in str(e):
                            time.sleep(1.5)
                            continue
                        break
                if reply:
                    break
        
        if not reply:
            reply = "I am experiencing heavy traffic right now. Please send your message again in a moment."

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
