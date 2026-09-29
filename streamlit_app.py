import os
import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gemini-like Minimal Dark CSS (No extra sparks, clean typography)
st.markdown("""
<style>
    /* Dark Slate Background */
    .stApp {
        background-color: #131314;
        color: #E3E3E3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Top Bar cleanup */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Centered Minimal Header */
    .nexus-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-top: 10px;
        margin-bottom: 2rem;
    }
    .nexus-title {
        font-size: 1.5rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        color: #E3E3E3;
    }
    .nexus-badge {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 6px;
        background: #1E1F20;
        color: #8AB4F8;
        border: 1px solid #3c4043;
    }

    /* Clean Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.25rem 0.5rem;
    }
    
    /* User Message Container */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background-color: #1E1F20 !important;
        border-radius: 18px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }

    /* Chat input styling */
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #1E1F20 !important;
        border: 1px solid #3c4043 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: #8AB4F8 !important;
    }

    /* Hide standard Streamlit footer & menu */
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Top Bar Layout
st.markdown("""
<div class="nexus-header">
    <span style="font-size: 1.6rem;">💠</span>
    <span class="nexus-title">VoidNexus</span>
    <span class="nexus-badge">VoidVisuals Core</span>
</div>
""", unsafe_allow_html=True)

# API Setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not found in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)
SYSTEM_PROMPT = (
    "You are VoidNexus, a precise, helpful, and intelligent AI companion created by VoidSpark92. "
    "Always identify as VoidNexus. Maintain an insightful, concise, and professional tone."
)

# Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    role = msg["role"]
    avatar = "👤" if role == "user" else "💠"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Message VoidNexus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💠"):
        with st.spinner(""):
            reply = None
            try:
                available_models = [
                    m.name for m in client.models.list()
                    if "generateContent" in (m.supported_actions or [])
                ]
            except Exception:
                available_models = ["gemini-3.8-flash", "gemini-3.1-pro-preview"]

            for model_name in available_models:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
                    )
                    if response.text:
                        reply = response.text
                        break
                except Exception:
                    continue

            if not reply:
                reply = "Unable to process request right now. Please try again."

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
