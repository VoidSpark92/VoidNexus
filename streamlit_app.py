import os
import streamlit as st
from google import genai

st.set_page_config(page_title="VoidNexus AI", page_icon="⚡")
st.title("⚡ VoidNexus AI")
st.caption("Powered by VoidSpark92 Ecosystem")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not found.")
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
        try:
            res = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={"system_instruction": SYSTEM_PROMPT}
            )
            reply = res.text
        except Exception as e:
            reply = f"Error: {e}"
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
