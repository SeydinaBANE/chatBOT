# ChatBot Ollama + LangChain

[![CI](https://github.com/SeydinaBANE/chatBOT/actions/workflows/ci.yml/badge.svg)](https://github.com/SeydinaBANE/chatBOT/actions/workflows/ci.yml)

Chatbot en Python avec architecture modulaire, utilisant LangChain (LCEL), le modèle LLaMA via Ollama, et une interface Streamlit.

## Fonctionnalités

- Questions en langage naturel avec réponses **streamées token-by-token**
- Modèle LLM local via Ollama (aucune API externe)
- Interface web Streamlit avec historique de conversation
- **RAG opérationnel** : upload PDF → indexation ChromaDB → réponses basées sur le document
- Gestion d'erreurs avec messages clairs (Ollama éteint, PDF corrompu…)
- Configuration externalisée via `.env`
- 49 tests unitaires (pytest)

## Prérequis

- Python 3.11+ **ou** Docker + Docker Compose
- [Ollama](https://ollama.com) (uniquement en mode local)

## Démarrage rapide — Docker (recommandé)

```bash
git clone https://github.com/SeydinaBANE/chatBOT.git
cd chatBOT

cp .env.example .env
make docker-up        # build + démarre Ollama et l'app
make docker-pull      # télécharge le modèle tinyllama dans Ollama
```

L'interface est disponible sur [http://localhost:8501](http://localhost:8501).

```bash
make docker-down      # arrêter les conteneurs
```

Les données (modèles Ollama, index ChromaDB) sont persistées dans des volumes Docker nommés.

## Installation locale (sans Docker)

```bash
git clone https://github.com/SeydinaBANE/chatBOT.git
cd chatBOT

cp .env.example .env
pip install -r requirements.txt
ollama pull tinyllama
```

## Utilisation locale

```bash
streamlit run main.py
```

### Mode RAG (documents PDF)

1. Ouvrir la **sidebar** dans Streamlit
2. Télécharger un fichier PDF
3. Cliquer sur **"Indexer le document"**
4. Poser des questions sur le contenu du document

Le mode RAG s'active automatiquement après indexation. Les réponses sont générées uniquement à partir du contenu du PDF. Un rechargement de l'app restaure le mode RAG si des documents ont déjà été indexés (persistance ChromaDB).

## Tests

```bash
pytest -v
```

## Qualité du code

```bash
# Installer les hooks (une fois)
pip install pre-commit
pre-commit install

# Lancer manuellement
ruff check .
ruff format .
mypy . --ignore-missing-imports
```

Les hooks ruff et mypy s'exécutent automatiquement à chaque `git commit`.

## Configuration

Les paramètres sont dans `.env` (copié depuis `.env.example`) :

| Variable | Défaut | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | URL du serveur Ollama |
| `OLLAMA_MODEL` | `tinyllama` | Modèle LLM à utiliser |
| `OLLAMA_TEMPERATURE` | `0.7` | Température de génération |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | Répertoire de persistance ChromaDB |
| `EMBED_MODEL` | `BAAI/bge-small-en-v1.5` | Modèle d'embeddings FastEmbed |
| `RAG_CHUNK_SIZE` | `1000` | Taille des chunks PDF (caractères) |
| `RAG_CHUNK_OVERLAP` | `200` | Chevauchement entre chunks |
| `RAG_RETRIEVER_K` | `4` | Nombre de chunks retournés par requête |

## Structure du projet

```
main.py                    ← point d'entrée (composition root)
pyproject.toml             ← config ruff, mypy, pytest
.pre-commit-config.yaml    ← hooks ruff + mypy
config/settings.py         ← configuration centralisée (pydantic-settings)
core/                      ← logique LangChain (LCEL)
services/
  chat_service.py          ← ChatService : poser_question() + stream_question()
  rag_service.py           ← RagService : indexation PDF + chaîne RAG
ui/                        ← interface Streamlit
rag/                       ← PDFLoader, Embedder, VectorStore (ChromaDB)
tests/                     ← 49 tests unitaires
```
