"""Tests du générateur d'embeddings."""

from unittest.mock import MagicMock, patch

from rag.embedder import Embedder


def test_get_embeddings_uses_configured_model():
    with patch("rag.embedder.FastEmbedEmbeddings") as MockFastEmbed:
        MockFastEmbed.return_value = MagicMock()
        embedder = Embedder(model_name="BAAI/bge-small-en-v1.5")
        embedder.get_embeddings()
        MockFastEmbed.assert_called_once_with(model_name="BAAI/bge-small-en-v1.5")


def test_get_embeddings_custom_model():
    with patch("rag.embedder.FastEmbedEmbeddings") as MockFastEmbed:
        MockFastEmbed.return_value = MagicMock()
        embedder = Embedder(model_name="nomic-ai/nomic-embed-text-v1")
        embedder.get_embeddings()
        MockFastEmbed.assert_called_once_with(model_name="nomic-ai/nomic-embed-text-v1")


def test_get_embeddings_returns_instance():
    mock_instance = MagicMock()
    with patch("rag.embedder.FastEmbedEmbeddings", return_value=mock_instance):
        embedder = Embedder()
        result = embedder.get_embeddings()
        assert result is mock_instance
