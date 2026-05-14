from pathlib import Path
from typing import List

from langchain_core.documents import Document


class PDFLoader:
    def load(self, path: Path) -> List[Document]:
        raise NotImplementedError("RAG — chargement PDF non encore implémenté")
