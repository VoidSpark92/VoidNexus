import os
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

SYSTEM_PROMPT = "You are VoidNexus, an advanced AI system created by VoidSpark92. Always identify as VoidNexus."

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
        with st.spinner("VoidNexus is thinking..."):
            reply = None
            last_err = None

            # Fetch active text models automatically from your account
            try:
                available_models = [
                    m.name for m in client.models.list()
                    if "generateContent" in (m.supported_actions or [])
                ]
            except Exception:
                available_models = ["gemini-3.8-flash", "gemini-3.1-pro-preview"]

            # Try available models until one responds
            for model_name in available_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
                    )
                    if response.text:
                        reply = response.text
                        break
                except Exception as e:
                    last_err = e
                    continue

            if not reply:
                reply = f"Error reaching AI engine: {last_err}"

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
