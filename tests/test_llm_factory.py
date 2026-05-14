"""Tests de la factory LLM."""

from unittest.mock import patch

from config.settings import Settings
from core.llm_factory import create_llm


def test_create_llm_passes_correct_params():
    s = Settings(
        ollama_base_url="http://test:11434",
        ollama_model="llama3",
        ollama_temperature=0.3,
    )
    with patch("core.llm_factory.ChatOllama") as MockChatOllama:
        create_llm(s)
        MockChatOllama.assert_called_once_with(
            base_url="http://test:11434",
            model="llama3",
            temperature=0.3,
        )


def test_create_llm_returns_ollama_instance():
    from unittest.mock import MagicMock
    s = Settings()
    with patch("core.llm_factory.ChatOllama") as MockChatOllama:
        mock_instance = MagicMock()
        MockChatOllama.return_value = mock_instance
        result = create_llm(s)
        assert result is mock_instance
