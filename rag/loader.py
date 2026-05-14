"""Chargement et découpage de documents PDF pour le pipeline RAG."""

import tempfile
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFLoader:
    """Charge un PDF depuis le disque ou des bytes et le découpe en chunks."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
        """
        Args:
            chunk_size: Taille maximale de chaque chunk en caractères.
            chunk_overlap: Chevauchement entre chunks consécutifs.
        """
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def load(self, path: Path) -> list[Document]:
        """Charge un fichier PDF depuis le disque et retourne les chunks.

        Args:
            path: Chemin vers le fichier PDF.

        Returns:
            Liste de Document LangChain découpés en chunks.
        """
        loader = PyPDFLoader(str(path))
        pages = loader.load()
        return self._splitter.split_documents(pages)

    def load_from_bytes(self, data: bytes, filename: str) -> list[Document]:
        """Charge un PDF depuis des bytes (upload Streamlit) et retourne les chunks.

        Args:
            data: Contenu binaire du fichier PDF.
            filename: Nom du fichier (utilisé pour les métadonnées).

        Returns:
            Liste de Document LangChain découpés en chunks.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(data)
            tmp_path = Path(tmp.name)
        try:
            return self.load(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)
