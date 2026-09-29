import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SVG logo injected directly
LOGO_SVG = """
<svg width="28" height="28" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="neonGlowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="50%" stop-color="#6366F1" />
      <stop offset="100%" stop-color="#EC4899" />
    </linearGradient>
    <linearGradient id="warmFlare" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E11D48" />
      <stop offset="100%" stop-color="#F59E0B" />
    </linearGradient>
  </defs>
  <path d="M 55 70 C 72 130, 98 178, 120 190 C 142 178, 168 130, 185 70" stroke="#1D4ED8" stroke-width="18" stroke-linecap="round"/>
  <path d="M 45 110 C 35 55, 90 30, 138 48 C 188 66, 202 130, 165 174 C 140 202, 98 194, 82 160" stroke="url(#neonGlowGrad)" stroke-width="14" stroke-linecap="round"/>
  <path d="M 120 190 C 138 152, 160 110, 178 76" stroke="#E11D48" stroke-width="10" stroke-linecap="round"/>
  <path d="M 85 92 C 104 136, 116 160, 120 164 C 126 156, 142 122, 154 98" stroke="url(#warmFlare)" stroke-width="8" stroke-linecap="round"/>
  <circle cx="120" cy="116" r="7" fill="#FFFFFF"/>
</svg>
"""

# Gemini Precision Layout & Button Styling
st.markdown("""
<style>
    .stApp {
        background-color: #131314;
        color: #E3E3E3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        width: 270px !important;
    }
    /* Universal Button Resets for Clean Gemini Look */
    div[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        transition: background 0.15s ease;
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
    }
    /* New Chat Specific Button */
    div[data-testid="stSidebar"] div.new-chat-btn .stButton > button {
        background-color: #282A2C !important;
        color: #E3E3E3 !important;
        border-radius: 24px !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stSidebar"] div.new-chat-btn .stButton > button:hover {
        background-color: #3C4043 !important;
    }
    .sidebar-heading {
        font-size: 0.74rem;
        color: #8E918F;
        padding: 16px 12px 6px 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .nexus-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 0 20px 0;
    }
    .nexus-header span.title {
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
        padding: 1rem 0 !important;
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
        margin-top: 10px;
    }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "history" not in st.session_state:
    st.session_state.history = {
        "chat_1": {"title": "New Chat", "messages": []}
    }

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "chat_1"

if "active_view" not in st.session_state:
    st.session_state.active_view = "chat"

current_id = st.session_state.current_chat_id

# ----------------- SIDEBAR -----------------
with st.sidebar:
    # 1. New Chat Button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕ New Chat", key="btn_new_chat"):
        new_key = f"chat_{len(st.session_state.history) + 1}"
        st.session_state.history[new_key] = {"title": "New Chat", "messages": []}
        st.session_state.current_chat_id = new_key
        st.session_state.active_view = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Functional Navigation Buttons
    if st.button("🔍 Search chats", key="nav_search"):
        st.session_state.active_view = "search"
        st.rerun()

    if st.button("🖼️ Images", key="nav_images"):
        st.session_state.active_view = "images"
        st.rerun()

    if st.button("🎥 Videos", key="nav_videos"):
        st.session_state.active_view = "videos"
        st.rerun()

    if st.button("🗂️ Library", key="nav_library"):
        st.session_state.active_view = "library"
        st.rerun()

    # 3. Dynamic Recent History
    st.markdown('<div class="sidebar-heading">Recent</div>', unsafe_allow_html=True)
    for c_id, c_data in reversed(list(st.session_state.history.items())):
        display_title = c_data["title"]
        if st.button(f"💬 {display_title}", key=f"hist_{c_id}"):
            st.session_state.current_chat_id = c_id
            st.session_state.active_view = "chat"
            st.rerun()

    # 4. User Profile Section
    st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-top: 1px solid #282A2C;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #2563EB; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold; color: white;">VS</div>
            <div>
                <div style="font-size: 0.86rem; font-weight: 500; color: #E3E3E3;">VoidSpark92</div>
                <div style="font-size: 0.72rem; color: #8E918F;">Architect</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN INTERFACE -----------------
# Header with Embedded Custom Logo
st.markdown(f"""
<div class="nexus-header">
    {LOGO_SVG}
    <span class="title">VoidNexus</span>
    <span class="core-badge">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

# ACTIVE VIEW SWITCHER (Search / Images / Videos / Library / Chat)
if st.session_state.active_view == "search":
    st.subheader("🔍 Search Chats")
    q = st.text_input("Search conversation records...")
    if q:
        matches = [c for c in st.session_state.history.values() if q.lower() in c['title'].lower()]
        for m in matches:
            st.write(f"• {m['title']}")
    if st.button("← Back to Chat"):
        st.session_state.active_view = "chat"
        st.rerun()

elif st.session_state.active_view == "images":
    st.subheader("🖼️ Images Gallery")
    st.info("No generated images yet in this session.")
    if st.button("← Back to Chat"):
        st.session_state.active_view = "chat"
        st.rerun()

elif st.session_state.active_view == "videos":
    st.subheader("🎥 Video Studio")
    st.info("Video processing module is idle.")
    if st.button("← Back to Chat"):
        st.session_state.active_view = "chat"
        st.rerun()

elif st.session_state.active_view == "library":
    st.subheader("🗂️ Library")
    st.write(f"Total Conversations Saved: **{len(st.session_state.history)}**")
    for key, item in st.session_state.history.items():
        st.text(f"- {item['title']} ({len(item['messages'])} messages)")
    if st.button("← Back to Chat"):
        st.session_state.active_view = "chat"
        st.rerun()

else:
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

    # Active Conversation Messages
    messages = st.session_state.history[current_id]["messages"]
    for msg in messages:
        avatar = "👤" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask VoidNexus"):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # First message sets the conversation title in Recents
        if len(messages) == 1:
            title = prompt[:24] + "..." if len(prompt) > 24 else prompt
            st.session_state.history[current_id]["title"] = title

        with st.chat_message("assistant", avatar="💠"):
            with st.spinner("VoidNexus is thinking..."):
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
            messages.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown('<div class="gemini-disclaimer">VoidNexus can make mistakes. Verify important info.</div>', unsafe_allow_html=True)
