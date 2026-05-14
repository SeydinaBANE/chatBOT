"""Génération d'embeddings vectoriels via FastEmbed."""

from langchain_community.embeddings import FastEmbedEmbeddings


class Embedder:
    """Fournit un modèle d'embeddings léger via FastEmbed (aucune API externe)."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        """
        Args:
            model_name: Identifiant du modèle FastEmbed à utiliser.
        """
        self._model_name = model_name

    def get_embeddings(self) -> FastEmbedEmbeddings:
        """Instancie et retourne le modèle d'embeddings configuré.

        Returns:
            Instance FastEmbedEmbeddings prête à être passée au vector store.
        """
        return FastEmbedEmbeddings(model_name=self._model_name)
