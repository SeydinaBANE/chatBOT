# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Prérequis

Docker ou Python 3.11+ avec Ollama en local.

## Lancer l'application

**Via Docker (recommandé) :**

```bash
cp .env.example .env
make docker-up      # build + démarre Ollama + app
make docker-pull    # télécharge tinyllama dans le conteneur Ollama
```

**En local :**

```bash
cp .env.example .env
pip install -r requirements.txt
ollama pull tinyllama
streamlit run main.py
```

## Docker

- `Dockerfile` — image `python:3.11-slim`, expose le port 8501
- `docker-compose.yml` — deux services : `ollama` + `app`
- L'env var `OLLAMA_BASE_URL=http://ollama:11434` dans `docker-compose.yml` écrase celle du `.env` pour que `app` parle au service `ollama` par son nom DNS interne
- Deux volumes nommés : `ollama_data` (modèles) et `chroma_data` (index RAG)

## Tests

```bash
pytest -v                              # tous les tests
pytest tests/test_rag_service.py -v   # un seul module
```

49 tests unitaires, tout mocké — aucun service externe requis.

## Qualité du code

```bash
pre-commit install          # activer les hooks (une fois)
ruff check .                # lint
ruff format .               # format
mypy . --ignore-missing-imports
```

La config ruff, mypy et pytest est dans `pyproject.toml`. Le CI exécute le job `lint` avant `tests`.

## Configuration

Tous les paramètres (LLM et RAG) sont dans `.env`, chargés via `pydantic-settings` dans `config/settings.py`. Aucune valeur n'est hardcodée dans le code.

## Architecture modulaire

```
main.py                  ← composition root : câble toutes les dépendances + configure logging
pyproject.toml           ← config ruff, mypy, pytest
.pre-commit-config.yaml  ← hooks ruff (lint + format) + mypy
config/settings.py       ← Settings (pydantic-settings), charge .env
core/
  llm_factory.py         ← create_llm(settings) → ChatOllama
  prompts.py             ← build_chat_prompt() et build_rag_prompt()
  chain.py               ← build_chain(llm) et build_rag_chain(llm, retriever)
services/
  chat_service.py        ← ChatService : poser_question() + stream_question(), logging + erreurs
  rag_service.py         ← RagService : index_pdf() + build_rag_chat_service(), logging + erreurs
ui/
  streamlit_app.py       ← run(chat_service, rag_service) : st.chat_input + st.write_stream
rag/
  loader.py              ← PDFLoader (PyPDF + RecursiveCharacterTextSplitter)
  embedder.py            ← Embedder / FastEmbedEmbeddings (local, sans API)
  vector_store.py        ← VectorStore / Chroma (persistance disque)
tests/                   ← 49 tests unitaires (pytest, tout mocké)
```

**Flux de dépendances :** `.env → settings → create_llm → build_chain → ChatService → UI`

L'UI n'importe aucune classe LangChain. `core/` n'importe rien de `services/` ou `ui/`.

## Chaînes LCEL

- **Simple** (`core/chain.py`) : `prompt | llm | StrOutputParser()`
- **RAG** (`core/chain.py`) : `RunnablePassthrough.assign(context=...) | rag_prompt | llm | parser`

Les deux chaînes s'appellent via `.invoke({"question": "..."})` ou `.stream({"question": "..."})`.

## Streaming

`ChatService.stream_question()` délègue à `chain.stream()` via `yield from` — c'est un générateur paresseux. L'UI utilise `st.write_stream()` pour afficher les tokens au fil de la génération. Les erreurs mid-stream sont capturées par le `try/except` autour du `yield from`.

## Gestion d'erreurs et logging

- Logging configuré dans `main.py` (`logging.basicConfig`, format ISO, level INFO)
- `ChatService` et `RagService` : `logger = logging.getLogger(__name__)`, `try/except` avec `logger.error(..., exc_info=True)` puis re-raise
- UI : `st.error()` autour des appels aux services — l'app ne plante jamais silencieusement

## Fonctionnement du RAG

1. L'utilisateur uploade un PDF via la sidebar Streamlit
2. `RagService.index_pdf()` → `PDFLoader.load_from_bytes()` → chunks → `VectorStore.add_documents()`
3. `RagService.build_rag_chat_service()` retourne un nouveau `ChatService` avec la chaîne RAG câblée
4. Les sessions suivantes restaurent le mode RAG automatiquement si `VectorStore.has_documents()` est vrai
