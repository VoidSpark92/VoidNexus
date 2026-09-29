import os
import streamlit as st
from google import genai

# Page Config (Gemini Dark Theme)
st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Strict One-Page View Layout CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background-color: #131314 !important;
        color: #E3E3E3;
        overflow: hidden !important; /* Forces scrollbars out of the system */
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Standard Wider Sidebar Layout */
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        min-width: 320px !important;
        max-width: 320px !important;
        width: 320px !important;
        padding-top: 1rem !important;
        overflow: hidden !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        width: 320px !important;
        padding: 1rem 1rem !important;
        height: 100vh !important;
        position: relative !important;
    }

    /* Text & Icon Rescaling */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 12px 18px !important;
        border-radius: 12px !important;
        font-size: 1.12rem !important; /* Up-scaled Font Size */
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        gap: 14px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s cubic-bezier(0.2, 0, 0, 1) !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
    }

    /* "New Chat" Action Button CSS */
    div[data-testid="stSidebar"] div.new-chat-container .stButton > button {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
        border-radius: 28px !important;
        padding: 14px 22px !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        border: 1px solid #3C4043 !important;
        margin-bottom: 24px !important;
    }

    div[data-testid="stSidebar"] div.new-chat-container .stButton > button:hover {
        background-color: #37393B !important;
        border-color: #8AB4F8 !important;
    }

    /* User Profile Locking at bottom - Resolves Scroll Overlap Issue */
    .user-footer {
        position: absolute;
        bottom: 22px;
        left: 12px;
        width: 296px;
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px;
        border-top: 1px solid #282A2C;
        background-color: #171819;
        border-radius: 14px;
    }

    .user-footer .avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #2563EB;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        font-weight: bold;
        color: white;
    }

    .user-footer .info-wrap {
        display: flex;
        flex-direction: column;
    }

    .user-footer .user-name {
        font-size: 1rem;
        font-weight: 600;
        color: #E3E3E3;
    }

    .user-footer .role {
        font-size: 0.8rem;
        color: #8E918F;
    }

    .sidebar-section-title {
        font-size: 0.86rem;
        color: #8E918F;
        padding: 24px 16px 12px 16px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Main Area Headers */
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

    /* Form and Layout alignment to standard web proportions */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.2rem 0 !important;
        font-size: 1.1rem !important;
    }

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

# Smooth Gradient Embedded SVG logo.svg Content
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

# Fetch the active Logo Mark
if os.path.exists("logo.svg"):
    try:
        with open("logo.svg", "r") as f:
            LOGO_MARK = f.read()
    except Exception:
        LOGO_MARK = LOGO_SVG
else:
    LOGO_MARK = LOGO_SVG

# ----------------- SESSION STATE -----------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "view" not in st.session_state:
    st.session_state.view = "chat"

# ----------------- SIDEBAR -----------------
with st.sidebar:
    # 1. Action Row "New Chat"
    st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
    if st.button("➕  New Chat", key="btn_new_chat"):
        new_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        st.session_state.view = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Main Large Navbar Section (Excluding 'Search' to give space)
    if st.button("🖼️   Images", key="btn_images"):
        st.session_state.view = "images"
        st.rerun()

    if st.button("🎥   Videos", key="btn_videos"):
        st.session_state.view = "videos"
        st.rerun()

    if st.button("🗂️   Library", key="btn_library"):
        st.session_state.view = "library"
        st.rerun()

    # 3. Compact Recent Chat Panel
    st.markdown('<div class="sidebar-section-title">Recent</div>', unsafe_allow_html=True)
    for c_name in list(st.session_state.chats.keys())[-3:]:  # Show only top 3 to keep zero-scroll constraints
        bullet = "● " if c_name == st.session_state.current_chat else "💬 "
        if st.button(f"{bullet}  {c_name}", key=f"rec_{c_name}"):
            st.session_state.current_chat = c_name
            st.session_state.view = "chat"
            st.rerun()

    # 4. User Profile absolute locking at the bottom
    st.markdown("""
        <div class="user-footer">
            <div class="avatar">VS</div>
            <div class="info-wrap">
                <span class="user-name">VoidSpark92</span>
                <span class="role">Architect</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN VIEW -----------------
st.markdown(f"""
<div class="top-navbar">
    <div style="width:34px; height:34px; display:flex; align-items:center;">{LOGO_MARK}</div>
    <span class="app-name">VoidNexus</span>
    <span class="core-pill">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

# Application state-handlers
if st.session_state.view == "images":
    st.subheader("🖼️ Images Gallery")
    st.info("Visual media indexing module is standby.")
    if st.button("← Back to Chat", key="btn_b_images"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "videos":
    st.subheader("🎥 Video Studio")
    st.info("Video streaming and processing pipeline idle.")
    if st.button("← Back to Chat", key="btn_b_videos"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "library":
    st.subheader("🗂️ Library")
    st.write(f"Active conversations inside workspace: **{len(st.session_state.chats)}**")
    for name, messages in st.session_state.chats.items():
        st.write(f"• **{name}** — {len(messages)} messages")
    if st.button("← Back to Chat", key="btn_b_library"):
        st.session_state.view = "chat"
        st.rerun()

else:
    # API Handshakes
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing in Secrets.")
        st.stop()

    client = genai.Client(api_key=api_key)
    SYSTEM_PROMPT = (
        "You are VoidNexus, an advanced AI system created exclusively by VoidSpark92. "
        "Always identify as VoidNexus. Maintain an insightful, concise, and professional tone."
    )

    curr_chat = st.session_state.current_chat
    chat_history = st.session_state.chats[curr_chat]

    # Chat Log Window
    for msg in chat_history:
        avatar = "👤" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Sticky chat interface
    if prompt := st.chat_input("Ask VoidNexus..."):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Truncated renaming for fast visual processing
        if len(chat_history) == 1:
            clean_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
            st.session_state.chats[clean_title] = st.session_state.chats.pop(curr_chat)
            st.session_state.current_chat = clean_title
            chat_history = st.session_state.chats[clean_title]

        with st.chat_message("assistant", avatar="💠"):
            with st.spinner(""):
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

# Anchored footer
st.markdown("<p style='text-align:center; font-size:0.8rem; color:#8E918F; margin-top:24px;'>VoidNexus can make mistakes. Verify important info.</p>", unsafe_allow_html=True)
