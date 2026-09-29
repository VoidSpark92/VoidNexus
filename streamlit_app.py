import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai

# Page Config with SVG Favicon
st.set_page_config(
    page_title="VoidNexus",
    page_icon="logo.svg" if os.path.exists("logo.svg") else "💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Gemini Architecture CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background-color: #131314 !important;
        color: #E3E3E3;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Modern Gemini Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        padding-top: 1rem !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem !important;
    }

    /* Reset All Sidebar Buttons to Ultra-Clean Nav Items */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 9px 14px !important;
        border-radius: 20px !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        transition: all 0.2s cubic-bezier(0.2, 0, 0, 1) !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
        transform: translateX(3px);
    }

    /* Primary "New Chat" Pill Button */
    div[data-testid="stSidebar"] div.new-chat-container .stButton > button {
        background-color: #282A2C !important;
        color: #E3E3E3 !important;
        border-radius: 24px !important;
        padding: 11px 18px !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        margin-bottom: 12px !important;
        border: 1px solid #3C4043 !important;
    }

    div[data-testid="stSidebar"] div.new-chat-container .stButton > button:hover {
        background-color: #37393B !important;
        color: #FFFFFF !important;
        border-color: #5E6368 !important;
        transform: none !important;
    }

    /* Sidebar Headings */
    .sidebar-section-title {
        font-size: 0.72rem;
        color: #8E918F;
        padding: 18px 14px 6px 14px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    /* Top App Bar Header */
    .top-navbar {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.4rem 0 1.6rem 0;
    }

    .top-navbar .app-name {
        font-size: 1.32rem;
        font-weight: 500;
        letter-spacing: -0.01em;
        color: #E3E3E3;
    }

    .core-pill {
        font-size: 0.72rem;
        font-weight: 500;
        background: #1E1F20;
        border: 1px solid #3C4043;
        color: #8AB4F8;
        padding: 3px 9px;
        border-radius: 6px;
    }

    /* Chat Messages */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.1rem 0 !important;
    }

    /* Sleek Gemini Bottom Pill */
    div[data-testid="stChatInput"] {
        background-color: #1E1F20 !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
        transition: border-color 0.2s;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #8AB4F8 !important;
    }

    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# JS Enhancer for Dynamic Micro-Interactions
components.html("""
<script>
    const adjustSidebar = () => {
        const sidebar = window.parent.document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.scrollbarWidth = 'none';
        }
    };
    setTimeout(adjustSidebar, 300);
</script>
""", height=0, width=0)

# Embedded SVG fallback if file not read directly
SVG_RAW = """
<svg width="26" height="26" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="neonGlowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="40%" stop-color="#4F46E5" />
      <stop offset="75%" stop-color="#9333EA" />
      <stop offset="100%" stop-color="#FF007A" />
    </linearGradient>
    <linearGradient id="crimsonFlame" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FF1744" />
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

# Read logo.svg if exists
if os.path.exists("logo.svg"):
    with open("logo.svg", "r") as f:
        LOGO_MARK = f.read()
else:
    LOGO_MARK = SVG_RAW

# ----------------- SESSION STATE -----------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "view" not in st.session_state:
    st.session_state.view = "chat"

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
    if st.button("➕ New Chat", key="btn_new_chat"):
        new_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        st.session_state.view = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍  Search chats", key="btn_search"):
        st.session_state.view = "search"
        st.rerun()

    if st.button("🖼️  Images", key="btn_images"):
        st.session_state.view = "images"
        st.rerun()

    if st.button("🎥  Videos", key="btn_videos"):
        st.session_state.view = "videos"
        st.rerun()

    if st.button("🗂️  Library", key="btn_library"):
        st.session_state.view = "library"
        st.rerun()

    st.markdown('<div class="sidebar-section-title">Recent</div>', unsafe_allow_html=True)
    for c_name in reversed(list(st.session_state.chats.keys())):
        active_prefix = "● " if c_name == st.session_state.current_chat else "💬 "
        if st.button(f"{active_prefix}{c_name}", key=f"rec_{c_name}"):
            st.session_state.current_chat = c_name
            st.session_state.view = "chat"
            st.rerun()

    # User Profile Pill at Bottom
    st.markdown("<div style='height: 22vh;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; padding:10px 12px; border-top:1px solid #282A2C;">
            <div style="width:30px; height:30px; border-radius:50%; background:#2563EB; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:bold; color:white;">VS</div>
            <div>
                <div style="font-size:0.85rem; font-weight:500; color:#E3E3E3;">VoidSpark92</div>
                <div style="font-size:0.7rem; color:#8E918F;">Architect</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN VIEW -----------------
# Header with Dynamic SVG Logo
st.markdown(f"""
<div class="top-navbar">
    <div style="width:26px; height:26px; display:flex; align-items:center;">{LOGO_MARK}</div>
    <span class="app-name">VoidNexus</span>
    <span class="core-pill">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.view == "search":
    st.subheader("🔍 Search Chats")
    query = st.text_input("Search through conversation history...", placeholder="Type to filter...")
    if query:
        results = [name for name in st.session_state.chats.keys() if query.lower() in name.lower()]
        for res in results:
            if st.button(f"Go to {res}", key=f"search_res_{res}"):
                st.session_state.current_chat = res
                st.session_state.view = "chat"
                st.rerun()
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "images":
    st.subheader("🖼️ Images")
    st.info("Visual generation module idle.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "videos":
    st.subheader("🎥 Videos")
    st.info("Video processing studio idle.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "library":
    st.subheader("🗂️ Library")
    st.write(f"Total Chats: **{len(st.session_state.chats)}**")
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

    if prompt := st.chat_input("Ask VoidNexus"):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Set title from first user prompt
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

st.markdown("<p style='text-align:center; font-size:0.75rem; color:#8E918F; margin-top:20px;'>VoidNexus can make mistakes. Verify important info.</p>", unsafe_allow_html=True)
