# ChatBot Ollama + LangChain

[![CI](https://github.com/SeydinaBANE/chatBOT/actions/workflows/ci.yml/badge.svg)](https://github.com/SeydinaBANE/chatBOT/actions/workflows/ci.yml)
[![ghcr.io](https://ghcr-badge.deta.dev/seydinabane/chatbot/latest_tag?trim=major&label=image)](https://ghcr.io/seydinabane/chatbot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Chatbot RAG en Python avec LangChain (LCEL), modèle LLaMA via Ollama, interface Streamlit, et pipeline CI/CD complet publiant sur ghcr.io.

## Fonctionnalités

- Questions en langage naturel avec réponses **streamées token-by-token**
- Modèle LLM local via Ollama (aucune API externe)
- Interface web Streamlit avec historique de conversation
- **RAG opérationnel** : upload PDF → indexation ChromaDB → réponses basées sur le document
- Gestion d'erreurs avec messages clairs (Ollama éteint, PDF corrompu…)
- Configuration externalisée via `.env` (pydantic-settings)
- Arrêt gracieux (signal handler SIGTERM)
- **49 tests unitaires** (pytest, 97% de couverture)
- Image Docker multi-stage publiée sur **ghcr.io**

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
make setup            # pip install + pre-commit install
ollama pull tinyllama
```

## Utilisation

```bash
make run              # streamlit run main.py
```

### Mode RAG (documents PDF)

1. Ouvrir la **sidebar** dans Streamlit
2. Télécharger un fichier PDF
3. Cliquer sur **"Indexer le document"**
4. Poser des questions sur le contenu du document

Le mode RAG s'active automatiquement après indexation. Les réponses sont générées uniquement à partir du contenu du PDF. Un rechargement de l'app restaure le mode RAG si des documents ont déjà été indexés (persistance ChromaDB).

## Déploiement avec Docker

### Image pré-buildée (ghcr.io)

```bash
docker pull ghcr.io/seydinabane/chatbot:latest

# Créer un réseau pour que l'app puisse joindre Ollama
docker network create chatbot-net

# Lancer Ollama
docker run -d --name ollama --network chatbot-net -v ollama_data:/root/.ollama ollama/ollama
docker exec ollama ollama pull tinyllama

# Lancer l'application
docker run -d --name chatbot --network chatbot-net -p 8501:8501 \
  -e OLLAMA_BASE_URL=http://ollama:11434 \
  -v chroma_data:/app/chroma_db \
  ghcr.io/seydinabane/chatbot:latest
```

### Avec Docker Compose (production)

```bash
cp .env.example .env
make docker-up
```

## Tests

```bash
make test             # pytest -v
make coverage         # pytest --cov --cov-report=term-missing
```

## Qualité du code

```bash
make setup            # installer les pre-commit hooks (une fois)
make check            # ruff lint + ruff format + mypy
make security         # bandit + safety + pip-audit
make all              # toutes les vérifications en une commande
```

### Pre-commit hooks (s'exécutent à chaque commit)

| Hook | Rôle |
|---|---|
| `trailing-whitespace` | Supprime les espaces en fin de ligne |
| `end-of-file-fixer` | Garantit une ligne vide en fin de fichier |
| `check-yaml` / `check-toml` / `check-json` | Valide les fichiers de config |
| `check-added-large-files` | Bloque les fichiers > 500 Ko |
| `check-merge-conflict` | Détecte les marqueurs de conflit git |
| `detect-private-key` | Empêche de commiter des clés privées |
| `ruff` (lint + format) | Maintient le style Python |
| `mypy` | Vérification statique des types |
| `bandit` | Analyse de sécurité SAST |

## CI / CD

La pipeline GitHub Actions exécute 4 jobs en séquence :

```
lint → tests → security → build-and-push
                              ├── Trivy scan (CRITICAL/HIGH)
                              ├── ghcr.io/seydinabane/chatbot:latest (push sur main)
                              └── ghcr.io/seydinabane/chatbot:vX.Y.Z (push tag)
```

- **Dependabot** mets à jour automatiquement les dépendances (pip, Docker, GitHub Actions) chaque lundi.

## Versioning

- La version est dans `VERSION` (sémantique) : actuellement `0.1.0`
- Le `CHANGELOG.md` suit le format [Keep a Changelog](https://keepachangelog.com/)
- Un tag `v*` sur git déclenche le push d'une image taguée sur ghcr.io

```bash
git tag v0.2.0 && git push origin v0.2.0
```

## Configuration

Les paramètres sont dans `.env` (copié depuis `.env.example`), chargés via `pydantic-settings` :

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
| `LOG_LEVEL` | `INFO` | Niveau de log (DEBUG, INFO, WARNING, ERROR) |

## Architecture du projet

```
.
├── main.py                    ← Composition root : câble les dépendances + logging + signal handlers
├── pyproject.toml             ← Config ruff, mypy, pytest, coverage
├── .pre-commit-config.yaml    ← 9 hooks pre-commit
├── .editorconfig              ← Cohérence éditeurs
├── .python-version            ← Version Python (pyenv)
├── VERSION                    ← Version sémantique courante
├── CHANGELOG.md               ← Historique des modifications
├── Dockerfile                 ← Multi-stage, non-root, labels OCI
├── docker-compose.yml         ← Ollama + app, resource limits, read-only
├── config/
│   └── settings.py            ← pydantic-settings (variables .env)
├── core/
│   ├── llm_factory.py         ← create_llm() → ChatOllama
│   ├── prompts.py             ← build_chat_prompt() / build_rag_prompt()
│   └── chain.py               ← build_chain() / build_rag_chain() (LCEL)
├── services/
│   ├── chat_service.py        ← poser_question() + stream_question()
│   └── rag_service.py         ← index_pdf() + build_rag_chat_service()
├── rag/
│   ├── loader.py              ← PDFLoader (PyPDF + text splitter)
│   ├── embedder.py            ← FastEmbed embeddings (local)
│   └── vector_store.py        ← ChromaDB (persistance disque)
├── ui/
│   └── streamlit_app.py       ← Interface utilisateur Streamlit
├── tests/                     ← 49 tests unitaires (pytest, mocké)
└── .github/
    ├── workflows/ci.yml       ← CI : lint → tests → security → build & push
    └── dependabot.yml         ← Mises à jour automatiques
```

**Flux de dépendances :** `.env → settings → create_llm → build_chain → ChatService → UI`

L'UI n'importe aucune classe LangChain. `core/` n'importe rien de `services/` ou `ui/`.

## Makefile

```bash
make help              # Affiche toutes les cibles disponibles
make install           # pip install -r requirements.txt
make setup             # install + pre-commit install
make run               # streamlit run main.py
make test              # pytest -v
make coverage          # pytest --cov
make lint              # ruff check .
make format            # ruff format .
make typecheck         # mypy .
make check             # lint + typecheck + format (dry-run)
make security          # bandit + safety + pip-audit
make clean             # nettoie les artefacts Python
make docker-build      # docker compose build
make docker-up         # docker compose up --build -d
make docker-down       # docker compose down
make docker-pull       # télécharge le modèle Ollama
make all               # check + test + coverage + security
```
