import streamlit as st
from chatbot import poser_question

st.title("Chatbot avec Ollama et LangChain")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Pose ta question")

if st.button("Envoyer") and question.strip():
    reponse = poser_question(question)
    st.session_state.history.append(("Vous", question))
    st.session_state.history.append(("Bot", reponse))

for auteur, msg in st.session_state.history:
    if auteur == "Vous":
        st.markdown(f"**🧑 {auteur} :** {msg}")
    else:
        st.markdown(f"**🤖 {auteur} :** {msg}")
