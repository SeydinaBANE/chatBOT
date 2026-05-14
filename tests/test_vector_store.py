"""Tests du vector store ChromaDB."""

from unittest.mock import MagicMock, patch

from rag.vector_store import VectorStore


def _make_store(count=0):
    """Crée un VectorStore avec un Chroma mocké."""
    with patch("rag.vector_store.Chroma") as MockChroma:
        mock_chroma = MagicMock()
        mock_chroma._collection.count.return_value = count
        MockChroma.return_value = mock_chroma
        vs = VectorStore(persist_dir="/tmp/test_chroma", embeddings=MagicMock())
        return vs, mock_chroma


def test_add_documents_delegates_to_chroma():
    vs, mock_chroma = _make_store()
    docs = [MagicMock(), MagicMock()]
    vs.add_documents(docs)
    mock_chroma.add_documents.assert_called_once_with(docs)


def test_get_retriever_passes_k():
    vs, mock_chroma = _make_store()
    vs.get_retriever(k=3)
    mock_chroma.as_retriever.assert_called_once_with(search_kwargs={"k": 3})


def test_get_retriever_default_k():
    vs, mock_chroma = _make_store()
    vs.get_retriever()
    mock_chroma.as_retriever.assert_called_once_with(search_kwargs={"k": 4})


def test_has_documents_true_when_count_positive():
    vs, _ = _make_store(count=5)
    assert vs.has_documents() is True


def test_has_documents_false_when_count_zero():
    vs, _ = _make_store(count=0)
    assert vs.has_documents() is False


def test_chroma_initialized_with_persist_dir():
    with patch("rag.vector_store.Chroma") as MockChroma:
        MockChroma.return_value = MagicMock()
        embeddings = MagicMock()
        VectorStore(persist_dir="/custom/path", embeddings=embeddings)
        MockChroma.assert_called_once_with(
            persist_directory="/custom/path",
            embedding_function=embeddings,
        )
