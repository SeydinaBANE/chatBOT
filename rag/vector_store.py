"""Gestion du vector store ChromaDB persistant."""

from typing import List

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


class VectorStore:
    """Encapsule ChromaDB avec persistance disque et expose un retriever LangChain."""

    def __init__(self, persist_dir: str, embeddings: object) -> None:
        """
        Args:
            persist_dir: Répertoire de persistance ChromaDB.
            embeddings: Instance d'embeddings compatible LangChain.
        """
        self._store = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
        )

    def add_documents(self, documents: List[Document]) -> None:
        """Indexe une liste de documents dans le vector store.

        Args:
            documents: Chunks LangChain à stocker et vectoriser.
        """
        self._store.add_documents(documents)

    def get_retriever(self, k: int = 4) -> VectorStoreRetriever:
        """Retourne un retriever pour la recherche sémantique.

        Args:
            k: Nombre de chunks à retourner par requête.

        Returns:
            VectorStoreRetriever utilisable dans une chaîne LCEL.
        """
        return self._store.as_retriever(search_kwargs={"k": k})

    def has_documents(self) -> bool:
        """Indique si le vector store contient au moins un document indexé."""
        return self._store._collection.count() > 0
