import streamlit as st
from openai import OpenAI

st.title("voxbox")

# Initialize session state for verification and chat history
if "verified" not in st.session_state:
    st.session_state.verified = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- PAGE 1: API KEY INPUT ---
if not st.session_state.verified:
    api_key = st.text_input("Enter your API Key", type="password")
    
    if st.button("Verify Key"):
        if api_key:
            try:
                # Test the key by listing models (low cost/impact)
                client = OpenAI(api_key=api_key)
                client.models.list() 
                
                # If successful, save to session state
                st.session_state.openai_key = api_key
                st.session_state.verified = True
                st.rerun()
            except Exception as e:
                st.error(f"Invalid API Key: {e}")
        else:
            st.warning("Please enter a key.")

# --- PAGE 2: CHATBOT INTERFACE ---
else:
    client = OpenAI(api_key=st.session_state.openai_key)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Logout / Clear Key"):
        st.session_state.verified = False
        st.rerun()
