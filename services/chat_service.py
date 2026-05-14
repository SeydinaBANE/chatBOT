"""Service métier du chatbot — point d'entrée unique pour l'UI."""

from langchain_core.runnables import Runnable


class ChatService:
    """Encapsule la chaîne LangChain et expose une API simple à l'interface."""

    def __init__(self, chain: Runnable) -> None:
        """
        Args:
            chain: Chaîne LCEL injectée depuis main.py.
        """
        self._chain = chain

    def poser_question(self, question: str) -> str:
        """Envoie une question à la chaîne et retourne la réponse textuelle.

        Args:
            question: Question posée par l'utilisateur.

        Returns:
            Réponse générée par le modèle.
        """
        return self._chain.invoke({"question": question})
