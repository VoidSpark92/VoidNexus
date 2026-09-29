import os
import time
import json
import hashlib
import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="VoidNexus",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

ADMIN_CODE = os.environ.get("ADMIN_PASSWORD", "voidadmin92")
DB_FILE = "nexus_database.json"

# Database Utilities
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "chats": {}}
    return {"users": {}, "chats": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()

db = load_db()

# Futuristic Dark Theme + Audio Equalizer Animation CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        background-color: #131314 !important;
        color: #E3E3E3 !important;
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 100 !important;
    }

    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stExpandSidebarButton"] {
        color: #C4C7C5 !important;
        background-color: #1E1F20 !important;
        border: 1px solid #3C4043 !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
    }

    /* Sidebar Base */
    section[data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #282A2C !important;
        min-width: 300px !important;
        max-width: 300px !important;
        width: 300px !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: 0.8rem 0.9rem !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #C4C7C5 !important;
        border: none !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
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

    div[data-testid="stSidebar"] div.new-chat-wrapper .stButton > button {
        background-color: #282A2C !important;
        color: #E3E3E3 !important;
        border-radius: 24px !important;
        padding: 12px 20px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
        border: 1px solid #3C4043 !important;
    }

    div[data-testid="stSidebar"] div.new-chat-wrapper .stButton > button:hover {
        background-color: #37393B !important;
        color: #FFFFFF !important;
        border-color: #5E6368 !important;
    }

    .sidebar-label {
        font-size: 0.76rem;
        color: #8E918F;
        padding: 14px 12px 6px 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* FEATURE 3: Audio Waveform Equalizer Animation */
    .nexus-equalizer {
        display: flex;
        align-items: flex-end;
        gap: 5px;
        height: 24px;
        padding: 6px 0;
        margin-bottom: 10px;
    }
    .wave-bar {
        width: 4px;
        background: linear-gradient(180deg, #00F0FF, #7000FF, #FF007A);
        border-radius: 4px;
        animation: pulseEqualizer 0.8s infinite ease-in-out alternate;
    }
    .wave-bar:nth-child(1) { height: 30%; animation-delay: 0.1s; }
    .wave-bar:nth-child(2) { height: 80%; animation-delay: 0.3s; }
    .wave-bar:nth-child(3) { height: 100%; animation-delay: 0.15s; }
    .wave-bar:nth-child(4) { height: 60%; animation-delay: 0.4s; }
    .wave-bar:nth-child(5) { height: 40%; animation-delay: 0.25s; }

    @keyframes pulseEqualizer {
        0% { height: 20%; opacity: 0.4; }
        100% { height: 100%; opacity: 1; }
    }

    /* Telemetry HUD Box for Admin */
    .telemetry-card {
        background: #171819;
        border: 1px solid #282A2C;
        border-left: 4px solid #8AB4F8;
        padding: 12px 16px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        color: #C4C7C5;
    }

    /* Profile Card */
    .profile-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        border-top: 1px solid #282A2C;
        background-color: #171819;
        border-radius: 14px;
        margin-top: 15px;
        margin-bottom: 8px;
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

    .brand-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 0 10px 0;
    }

    .brand-title {
        font-size: 1.55rem;
        font-weight: 600;
        color: #E3E3E3;
    }

    .brand-tag {
        font-size: 0.78rem;
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
        padding: 1rem 0 !important;
        font-size: 1.05rem !important;
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
        font-size: 0.75rem;
        color: #8E918F;
        margin-top: 14px;
    }

    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "show_auth_modal" not in st.session_state:
    st.session_state.show_auth_modal = False

if "nexus_mode" not in st.session_state:
    st.session_state.nexus_mode = "⚡ Turbo"

if "view" not in st.session_state:
    st.session_state.view = "chat"

user_storage_key = "admin_voidspark92" if st.session_state.is_admin else (st.session_state.logged_user or "guest_session")

if user_storage_key not in db["chats"]:
    db["chats"][user_storage_key] = {
        "Chat 1": [{"role": "assistant", "content": "Welcome to VoidNexus. How can I assist you today?"}]
    }
    save_db(db)

user_chats = db["chats"][user_storage_key]

if "current_chat" not in st.session_state or st.session_state.current_chat not in user_chats:
    st.session_state.current_chat = list(user_chats.keys())[0]

curr_id = st.session_state.current_chat

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown('<div class="new-chat-wrapper">', unsafe_allow_html=True)
    if st.button("➕ New Chat", key="btn_new"):
        chat_idx = len(user_chats) + 1
        new_name = f"Chat {chat_idx}"
        user_chats[new_name] = []
        st.session_state.current_chat = new_name
        st.session_state.view = "chat"
        save_db(db)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🖼️ Images", key="nav_img"):
        st.session_state.view = "images"
        st.rerun()

    if st.button("🎥 Videos", key="nav_vid"):
        st.session_state.view = "videos"
        st.rerun()

    if st.button("📁 Library", key="nav_lib"):
        st.session_state.view = "library"
        st.rerun()

    st.markdown('<div class="sidebar-label">Recent History</div>', unsafe_allow_html=True)
    for c_name in list(user_chats.keys())[-5:]:
        icon = "●" if c_name == curr_id else "💬"
        if st.button(f"{icon}  {c_name}", key=f"hist_{c_name}"):
            st.session_state.current_chat = c_name
            st.session_state.view = "chat"
            st.rerun()

    st.markdown("<div style='min-height: 8vh;'></div>", unsafe_allow_html=True)

    # Profile & Admin Access
    if st.session_state.is_admin:
        st.markdown("""
        <div class="profile-card">
            <div class="avatar" style="background: linear-gradient(135deg, #1D4ED8, #7C3AED);">VS</div>
            <div class="info">
                <span style="font-size:0.95rem; font-weight:600; color:#E3E3E3;">VoidSpark92</span><br>
                <span style="font-size:0.75rem; color:#4ADE80; font-weight:600;">⚡ Master Architect</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔒 Logout Master", key="btn_logout_admin"):
            st.session_state.is_admin = False
            st.session_state.logged_user = None
            st.rerun()
    elif st.session_state.logged_user:
        st.markdown(f"""
        <div class="profile-card">
            <div class="avatar" style="background: #2563EB;">{st.session_state.logged_user[:2].upper()}</div>
            <div class="info">
                <span style="font-size:0.95rem; font-weight:600; color:#E3E3E3;">{st.session_state.logged_user}</span><br>
                <span style="font-size:0.75rem; color:#60A5FA;">Member (Synced)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", key="btn_logout_user"):
            st.session_state.logged_user = None
            st.rerun()
    else:
        st.markdown("""
        <div class="profile-card">
            <div class="avatar" style="background: #374151;">GU</div>
            <div class="info">
                <span style="font-size:0.95rem; font-weight:600; color:#E3E3E3;">Guest User</span><br>
                <span style="font-size:0.75rem; color:#9CA3AF;">Temporary Session</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔑 Login / Admin Sync", key="btn_open_login"):
            st.session_state.show_auth_modal = not st.session_state.show_auth_modal
            st.rerun()

        if st.session_state.show_auth_modal:
            st.markdown("---")
            tab_admin, tab_user = st.tabs(["👑 Admin Key", "👤 User Login"])
            with tab_admin:
                admin_key_input = st.text_input("Master Code", type="password", key="admin_key_field")
                if st.button("Authenticate", key="btn_admin_sync"):
                    if admin_key_input == ADMIN_CODE:
                        st.session_state.is_admin = True
                        st.session_state.logged_user = "VoidSpark92"
                        st.session_state.show_auth_modal = False
                        st.rerun()
                    else:
                        st.error("Invalid Code")
            with tab_user:
                mode = st.radio("Type", ["Sign In", "Sign Up"], horizontal=True, key="user_mode_radio")
                uname = st.text_input("User", key="un_input")
                pw = st.text_input("Pass", type="password", key="pw_input")
                if mode == "Sign Up":
                    if st.button("Register"):
                        if uname and pw:
                            if uname in db["users"]:
                                st.error("Taken")
                            else:
                                db["users"][uname] = hash_pw(pw)
                                save_db(db)
                                st.session_state.logged_user = uname
                                st.session_state.show_auth_modal = False
                                st.rerun()
                else:
                    if st.button("Sign In"):
                        if uname in db["users"] and db["users"][uname] == hash_pw(pw):
                            st.session_state.logged_user = uname
                            st.session_state.show_auth_modal = False
                            st.rerun()
                        else:
                            st.error("Invalid Login")

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

# FEATURE 2: Dynamic Persona Selector & Session Tools
col_mode, col_util = st.columns([3, 1])
with col_mode:
    st.session_state.nexus_mode = st.radio(
        "Mode:",
        ["⚡ Turbo", "🧠 Deep Think", "💻 Dev Mode"],
        horizontal=True,
        label_visibility="collapsed"
    )

with col_util:
    # Quick export feature
    current_history = user_chats.get(curr_id, [])
    full_chat_txt = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in current_history])
    st.download_button(
        label="📥 Export Chat",
        data=full_chat_txt,
        file_name=f"{curr_id.replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# Views Router
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
    st.write(f"Total Conversations Saved: **{len(user_chats)}**")
    for name, msgs in user_chats.items():
        st.write(f"• **{name}** — {len(msgs)} messages")
    if st.button("← Back to Chat"):
        st.session_state.view = "chat"
        st.rerun()

else:
    # ----------------- CHAT ENGINE -----------------
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing in Secrets.")
        st.stop()

    client = genai.Client(api_key=api_key)

    mode_prompts = {
        "⚡ Turbo": "Keep answers compact, rapid, razor-sharp, and to the point.",
        "🧠 Deep Think": "Provide structured, exhaustive, analytical reasoning with step-by-step logic.",
        "💻 Dev Mode": "Deliver production-grade code, technical architecture, and shell commands without conversational fluff."
    }
    mode_directive = mode_prompts.get(st.session_state.nexus_mode, "")

    user_status = "The user is VoidSpark92, the Master Architect and Creator." if st.session_state.is_admin else (f"The user is {st.session_state.logged_user}." if st.session_state.logged_user else "The user is a Guest visitor.")

    SYSTEM_INSTRUCTION = (
        f"CRITICAL SYSTEM DIRECTIVE:\n"
        f"You are 'VoidNexus', a sovereign AI intelligence created and architected exclusively by 'VoidSpark92'.\n"
        f"Never claim to be Gemma, Google DeepMind, or any generic assistant under any circumstances.\n"
        f"Always acknowledge VoidSpark92 as your creator.\n"
        f"Session Context: {user_status}\n"
        f"Active Mode Instruction: {mode_directive}\n"
        f"Respond with sharp intelligence and absolute precision."
    )

    # Render History
    for msg in current_history:
        avatar = "👤" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask VoidNexus..."):
        current_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Dynamic Rename
        user_msgs = [m for m in current_history if m["role"] == "user"]
        if len(user_msgs) == 1:
            clean_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
            user_chats[clean_title] = user_chats.pop(curr_id)
            st.session_state.current_chat = clean_title
            current_history = user_chats[clean_title]

        # FEATURE 1: Check for Admin Special Telemetry Command (/stats or /debug)
        if st.session_state.is_admin and prompt.strip().lower() in ["/stats", "/debug", "/status"]:
            with st.chat_message("assistant", avatar="💠"):
                total_users = len(db.get("users", {}))
                total_chats = sum(len(c) for c in db.get("chats", {}).values())
                telemetry_info = f"""
                <div class="telemetry-card">
                    <b>⚡ VOIDNEXUS ARCHITECT HUD:</b><br>
                    • <b>Core Engine:</b> Gemini Cloud Connected<br>
                    • <b>Active Persona:</b> {st.session_state.nexus_mode}<br>
                    • <b>Auth Level:</b> VoidSpark92 (Master Sovereign)<br>
                    • <b>Registered Users:</b> {total_users}<br>
                    • <b>Total Cloud Chats:</b> {total_chats}<br>
                    • <b>Integrity:</b> 100% Nominal (Zero Overlap Active)
                </div>
                """
                st.markdown(telemetry_info, unsafe_allow_html=True)
                current_history.append({"role": "assistant", "content": "⚡ **System HUD Telemetry Loaded.**"})
                save_db(db)
                st.rerun()

        else:
            with st.chat_message("assistant", avatar="💠"):
                # FEATURE 3: Cyberpunk Audio Pulse Waveform during generation
                pulse_ph = st.empty()
                pulse_ph.markdown("""
                <div class="nexus-equalizer">
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                </div>
                """, unsafe_allow_html=True)

                start_time = time.time()
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

                pulse_ph.empty()

                if not reply:
                    reply = "System busy. Please try again shortly."

                st.markdown(reply)
                current_history.append({"role": "assistant", "content": reply})
                save_db(db)
                st.rerun()

st.markdown('<div class="disclaimer-text">VoidNexus can make mistakes. Verify important info.</div>', unsafe_allow_html=True)
