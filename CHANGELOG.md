# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Format basé sur [Keep a Changelog](https://keepachangelog.com/),
et le projet suit [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-06-01

### Ajouté

- Interface Streamlit avec historique de conversation
- Mode RAG : upload PDF → indexation ChromaDB → réponses contextuelles
- Streaming token-by-token des réponses LLM
- Architecture modulaire : config / core / services / rag / ui
- 49 tests unitaires (pytest, tout mocké)
- CI pipeline : ruff + mypy + pytest (GitHub Actions)
- Docker Compose : Ollama + application
- Image Docker multi-stage avec utilisateur non-root
- Publication automatique sur ghcr.io
- Pre-commit hooks : ruff, mypy, bandit, hooks génériques
- Dependabot pour requirements.txt, Docker, GitHub Actions
- Scanner de sécurité Trivy dans la CI
- Configuration externalisée via pydantic-settings + .env
