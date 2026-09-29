import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai

# Page Config
st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Wider Sidebar & Bigger Typography CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background-color: #131314 !important;
        color: #E3E3E3;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* 1. Force Wider Sidebar (320px) */
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        min-width: 320px !important;
        max-width: 320px !important;
        width: 320px !important;
        padding-top: 1.2rem !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 320px !important;
        padding: 1.2rem 1rem !important;
    }

    /* 2. Bigger Sidebar Action Buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 12px 18px !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        gap: 12px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s cubic-bezier(0.2, 0, 0, 1) !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
        transform: translateX(4px);
    }

    /* 3. High-Contrast Bold "New Chat" Button */
    div[data-testid="stSidebar"] div.new-chat-container .stButton > button {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
        border-radius: 28px !important;
        padding: 14px 22px !important;
        font-size: 1.12rem !important;
        font-weight: 600 !important;
        border: 1px solid #3C4043 !important;
        margin-bottom: 22px !important;
    }

    div[data-testid="stSidebar"] div.new-chat-container .stButton > button:hover {
        background-color: #37393B !important;
        border-color: #8AB4F8 !important;
        transform: none !important;
    }

    /* 4. Readable Section Headings */
    .sidebar-section-title {
        font-size: 0.82rem;
        color: #8E918F;
        padding: 22px 16px 10px 16px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* 5. Header Navbar Styling */
    .top-navbar {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 0.8rem 0 1.8rem 0;
    }

    .top-navbar .app-name {
        font-size: 1.6rem;
        font-weight: 600;
        color: #E3E3E3;
    }

    .core-pill {
        font-size: 0.82rem;
        font-weight: 600;
        background: #1E1F20;
        border: 1px solid #3C4043;
        color: #8AB4F8;
        padding: 4px 12px;
        border-radius: 8px;
    }

    /* Chat Messages Typography */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.2rem 0 !important;
        font-size: 1.05rem !important;
    }

    /* Chat Input Bar */
    div[data-testid="stChatInput"] {
        background-color: #1E1F20 !important;
        border-radius: 32px !important;
        border: 1px solid #3C4043 !important;
        box-shadow: 0 4px 28px rgba(0, 0, 0, 0.4) !important;
        padding: 6px 12px !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #8AB4F8 !important;
    }

    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# JS: Force Sidebar Width, Padding and Micro-Animations
components.html("""
<script>
    const setupSidebar = () => {
        const doc = window.parent.document;
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.width = '320px';
            sidebar.style.minWidth = '320px';
            sidebar.style.transition = 'width 0.3s ease';
        }
    };
    setInterval(setupSidebar, 500);
</script>
""", height=0, width=0)

# Embedded Crisp Curved Multi-Color SVG Logo
LOGO_SVG = """
<svg width="34" height="34" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="neonGlowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="45%" stop-color="#4F46E5" />
      <stop offset="75%" stop-color="#9333EA" />
      <stop offset="100%" stop-color="#FF007A" />
    </linearGradient>
    <linearGradient id="crimsonFlame" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FF1744" />
      <stop offset="60%" stop-color="#FF9100" />
      <stop offset="100%" stop-color="#FFEA00" />
    </linearGradient>
  </defs>
  <path d="M 52 70 C 72 135, 98 180, 120 192 C 142 180, 168 135, 188 70" stroke="#1D4ED8" stroke-width="16" stroke-linecap="round"/>
  <path d="M 44 112 C 34 54, 92 28, 140 46 C 190 64, 204 132, 166 176 C 140 205, 96 195, 80 160" stroke="url(#neonGlowGrad)" stroke-width="13" stroke-linecap="round"/>
  <path d="M 120 192 C 138 152, 162 108, 180 74" stroke="#E11D48" stroke-width="10" stroke-linecap="round"/>
  <path d="M 84 90 C 104 138, 116 162, 120 166 C 126 158, 142 122, 156 96" stroke="url(#crimsonFlame)" stroke-width="8" stroke-linecap="round"/>
  <circle cx="120" cy="116" r="6" fill="#FFFFFF"/>
</svg>
"""

# Read local logo.svg if exists
if os.path.exists("logo.svg"):
    try:
        with open("logo.svg", "r") as f:
            LOGO_MARK = f.read()
    except Exception:
        LOGO_MARK = LOGO_SVG
else:
    LOGO_MARK = LOGO_SVG

# ----------------- STATE -----------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Default Session": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Default Session"

if "view" not in st.session_state:
    st.session_state.view = "chat"

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
    if st.button("➕  New Chat", key="btn_new_chat"):
        new_name = f"Session {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        st.session_state.view = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍   Search chats", key="btn_search"):
        st.session_state.view = "search"
        st.rerun()

    if st.button("🖼️   Images", key="btn_images"):
        st.session_state.view = "images"
        st.rerun()

    if st.button("🎥   Videos", key="btn_videos"):
        st.session_state.view = "videos"
        st.rerun()

    if st.button("🗂️   Library", key="btn_library"):
        st.session_state.view = "library"
        st.rerun()

    st.markdown('<div class="sidebar-section-title">Recent Conversations</div>', unsafe_allow_html=True)
    for c_name in reversed(list(st.session_state.chats.keys())):
        bullet = "● " if c_name == st.session_state.current_chat else "💬 "
        if st.button(f"{bullet}  {c_name}", key=f"rec_{c_name}"):
            st.session_state.current_chat = c_name
            st.session_state.view = "chat"
            st.rerun()

    # User Profile Pill
    st.markdown("<div style='height: 14vh;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; padding:12px 14px; border-top:1px solid #282A2C; background-color: #171819; border-radius: 12px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#2563EB; display:flex; align-items:center; justify-content:center; font-size:0.9rem; font-weight:bold; color:white;">VS</div>
            <div>
                <div style="font-size:0.95rem; font-weight:600; color:#E3E3E3;">VoidSpark92</div>
                <div style="font-size:0.75rem; color:#8E918F;">Architect</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN AREA -----------------
st.markdown(f"""
<div class="top-navbar">
    <div style="width:34px; height:34px; display:flex; align-items:center;">{LOGO_MARK}</div>
    <span class="app-name">VoidNexus</span>
    <span class="core-pill">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.view == "search":
    st.subheader("🔍 Search Chats")
    query = st.text_input("Search through conversation history...", placeholder="Type title to search...")
    if query:
        matches = [name for name in st.session_state.chats.keys() if query.lower() in name.lower()]
        for m in matches:
            if st.button(f"Open: {m}", key=f"q_{m}"):
                st.session_state.current_chat = m
                st.session_state.view = "chat"
                st.rerun()
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "images":
    st.subheader("🖼️ Images Gallery")
    st.info("No generated media in active workspace.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "videos":
    st.subheader("🎥 Video Studio")
    st.info("Video pipeline is standing by.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "library":
    st.subheader("🗂️ Library")
    st.write(f"Total Conversations: **{len(st.session_state.chats)}**")
    for name, messages in st.session_state.chats.items():
        st.write(f"• **{name}** — {len(messages)} messages")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

else:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing in Secrets.")
        st.stop()

    client = genai.Client(api_key=api_key)
    SYSTEM_PROMPT = (
        "You are VoidNexus, an advanced AI system created exclusively by VoidSpark92. "
        "Always identify as VoidNexus. Speak with clarity, insight, and sharp intelligence."
    )

    curr_chat = st.session_state.current_chat
    chat_history = st.session_state.chats[curr_chat]

    for msg in chat_history:
        avatar = "👤" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask VoidNexus..."):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Dynamic Auto Title Rename
        if len(chat_history) == 1:
            clean_title = prompt[:24] + "..." if len(prompt) > 24 else prompt
            st.session_state.chats[clean_title] = st.session_state.chats.pop(curr_chat)
            st.session_state.current_chat = clean_title
            chat_history = st.session_state.chats[clean_title]

        with st.chat_message("assistant", avatar="💠"):
            with st.spinner("VoidNexus is thinking..."):
                reply = None
                try:
                    models = [m.name for m in client.models.list() if "generateContent" in (m.supported_actions or [])]
                except Exception:
                    models = ["gemini-3.8-flash", "gemini-3.1-pro-preview"]

                for m in models:
                    try:
                        res = client.models.generate_content(
                            model=m,
                            contents=f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
                        )
                        if res.text:
                            reply = res.text
                            break
                    except Exception:
                        continue

                if not reply:
                    reply = "System busy, please try again."

            st.markdown(reply)
            chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown("<p style='text-align:center; font-size:0.8rem; color:#8E918F; margin-top:24px;'>VoidNexus can make mistakes. Verify important info.</p>", unsafe_allow_html=True)
