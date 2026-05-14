"""Tests de la configuration centralisée."""

import pytest
from config.settings import Settings


def test_default_llm_values():
    s = Settings()
    assert s.ollama_base_url == "http://localhost:11434"
    assert s.ollama_model == "tinyllama"
    assert s.ollama_temperature == 0.7


def test_default_rag_values():
    s = Settings()
    assert s.chroma_persist_dir == "./chroma_db"
    assert s.embed_model == "BAAI/bge-small-en-v1.5"
    assert s.rag_chunk_size == 1000
    assert s.rag_chunk_overlap == 200
    assert s.rag_retriever_k == 4


def test_env_override_model(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "llama3")
    s = Settings()
    assert s.ollama_model == "llama3"


def test_env_override_temperature(monkeypatch):
    monkeypatch.setenv("OLLAMA_TEMPERATURE", "0.2")
    s = Settings()
    assert s.ollama_temperature == 0.2


def test_env_override_chunk_size(monkeypatch):
    monkeypatch.setenv("RAG_CHUNK_SIZE", "512")
    s = Settings()
    assert s.rag_chunk_size == 512
