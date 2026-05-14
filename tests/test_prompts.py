"""Tests des prompts LangChain."""

from langchain_core.prompts import ChatPromptTemplate

from core.prompts import build_chat_prompt, build_rag_prompt


def test_build_chat_prompt_returns_template():
    prompt = build_chat_prompt()
    assert isinstance(prompt, ChatPromptTemplate)


def test_build_chat_prompt_requires_question():
    prompt = build_chat_prompt()
    assert "question" in prompt.input_variables


def test_build_chat_prompt_only_question():
    prompt = build_chat_prompt()
    assert set(prompt.input_variables) == {"question"}


def test_build_rag_prompt_returns_template():
    prompt = build_rag_prompt()
    assert isinstance(prompt, ChatPromptTemplate)


def test_build_rag_prompt_requires_context_and_question():
    prompt = build_rag_prompt()
    assert "question" in prompt.input_variables
    assert "context" in prompt.input_variables


def test_build_rag_prompt_only_context_and_question():
    prompt = build_rag_prompt()
    assert set(prompt.input_variables) == {"context", "question"}
