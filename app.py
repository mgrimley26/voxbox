import streamlit as st
from openai import OpenAI

# --- STEALTH UI CONFIG ---
st.set_page_config(page_title="Draft_v1", layout="centered", initial_sidebar_state="collapsed")

# CSS to hide all "Streamlit" visual cues and make text look like a document
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stMarkdown { font-family: 'Courier New', Courier, monospace; font-size: 14px; }
        .stTextInput > div > div > input { background-color: transparent; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "verified" not in st.session_state:
    st.session_state.verified = False

# --- HIDDEN INITIALIZATION ---
if not st.session_state.verified:
    # Quiet login: looks like a "Serial Number" or "Session ID" entry
    key = st.text_input("Session ID", type="password")
    if key:
        try:
            client = OpenAI(api_key=key)
            client.models.list()
            st.session_state.key = key
            st.session_state.verified = True
            st.rerun()
        except: st.error("Invalid ID")
    st.stop()

# --- THE "DOCUMENT" INTERFACE ---
client = OpenAI(api_key=st.session_state.key)

# Display the conversation as a simple text log
for msg in st.session_state.messages:
    prefix = "> " if msg["role"] == "user" else ""
    st.markdown(f"{prefix}{msg['content']}")

# Discrete input at the bottom (replaces the obvious chat bar)
with st.container():
    query = st.text_input("", placeholder="Type here...", label_visibility="collapsed")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Get AI response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
