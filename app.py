import streamlit as st
from google import genai

st.title("Mera Personal AI Assistant")

# Secrets se API key lein
if "GOOGLE_API_KEY" in st.secrets:
    # Nayi library ka client initialize karein
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Please set it in Streamlit Cloud Secrets.")
    st.stop()

# Session state initialize karein
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages dikhayein
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Naya input lein
if prompt := st.chat_input("Mujhse kuch bhi poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Nayi library ka istemal karte hue model call
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
