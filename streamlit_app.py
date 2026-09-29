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
            try:
                # System prompt ko direct user message ke context me attach kiya
                full_prompt = (
                    "System instruction: You are VoidNexus, created by VoidSpark92. "
                    "Always identify as VoidNexus.\n\n"
                    f"User: {prompt}"
                )
                
                # Standard auto-routed model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt,
                )
                reply = response.text
            except Exception as e:
                reply = f"System Report: {e}"

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
