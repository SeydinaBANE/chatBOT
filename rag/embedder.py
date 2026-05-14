"""Génération d'embeddings pour le pipeline RAG (scaffold)."""

from langchain_community.embeddings import FastEmbedEmbeddings


class Embedder:
    """Fournit un modèle d'embeddings via FastEmbed."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        """
        Args:
            model_name: Identifiant du modèle FastEmbed à utiliser.
        """
        self._model_name = model_name

    def get_embeddings(self) -> FastEmbedEmbeddings:
        """Retourne une instance FastEmbedEmbeddings configurée.

        Returns:
            Instance prête à être passée au vector store.

        Raises:
            NotImplementedError: Jusqu'à l'implémentation complète du RAG.
        """
        raise NotImplementedError("RAG — embeddings non encore implémentés")
