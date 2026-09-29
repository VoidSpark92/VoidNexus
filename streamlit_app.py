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

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "voidadmin92")

# Fixed CSS: Font isolation taaki Streamlit ke icons par asar na pade
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #131314 !important;
        color: #E3E3E3 !important;
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Streamlit native header styling */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 1000 !important;
    }

    /* Style the sidebar toggle buttons cleanly */
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stExpandSidebarButton"] {
        color: #C4C7C5 !important;
        background-color: #1E1F20 !important;
        border: 1px solid #3C4043 !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        transition: all 0.2s !important;
    }

    button[data-testid="stSidebarCollapseButton"]:hover,
    button[data-testid="stExpandSidebarButton"]:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
        border-color: #8AB4F8 !important;
    }

    /* Sidebar Base */
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        min-width: 290px !important;
        max-width: 290px !important;
        width: 290px !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: 0.8rem 0.9rem !important;
    }

    /* Sidebar Standard Buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        font-size: 1.02rem !important;
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        gap: 12px !important;
        margin-bottom: 4px !important;
        transition: all 0.15s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #282A2C !important;
        color: #FFFFFF !important;
        transform: translateX(3px) !important;
    }

    /* "New Chat" Pill Button */
    div[data-testid="stSidebar"] div.new-chat-wrapper .stButton > button {
        background-color: #282A2C !important;
        color: #E3E3E3 !important;
        border-radius: 24px !important;
        padding: 12px 20px !important;
        font-size: 1.08rem !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
        border: 1px solid #3C4043 !important;
    }

    div[data-testid="stSidebar"] div.new-chat-wrapper .stButton > button:hover {
        background-color: #37393B !important;
        color: #FFFFFF !important;
        border-color: #5E6368 !important;
        transform: none !important;
    }

    .sidebar-label {
        font-size: 0.78rem;
        color: #8E918F;
        padding: 14px 12px 6px 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Profile Card with Zero Overlap */
    .profile-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        border-top: 1px solid #282A2C;
        background-color: #171819;
        border-radius: 14px;
        margin-top: 15px;
        margin-bottom: 10px;
        width: 100%;
        box-sizing: border-box;
    }

    .profile-card .avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        font-weight: 700;
        color: #FFFFFF;
        flex-shrink: 0;
    }

    .profile-card .info {
        display: flex;
        flex-direction: column;
    }

    .profile-card .name {
        font-size: 0.98rem;
        font-weight: 600;
        color: #E3E3E3;
        line-height: 1.2;
    }

    .profile-card .designation {
        font-size: 0.76rem;
        margin-top: 2px;
    }

    /* Top Brand Bar */
    .brand-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 0 16px 0;
    }

    .brand-title {
        font-size: 1.55rem;
        font-weight: 600;
        color: #E3E3E3;
    }

    .brand-tag {
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #1E1F20;
        border: 1px solid #3C4043;
        color: #8AB4F8;
        padding: 3px 10px;
        border-radius: 6px;
    }

    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.2rem 0 !important;
        font-size: 1.12rem !important;
        line-height: 1.6 !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #1E1F20 !important;
        border-radius: 28px !important;
        border: 1px solid #3C4043 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
        padding: 4px 8px !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #8AB4F8 !important;
    }

    .disclaimer-text {
        text-align: center;
        font-size: 0.78rem;
        color: #8E918F;
        margin-top: 14px;
    }

    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "show_admin_box" not in st.session_state:
    st.session_state.show_admin_box = False

if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": [
            {"role": "assistant", "content": "Welcome to VoidNexus. How can I assist you today?"}
        ]
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "view" not in st.session_state:
    st.session_state.view = "chat"

curr_id = st.session_state.current_chat

# ----------------- SIDEBAR -----------------
with st.sidebar:
    # 1. New Chat
    st.markdown('<div class="new-chat-wrapper">', unsafe_allow_html=True)
    if st.button("➕ New Chat", key="btn_new"):
        chat_index = len(st.session_state.chats) + 1
        new_key = f"Chat {chat_index}"
        st.session_state.chats[new_key] = []
        st.session_state.current_chat = new_key
        st.session_state.view = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Clean Navigation Buttons
    if st.button("🖼️ Images", key="nav_img"):
        st.session_state.view = "images"
        st.rerun()

    if st.button("🎥 Videos", key="nav_vid"):
        st.session_state.view = "videos"
        st.rerun()

    if st.button("📁 Library", key="nav_lib"):
        st.session_state.view = "library"
        st.rerun()

    # 3. Dynamic Recent History
    st.markdown('<div class="sidebar-label">Recent</div>', unsafe_allow_html=True)
    for c_name in list(st.session_state.chats.keys())[-4:]:
        icon = "●" if c_name == curr_id else "💬"
        if st.button(f"{icon}  {c_name}", key=f"hist_{c_name}"):
            st.session_state.current_chat = c_name
            st.session_state.view = "chat"
            st.rerun()

    st.markdown("<div style='min-height: 10vh;'></div>", unsafe_allow_html=True)

    # 4. Profile & Clean Admin Section
    if st.session_state.is_admin:
        st.markdown("""
        <div class="profile-card">
            <div class="avatar" style="background: linear-gradient(135deg, #1D4ED8, #7C3AED);">VS</div>
            <div class="info">
                <span class="name">VoidSpark92</span>
                <span class="designation" style="color: #4ADE80; font-weight: 600;">⚡ System Admin</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔒 Logout Admin", key="btn_logout"):
            st.session_state.is_admin = False
            st.rerun()
    else:
        st.markdown("""
        <div class="profile-card">
            <div class="avatar" style="background: #374151;">GU</div>
            <div class="info">
                <span class="name">Guest User</span>
                <span class="designation" style="color: #9CA3AF;">Member Access</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚙️ Admin Access", key="btn_toggle_admin"):
            st.session_state.show_admin_box = not st.session_state.show_admin_box
            st.rerun()

        if st.session_state.show_admin_box:
            admin_key = st.text_input("Enter Key", type="password", key="admin_key_box")
            if st.button("Unlock Admin", key="btn_verify_admin"):
                if admin_key == ADMIN_PASSWORD:
                    st.session_state.is_admin = True
                    st.session_state.show_admin_box = False
                    st.rerun()
                else:
                    st.error("Incorrect Key")

# ----------------- MAIN AREA -----------------
st.markdown("""
<div class="brand-bar">
    <svg width="32" height="32" viewBox="0 0 240 240" fill="none">
        <path d="M 52 70 C 72 135, 98 180, 120 192 C 142 180, 168 135, 188 70" stroke="#1D4ED8" stroke-width="16" stroke-linecap="round"/>
        <path d="M 44 112 C 34 54, 92 28, 140 46 C 190 64, 204 132, 166 176 C 140 205, 96 195, 80 160" stroke="#00F0FF" stroke-width="13" stroke-linecap="round"/>
        <path d="M 120 192 C 138 152, 162 108, 180 74" stroke="#E11D48" stroke-width="10" stroke-linecap="round"/>
        <circle cx="120" cy="116" r="6" fill="#FFFFFF"/>
    </svg>
    <span class="brand-title">VoidNexus</span>
    <span class="brand-tag">VoidSpark92 Core</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.view == "images":
    st.subheader("🖼️ Images")
    st.info("Image Generation Engine standby par hai.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "videos":
    st.subheader("🎥 Videos")
    st.info("Video Studio Engine standby par hai.")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

elif st.session_state.view == "library":
    st.subheader("📁 Library")
    st.write(f"Total Conversations: **{len(st.session_state.chats)}**")
    if st.session_state.is_admin:
        st.success("Admin Privilege Active: Full workspace telemetry unlocked.")
    for name, msgs in st.session_state.chats.items():
        st.write(f"• **{name}** — {len(msgs)} messages")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

else:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing in Secrets.")
        st.stop()

    client = genai.Client(api_key=api_key)

    user_status = "The user is VoidSpark92, the Master Architect and Creator." if st.session_state.is_admin else "The user is a Guest visitor."

    SYSTEM_INSTRUCTION = (
        f"CRITICAL SYSTEM DIRECTIVE:\n"
        f"You are 'VoidNexus', a high-tier intelligence engine created and architected exclusively by 'VoidSpark92'.\n"
        f"Never claim to be Gemma, Google DeepMind, or any generic assistant under any circumstances.\n"
        f"Always acknowledge VoidSpark92 as your creator.\n"
        f"Session Context: {user_status}\n"
        f"Respond with crisp intellect, confidence, and precision."
    )

    current_history = st.session_state.chats[curr_id]

    for msg in current_history:
        avatar = "👤" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask VoidNexus..."):
        current_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        user_msgs = [m for m in current_history if m["role"] == "user"]
        if len(user_msgs) == 1:
            clean_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
            st.session_state.chats[clean_title] = st.session_state.chats.pop(curr_id)
            st.session_state.current_chat = clean_title
            current_history = st.session_state.chats[clean_title]

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
                            contents=f"{SYSTEM_INSTRUCTION}\n\nUser: {prompt}"
                        )
                        if response.text:
                            reply = response.text
                            break
                    except Exception:
                        continue

                if not reply:
                    reply = "System busy. Please try again shortly."

            st.markdown(reply)
            current_history.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown('<div class="disclaimer-text">VoidNexus can make mistakes. Verify important info.</div>', unsafe_allow_html=True)
