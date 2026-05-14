"""Point d'entrée de l'application — composition root.

Câble toutes les dépendances et lance l'interface Streamlit.
Lancer avec : streamlit run main.py
"""

from config.settings import settings
from core.chain import build_chain
from core.llm_factory import create_llm
from rag.embedder import Embedder
from rag.loader import PDFLoader
from rag.vector_store import VectorStore
from services.chat_service import ChatService
from services.rag_service import RagService
from ui.streamlit_app import run

llm = create_llm(settings)

embedder = Embedder(model_name=settings.embed_model)
embeddings = embedder.get_embeddings()

loader = PDFLoader(
    chunk_size=settings.rag_chunk_size,
    chunk_overlap=settings.rag_chunk_overlap,
)
vector_store = VectorStore(
    persist_dir=settings.chroma_persist_dir,
    embeddings=embeddings,
)
rag_service = RagService(loader=loader, vector_store=vector_store, llm=llm)

chat_service = ChatService(build_chain(llm))

run(chat_service, rag_service)
