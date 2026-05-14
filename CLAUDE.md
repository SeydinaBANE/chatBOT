# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Prérequis

Ollama doit tourner en local avec le modèle souhaité :

```bash
ollama pull tinyllama
ollama serve   # si le service ne tourne pas déjà
```

## Lancer l'application

```bash
cp .env.example .env
pip install -r requirements.txt
streamlit run main.py
```

## Tests

```bash
pytest -v                              # tous les tests
pytest tests/test_rag_service.py -v   # un seul module
```

39 tests unitaires, tout mocké — aucun service externe requis.

## Configuration

Tous les paramètres (LLM et RAG) sont dans `.env`, chargés via `pydantic-settings` dans `config/settings.py`. Aucune valeur n'est hardcodée dans le code.

## Architecture modulaire

```
main.py                  ← composition root : câble toutes les dépendances
config/settings.py       ← Settings (pydantic-settings), charge .env
core/
  llm_factory.py         ← create_llm(settings) → ChatOllama
  prompts.py             ← build_chat_prompt() et build_rag_prompt()
  chain.py               ← build_chain(llm) et build_rag_chain(llm, retriever)
services/
  chat_service.py        ← ChatService.poser_question(question) → str
  rag_service.py         ← RagService : index_pdf() + build_rag_chat_service()
ui/
  streamlit_app.py       ← run(chat_service, rag_service) : sidebar PDF + chat
rag/
  loader.py              ← PDFLoader (PyPDF + RecursiveCharacterTextSplitter)
  embedder.py            ← Embedder / FastEmbedEmbeddings (local, sans API)
  vector_store.py        ← VectorStore / Chroma (persistance disque)
tests/                   ← 39 tests unitaires (pytest, tout mocké)
pytest.ini               ← pythonpath=. testpaths=tests
```

**Flux de dépendances :** `.env → settings → create_llm → build_chain → ChatService → UI`

L'UI n'importe aucune classe LangChain. `core/` n'importe rien de `services/` ou `ui/`.

## Chaînes LCEL

- **Simple** (`core/chain.py`) : `prompt | llm | StrOutputParser()` — `.invoke({"question": "..."})`
- **RAG** (`core/chain.py`) : `RunnablePassthrough.assign(context=...) | rag_prompt | llm | parser` — même interface `.invoke({"question": "..."})`

Pour activer le streaming Streamlit, remplacer `.invoke()` par `.stream()` dans `services/chat_service.py` sans toucher aux chaînes.

## Fonctionnement du RAG

1. L'utilisateur uploade un PDF via la sidebar Streamlit
2. `RagService.index_pdf()` → `PDFLoader.load_from_bytes()` → chunks → `VectorStore.add_documents()`
3. `RagService.build_rag_chat_service()` retourne un nouveau `ChatService` avec la chaîne RAG câblée
4. Les sessions suivantes restaurent le mode RAG automatiquement si `VectorStore.has_documents()` est vrai
