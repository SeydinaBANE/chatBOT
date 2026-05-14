"""Service métier du chatbot — point d'entrée unique pour l'UI."""

from typing import Iterator

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
        """Envoie une question à la chaîne et retourne la réponse complète.

        Args:
            question: Question posée par l'utilisateur.

        Returns:
            Réponse générée par le modèle.
        """
        return self._chain.invoke({"question": question})

    def stream_question(self, question: str) -> Iterator[str]:
        """Envoie une question et retourne un générateur de tokens.

        Permet un affichage progressif (token-by-token) dans l'UI.

        Args:
            question: Question posée par l'utilisateur.

        Returns:
            Générateur de fragments de texte au fil de la génération.
        """
        return self._chain.stream({"question": question})
