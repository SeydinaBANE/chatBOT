"""Service métier du chatbot — point d'entrée unique pour l'UI."""

import logging
from typing import Iterator

from langchain_core.runnables import Runnable

logger = logging.getLogger(__name__)


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

        Raises:
            Exception: Propage toute erreur LLM après l'avoir loguée.
        """
        try:
            return self._chain.invoke({"question": question})
        except Exception as e:
            logger.error("Erreur lors de la génération de la réponse : %s", e, exc_info=True)
            raise

    def stream_question(self, question: str) -> Iterator[str]:
        """Envoie une question et retourne un générateur de tokens.

        Permet un affichage progressif (token-by-token) dans l'UI.

        Args:
            question: Question posée par l'utilisateur.

        Returns:
            Générateur de fragments de texte au fil de la génération.

        Raises:
            Exception: Propage toute erreur survenant pendant le streaming.
        """
        try:
            yield from self._chain.stream({"question": question})
        except Exception as e:
            logger.error("Erreur pendant le streaming : %s", e, exc_info=True)
            raise
