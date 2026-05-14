"""Tests du service RAG."""

import logging
from unittest.mock import MagicMock, patch

import pytest

from services.chat_service import ChatService
from services.rag_service import RagService


def _make_service(n_docs=2):
    loader = MagicMock()
    loader.load_from_bytes.return_value = [MagicMock() for _ in range(n_docs)]
    vector_store = MagicMock()
    llm = MagicMock()
    return RagService(loader=loader, vector_store=vector_store, llm=llm), loader, vector_store


def test_index_pdf_returns_chunk_count():
    service, loader, _ = _make_service(n_docs=3)
    count = service.index_pdf(b"fake pdf", "doc.pdf")
    assert count == 3


def test_index_pdf_calls_loader_with_bytes_and_filename():
    service, loader, _ = _make_service()
    service.index_pdf(b"data", "fichier.pdf")
    loader.load_from_bytes.assert_called_once_with(b"data", "fichier.pdf")


def test_index_pdf_adds_documents_to_vector_store():
    service, loader, vector_store = _make_service(n_docs=2)
    service.index_pdf(b"data", "doc.pdf")
    vector_store.add_documents.assert_called_once_with(loader.load_from_bytes.return_value)


def test_index_pdf_propagates_exception():
    service, loader, _ = _make_service()
    loader.load_from_bytes.side_effect = ValueError("PDF corrompu")
    with pytest.raises(ValueError, match="PDF corrompu"):
        service.index_pdf(b"bad data", "corrupt.pdf")


def test_index_pdf_logs_start_and_success(caplog):
    service, _, _ = _make_service(n_docs=2)
    with caplog.at_level(logging.INFO, logger="services.rag_service"):
        service.index_pdf(b"data", "rapport.pdf")
    assert "rapport.pdf" in caplog.text
    assert "2 chunks" in caplog.text


def test_index_pdf_logs_error(caplog):
    service, loader, _ = _make_service()
    loader.load_from_bytes.side_effect = RuntimeError("échec parsing")
    with caplog.at_level(logging.ERROR, logger="services.rag_service"):
        with pytest.raises(RuntimeError):
            service.index_pdf(b"data", "doc.pdf")
    assert "échec parsing" in caplog.text


def test_has_documents_delegates_to_vector_store():
    service, _, vector_store = _make_service()
    vector_store.has_documents.return_value = True
    assert service.has_documents() is True
    vector_store.has_documents.return_value = False
    assert service.has_documents() is False


def test_build_rag_chat_service_returns_chat_service():
    service, _, vector_store = _make_service()
    with patch("services.rag_service.build_rag_chain", return_value=MagicMock()):
        result = service.build_rag_chat_service()
    assert isinstance(result, ChatService)


def test_build_rag_chat_service_uses_retriever():
    service, _, vector_store = _make_service()
    with patch("services.rag_service.build_rag_chain") as mock_build:
        mock_build.return_value = MagicMock()
        service.build_rag_chat_service()
        vector_store.get_retriever.assert_called_once()
        mock_build.assert_called_once_with(service._llm, vector_store.get_retriever.return_value)
