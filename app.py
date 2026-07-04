import streamlit as st
import google.generativeai as genai

# Streamlit secrets se key utha rahe hain
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Model ka naam sahi likhein: 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Mera Personal AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mujhse kuch bhi poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
