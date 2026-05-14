"""Gestion du vector store ChromaDB pour le pipeline RAG (scaffold)."""

from langchain_core.vectorstores import VectorStoreRetriever


class VectorStore:
    """Encapsule ChromaDB et expose un retriever LangChain."""

    def get_retriever(self) -> VectorStoreRetriever:
        """Retourne un retriever utilisable dans une chaîne LCEL.

        Returns:
            VectorStoreRetriever configuré pour la recherche sémantique.

        Raises:
            NotImplementedError: Jusqu'à l'implémentation complète du RAG.
        """
        raise NotImplementedError("RAG — vector store non encore implémenté")
