"""Interface utilisateur Streamlit du chatbot (mode simple et mode RAG)."""

import streamlit as st

from services.chat_service import ChatService
from services.rag_service import RagService


def run(chat_service: ChatService, rag_service: RagService) -> None:
    """Lance l'interface Streamlit avec streaming et support optionnel du RAG.

    Les réponses sont affichées token-by-token via st.write_stream().
    La sidebar permet d'uploader un PDF pour activer le mode RAG.

    Args:
        chat_service: Service de chat simple (sans contexte documentaire).
        rag_service: Service d'indexation PDF et de construction de la chaîne RAG.
    """
    st.title("Chatbot avec Ollama et LangChain")

    if "chat_service" not in st.session_state:
        st.session_state.chat_service = chat_service
    if "history" not in st.session_state:
        st.session_state.history = []
    if "rag_active" not in st.session_state:
        st.session_state.rag_active = rag_service.has_documents()

    # --- Sidebar ---
    with st.sidebar:
        st.header("Base de connaissances (RAG)")
        uploaded = st.file_uploader("Télécharger un PDF", type="pdf")

        if uploaded:
            if st.button("Indexer le document"):
                with st.spinner("Indexation en cours..."):
                    n_chunks = rag_service.index_pdf(uploaded.read(), uploaded.name)
                    st.session_state.chat_service = rag_service.build_rag_chat_service()
                    st.session_state.rag_active = True
                    st.session_state.history = []
                st.success(f"✅ {uploaded.name} indexé ({n_chunks} chunks).")

        if st.session_state.rag_active:
            st.info("Mode RAG actif — les réponses sont basées sur le document.")
        else:
            st.caption("Aucun document indexé. Le chatbot répond librement.")

    # --- Historique ---
    for auteur, msg in st.session_state.history:
        role = "user" if auteur == "Vous" else "assistant"
        with st.chat_message(role):
            st.markdown(msg)

    # --- Saisie et streaming ---
    if question := st.chat_input("Pose ta question"):
        st.session_state.history.append(("Vous", question))
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            reponse = st.write_stream(
                st.session_state.chat_service.stream_question(question)
            )
        st.session_state.history.append(("Bot", reponse))
