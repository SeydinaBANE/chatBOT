"""Tests du service de chat."""

import logging

import pytest

from services.chat_service import ChatService


def test_poser_question_calls_chain_invoke(mock_chain):
    service = ChatService(mock_chain)
    service.poser_question("Bonjour")
    mock_chain.invoke.assert_called_once_with({"question": "Bonjour"})


def test_poser_question_returns_chain_result(mock_chain):
    service = ChatService(mock_chain)
    result = service.poser_question("Quelle heure est-il ?")
    assert result == "réponse simulée"


def test_poser_question_passes_exact_text(mock_chain):
    service = ChatService(mock_chain)
    service.poser_question("Qui es-tu ?")
    args = mock_chain.invoke.call_args[0][0]
    assert args["question"] == "Qui es-tu ?"


def test_poser_question_propagates_exception(mock_chain):
    mock_chain.invoke.side_effect = ConnectionError("Ollama non disponible")
    service = ChatService(mock_chain)
    with pytest.raises(ConnectionError):
        service.poser_question("Bonjour")


def test_poser_question_logs_error(mock_chain, caplog):
    mock_chain.invoke.side_effect = RuntimeError("erreur LLM")
    service = ChatService(mock_chain)
    with caplog.at_level(logging.ERROR, logger="services.chat_service"):
        with pytest.raises(RuntimeError):
            service.poser_question("Test")
    assert "erreur LLM" in caplog.text


def test_stream_question_calls_chain_stream(mock_chain):
    mock_chain.stream.return_value = iter(["token1", " token2"])
    service = ChatService(mock_chain)
    list(service.stream_question("Salut"))
    mock_chain.stream.assert_called_once_with({"question": "Salut"})


def test_stream_question_yields_tokens(mock_chain):
    mock_chain.stream.return_value = iter(["Bon", "jour", " !"])
    service = ChatService(mock_chain)
    tokens = list(service.stream_question("Test"))
    assert tokens == ["Bon", "jour", " !"]


def test_stream_question_passes_exact_text(mock_chain):
    mock_chain.stream.return_value = iter([])
    service = ChatService(mock_chain)
    list(service.stream_question("Quelle est la capitale ?"))  # consomme le générateur
    args = mock_chain.stream.call_args[0][0]
    assert args["question"] == "Quelle est la capitale ?"


def test_stream_question_propagates_exception(mock_chain):
    def _failing_stream(*args, **kwargs):
        yield "token1"
        raise ConnectionError("connexion perdue en cours de stream")

    mock_chain.stream.side_effect = _failing_stream
    service = ChatService(mock_chain)
    with pytest.raises(ConnectionError):
        list(service.stream_question("Test"))


def test_stream_question_logs_error(mock_chain, caplog):
    def _failing_stream(*args, **kwargs):
        raise RuntimeError("erreur stream")
        yield  # noqa: RET505 — rend la fonction générateur

    mock_chain.stream.side_effect = _failing_stream
    service = ChatService(mock_chain)
    with caplog.at_level(logging.ERROR, logger="services.chat_service"):
        with pytest.raises(RuntimeError):
            list(service.stream_question("Test"))
    assert "erreur stream" in caplog.text
