import os
import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Exact Gemini Theme CSS
st.markdown("""
<style>
    /* Gemini Dark Canvas */
    .stApp {
        background-color: #131314;
        color: #E3E3E3;
        font-family: "Google Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Top Default Streamlit Bar Cleanup */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Left Sidebar: Exact dark panel */
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        width: 260px !important;
    }

    /* Sidebar buttons & text */
    .sidebar-btn {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 20px;
        background-color: #282A2C;
        color: #E3E3E3;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        margin-bottom: 20px;
        border: none;
    }
    
    .sidebar-nav-item {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 12px;
        color: #C4C7C5;
        font-size: 0.88rem;
        border-radius: 8px;
        margin-bottom: 4px;
    }
    
    .sidebar-heading {
        font-size: 0.75rem;
        color: #8E918F;
        padding: 16px 12px 6px 12px;
        font-weight: 600;
    }

    /* Gemini Minimal Top Header */
    .gemini-top-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0 24px 0;
    }
    .gemini-top-header span.title {
        font-size: 1.35rem;
        font-weight: 500;
        color: #E3E3E3;
    }
    .core-badge {
        font-size: 0.72rem;
        background: #1E1F20;
        border: 1px solid #3C4043;
        color: #8AB4F8;
        padding: 2px 8px;
        border-radius: 6px;
    }

    /* Gemini Typography (No bulky boxes) */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.2rem 0 !important;
        border: none !important;
    }

    /* Rounded Pill Input Box like Gemini */
    div[data-testid="stChatInput"] {
        background-color: #1E1F20 !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        padding: 4px 8px !important;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: #8AB4F8 !important;
    }

    /* Gemini Disclaimer footer text */
    .gemini-disclaimer {
        text-align: center;
        font-size: 0.75rem;
        color: #8E918F;
        margin-top: 8px;
    }

    /* Hide standard UI watermarks */
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR (Matches your screenshot) -----------------
with st.sidebar:
    st.markdown('<div class="sidebar-btn">✏️ New chat</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="sidebar-nav-item">🔍 Search chats</div>
        <div class="sidebar-nav-item">🖼️ Images</div>
        <div class="sidebar-nav-item">🎥 Videos</div>
        <div class="sidebar-nav-item">🗂️ Library</div>
        
        <div class="sidebar-heading">Recent</div>
        <div class="sidebar-nav-item">💬 GitHub Par AI Project Guide</div>
        <div class="sidebar-nav-item">💬 VoidNexus Architecture</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 35vh;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-top: 1px solid #282A2C;">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: #4F46E5; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: bold;">VS</div>
            <div>
                <div style="font-size: 0.85rem; font-weight: 500; color: #E3E3E3;">VoidSpark92</div>
                <div style="font-size: 0.7rem; color: #8E918F;">Architect</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN INTERFACE -----------------
st.markdown("""
<div class="gemini-top-header">
    <span style="font-size: 1.4rem;">💠</span>
    <span class="title">VoidNexus</span>
    <span class="core-badge">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

# API Setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key missing in Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)
SYSTEM_PROMPT = (
    "You are VoidNexus, an advanced AI system created exclusively by VoidSpark92. "
    "Always identify as VoidNexus. Speak with clarity, insight, and sharp intelligence."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Messages feed
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "💠"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Bottom Input & Disclaimer
if prompt := st.chat_input("Ask VoidNexus"):
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
                reply = "System busy. Please try again shortly."

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown('<div class="gemini-disclaimer">VoidNexus can make mistakes. Verify important info.</div>', unsafe_allow_html=True)

            if not reply:
                reply = "Unable to process request right now. Please try again."

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
