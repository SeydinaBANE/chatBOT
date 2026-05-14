"""Chargement de documents PDF pour le pipeline RAG (scaffold)."""

from pathlib import Path
from typing import List

from langchain_core.documents import Document


class PDFLoader:
    """Charge et découpe des fichiers PDF en documents LangChain."""

    def load(self, path: Path) -> List[Document]:
        """Charge un fichier PDF et retourne une liste de documents.

        Args:
            path: Chemin vers le fichier PDF à charger.

        Returns:
            Liste de Document LangChain (un par page ou par chunk).

        Raises:
            NotImplementedError: Jusqu'à l'implémentation complète du RAG.
        """
        raise NotImplementedError("RAG — chargement PDF non encore implémenté")
