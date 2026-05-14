"""Tests d'assemblage des chaînes LCEL."""

from langchain_core.runnables import Runnable

from core.chain import build_chain, build_rag_chain


def test_build_chain_returns_runnable(mock_llm):
    chain = build_chain(mock_llm)
    assert isinstance(chain, Runnable)


def test_build_rag_chain_returns_runnable(mock_llm, mock_retriever):
    chain = build_rag_chain(mock_llm, mock_retriever)
    assert isinstance(chain, Runnable)


def test_build_chain_and_rag_chain_are_distinct(mock_llm, mock_retriever):
    simple = build_chain(mock_llm)
    rag = build_rag_chain(mock_llm, mock_retriever)
    assert simple is not rag
