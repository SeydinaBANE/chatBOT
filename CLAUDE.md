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

## Configuration

Tous les paramètres (modèle, URL Ollama, température) sont dans `.env`, chargés via `pydantic-settings` dans `config/settings.py`. Aucune valeur n'est hardcodée dans le code.

## Architecture modulaire

```
main.py              ← composition root : câble toutes les dépendances
config/settings.py   ← Settings (pydantic-settings), charge .env
core/
  llm_factory.py     ← create_llm(settings) → ChatOllama
  prompts.py         ← build_chat_prompt() → ChatPromptTemplate (français)
  chain.py           ← build_chain(llm) → LCEL : prompt | llm | StrOutputParser
services/
  chat_service.py    ← ChatService.poser_question(question) → str
ui/
  streamlit_app.py   ← run(chat_service) : interface Streamlit
rag/
  loader.py          ← PDFLoader (scaffold, NotImplementedError)
  embedder.py        ← Embedder / FastEmbedEmbeddings (scaffold)
  vector_store.py    ← VectorStore / ChromaDB (scaffold)
```

**Flux de dépendances :** `.env → settings → create_llm → build_chain → ChatService → UI`

L'UI n'importe aucune classe LangChain. Le module `rag/` est isolé — non câblé dans `main.py` tant que le RAG n'est pas implémenté.

## Chaîne LCEL

Définie dans `core/chain.py` : `prompt | llm | StrOutputParser()`, appelée via `.invoke({"question": "..."})` dans `ChatService`. Pour activer le streaming Streamlit, remplacer `.invoke()` par `.stream()` dans `services/chat_service.py` sans toucher à la chaîne.

## Étendre avec le RAG

Les stubs dans `rag/` lèvent `NotImplementedError`. Pour implémenter :
1. Compléter `rag/loader.py` (pypdf), `rag/embedder.py` (fastembed), `rag/vector_store.py` (chromadb)
2. Câbler le retriever dans `core/chain.py` via LCEL
3. Injecter dans `main.py`
