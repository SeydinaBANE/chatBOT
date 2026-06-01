# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Format basé sur [Keep a Changelog](https://keepachangelog.com/),
et le projet suit [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-06-01

### Ajouté

- Interface Streamlit avec historique de conversation
- Mode RAG : upload PDF → indexation ChromaDB → réponses contextuelles
- Streaming token-by-token des réponses LLM
- 49 tests unitaires (pytest, tout mocké, 97% de couverture)
- Logging structuré avec niveau configurable via `LOG_LEVEL`
- Arrêt gracieux (signal handler SIGTERM)

### CI / CD

- Pipeline GitHub Actions à 4 jobs : lint → tests → security → build-and-push
- Image Docker multi-stage avec utilisateur non-root (labels OCI)
- Publication automatique sur `ghcr.io/seydinabane/chatbot:latest` et `:v*`
- Scanner Trivy (CRITICAL/HIGH, non-bloquant)
- Dependabot pour pip, Docker, GitHub Actions

### Qualité

- 9 hooks pre-commit : ruff (lint + format), mypy, bandit, hooks génériques
- Makefile avec 20 cibles (test, coverage, security, clean, all…)
- Dépendances Python pinnées (requirements.txt)
- Configuration Pydantic v2 (SettingsConfigDict)
- Annotations de type strictes dans toute la codebase
- `.editorconfig` + `.python-version` pour la cohérence des outils

### Infrastructure

- Docker Compose avec resource limits et read-only rootfs
- Multi-stage Docker builder pattern (image finale ~120 Mo)
- Métadonnées OCI dans l'image Docker

### Documentation

- README.md enrichi : badges, CI/CD, Makefile, architecture complète
- CLAUDE.md synchronisé avec les commandes et la structure
- CHANGELOG.md au format Keep a Changelog
- VERSION (source unique de vérité sémantique)
