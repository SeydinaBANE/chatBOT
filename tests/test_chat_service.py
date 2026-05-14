"""Tests du service de chat."""

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
