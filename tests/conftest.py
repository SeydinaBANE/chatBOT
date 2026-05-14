"""Fixtures partagées entre tous les tests."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_chain():
    chain = MagicMock()
    chain.invoke.return_value = "réponse simulée"
    return chain


@pytest.fixture
def mock_llm():
    return MagicMock()


@pytest.fixture
def mock_retriever():
    retriever = MagicMock()
    retriever.invoke.return_value = []
    return retriever


@pytest.fixture
def mock_vector_store():
    vs = MagicMock()
    vs.has_documents.return_value = False
    vs.get_retriever.return_value = MagicMock()
    return vs
