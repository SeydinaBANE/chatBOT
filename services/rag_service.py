"""Service d'indexation PDF et de construction de la chaîne RAG."""

from langchain_community.chat_models import ChatOllama

from core.chain import build_rag_chain
from rag.loader import PDFLoader
from rag.vector_store import VectorStore
from services.chat_service import ChatService


class RagService:
    """Orchestre l'indexation de documents PDF et la création du ChatService RAG."""

    def __init__(
        self,
        loader: PDFLoader,
        vector_store: VectorStore,
        llm: ChatOllama,
    ) -> None:
        """
        Args:
            loader: Chargeur PDF avec découpage en chunks.
            vector_store: Vector store ChromaDB persistant.
            llm: Modèle de langage partagé avec la chaîne simple.
        """
        self._loader = loader
        self._vector_store = vector_store
        self._llm = llm

    def index_pdf(self, data: bytes, filename: str) -> int:
        """Indexe un fichier PDF dans le vector store.

        Args:
            data: Contenu binaire du PDF (depuis un upload Streamlit).
            filename: Nom du fichier pour les métadonnées.

        Returns:
            Nombre de chunks indexés.
        """
        documents = self._loader.load_from_bytes(data, filename)
        self._vector_store.add_documents(documents)
        return len(documents)

    def build_rag_chat_service(self) -> ChatService:
        """Construit un ChatService utilisant la chaîne RAG avec le retriever actuel.

        Returns:
            ChatService prêt à répondre à partir des documents indexés.
        """
        retriever = self._vector_store.get_retriever()
        chain = build_rag_chain(self._llm, retriever)
        return ChatService(chain)

    def has_documents(self) -> bool:
        """Indique si des documents ont déjà été indexés dans le vector store."""
        return self._vector_store.has_documents()
