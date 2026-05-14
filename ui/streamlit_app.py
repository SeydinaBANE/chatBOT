import streamlit as st

from services.chat_service import ChatService


def run(chat_service: ChatService) -> None:
    st.title("Chatbot avec Ollama et LangChain")

    if "history" not in st.session_state:
        st.session_state.history = []

    question = st.text_input("Pose ta question")

    if st.button("Envoyer") and question.strip():
        reponse = chat_service.poser_question(question)
        st.session_state.history.append(("Vous", question))
        st.session_state.history.append(("Bot", reponse))

    for auteur, msg in st.session_state.history:
        if auteur == "Vous":
            st.markdown(f"**🧑 Vous :** {msg}")
        else:
            st.markdown(f"**🤖 Bot :** {msg}")
