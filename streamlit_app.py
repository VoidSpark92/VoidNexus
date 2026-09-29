import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean Minimal CSS
st.markdown("""
<style>
    .stApp {
        background-color: #131314;
        color: #E3E3E3;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        width: 260px !important;
    }
    /* Sidebar Buttons Clean Look */
    div[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
    }
    /* New Chat Button */
    div[data-testid="stSidebar"] div.new-chat-wrap .stButton > button {
        background-color: #282A2C !important;
        border-radius: 20px !important;
        padding: 10px 16px !important;
        margin-bottom: 12px !important;
    }
    /* Chat styling */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #1E1F20 !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
    }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "view" not in st.session_state:
    st.session_state.view = "chat"

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown('<div class="new-chat-wrap">', unsafe_allow_html=True)
    if st.button("➕ New Chat"):
        new_name = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        st.session_state.view = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Search chats"):
        st.session_state.view = "search"
        st.rerun()

    if st.button("🖼️ Images"):
        st.session_state.view = "images"
        st.rerun()

    if st.button("🎥 Videos"):
        st.session_state.view = "videos"
        st.rerun()

    if st.button("🗂️ Library"):
        st.session_state.view = "library"
        st.rerun()

    st.markdown("<p style='font-size:0.75rem; color:#8E918F; margin: 18px 0 6px 10px; font-weight:600;'>RECENT</p>", unsafe_allow_html=True)
    for c_name in list(st.session_state.chats.keys()):
        if st.button(f"💬 {c_name}", key=f"rec_{c_name}"):
            st.session_state.current_chat = c_name
            st.session_state.view = "chat"
            st.rerun()

# ----------------- MAIN AREA -----------------
# Clean Single-Line Header with inline SVG Logo
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
    <svg width="24" height="24" viewBox="0 0 240 240" fill="none">
        <path d="M55 70 C72 130, 98 178, 120 190 C142 178, 168 130, 185 70" stroke="#1D4ED8" stroke-width="18" stroke-linecap="round"/>
        <path d="M45 110 C35 55, 90 30, 138 48 C188 66, 202 130, 165 174 C140 202, 98 194, 82 160" stroke="#00F0FF" stroke-width="14" stroke-linecap="round"/>
        <path d="M120 190 C138 152, 160 110, 178 76" stroke="#E11D48" stroke-width="10" stroke-linecap="round"/>
        <circle cx="120" cy="116" r="7" fill="#FFFFFF"/>
    </svg>
    <span style="font-size:1.3rem; font-weight:600; color:#E3E3E3;">VoidNexus</span>
    <span style="font-size:0.75rem; background:#1E1F20; border:1px solid #3C4043; color:#8AB4F8; padding:2px 8px; border-radius:6px;">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

# Navigation View Handlers
if st.session_state.view == "search":
    st.subheader("🔍 Search Chats")
    st.write("Abhi koi chat search index nahi hai.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "images":
    st.subheader("🖼️ Images")
    st.info("Image generation module standby par hai.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "videos":
    st.subheader("🎥 Videos")
    st.info("Video generation module standby par hai.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "library":
    st.subheader("🗂️ Library")
    st.write(f"Total chats saved: {len(st.session_state.chats)}")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

else:
    # Chat Window
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing.")
        st.stop()

    client = genai.Client(api_key=api_key)
    curr = st.session_state.current_chat
    chat_history = st.session_state.chats[curr]

    for msg in chat_history:
        avatar = "👤" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask VoidNexus"):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)

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
                            contents=f"You are VoidNexus created by VoidSpark92. Always identify as VoidNexus.\n\nUser: {prompt}"
                        )
                        if res.text:
                            reply = res.text
                            break
                    except Exception:
                        continue

                if not reply:
                    reply = "System busy, please try again."

            st.write(reply)
            chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown("<p style='text-align:center; font-size:0.75rem; color:#8E918F; margin-top:20px;'>VoidNexus can make mistakes. Verify important info.</p>", unsafe_allow_html=True)
