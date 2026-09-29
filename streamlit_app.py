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

# Dark Theme CSS (No mock chats, exact user history mapping)
st.markdown("""
<style>
    .stApp {
        background-color: #131314;
        color: #E3E3E3;
        font-family: "Google Sans", -apple-system, BlinkMacSystemFont, sans-serif;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        width: 260px !important;
    }
    /* New Chat button overrides standard look */
    .stButton > button {
        width: 100% !important;
        background-color: #282A2C !important;
        color: #E3E3E3 !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 500 !important;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #3C4043 !important;
    }
    /* Recent Dynamic Links */
    .sidebar-heading {
        font-size: 0.75rem;
        color: #8E918F;
        padding: 16px 12px 6px 12px;
        font-weight: 600;
    }
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
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.2rem 0 !important;
        border: none !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #1E1F20 !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    .gemini-disclaimer {
        text-align: center;
        font-size: 0.75rem;
        color: #8E918F;
        margin-top: 8px;
    }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
# History structure: { "chat_id": { "title": str, "messages": list } }
if "history" not in st.session_state:
    st.session_state.history = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Default Chat"
    st.session_state.history["Default Chat"] = {"title": "Default Chat", "messages": []}

# Active chats reference
current_id = st.session_state.current_chat_id

# ----------------- SIDEBAR -----------------
with st.sidebar:
    # New chat triggers state shift
    if st.button("✏️ New chat"):
        new_id = f"Chat {len(st.session_state.history) + 1}"
        st.session_state.history[new_id] = {"title": new_id, "messages": []}
        st.session_state.current_chat_id = new_id
        st.rerun()

    # App links
    st.markdown("""
        <div style="color: #C4C7C5; font-size: 0.88rem; padding: 10px 12px; display: flex; flex-direction: column; gap: 12px;">
            <div>🔍 Search chats</div>
            <div>🖼️ Images</div>
            <div>🎥 Videos</div>
            <div>🗂️ Library</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-heading">Recent</div>', unsafe_allow_html=True)
    
    # Active Dynamic Chat Switcher
    for chat_id, chat_data in list(st.session_state.history.items()):
        # Show recent title based on user first message
        title = chat_data["title"]
        if st.button(f"💬 {title}", key=f"btn_{chat_id}"):
            st.session_state.current_chat_id = chat_id
            st.rerun()
            
    st.markdown("<div style='height: 25vh;'></div>", unsafe_allow_html=True)
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

# Display Messages from Current Chat
active_messages = st.session_state.history[current_id]["messages"]
for msg in active_messages:
    avatar = "👤" if msg["role"] == "user" else "💠"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Bottom Input & Disclaimer
if prompt := st.chat_input("Ask VoidNexus"):
    # Add user message to state
    active_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Automatically rename chat history on the first message
    if len(active_messages) == 1:
        truncated_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        st.session_state.history[current_id]["title"] = truncated_title

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
        active_messages.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown('<div class="gemini-disclaimer">VoidNexus can make mistakes. Verify important info.</div>', unsafe_allow_html=True)
