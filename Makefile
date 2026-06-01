.PHONY: help install setup run test coverage lint format typecheck check security clean build \
        docker-up docker-down docker-pull docker-build docker-push all

.DEFAULT_GOAL := help

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installe les dépendances Python
	pip install -r requirements.txt

setup: install ## Installe les dépendances + pre-commit hooks
	pre-commit install

run: ## Lance l'application en local
	streamlit run main.py

test: ## Lance les tests unitaires
	pytest -v

coverage: ## Lance les tests avec rapport de couverture
	pytest --cov --cov-report=term-missing

lint: ## Vérifie le code avec ruff
	ruff check .

format: ## Formate le code avec ruff
	ruff format .

typecheck: ## Vérifie les types avec mypy
	mypy . --ignore-missing-imports

check: lint typecheck format ## Exécute lint + typecheck + format (dry-run)
	ruff format --check .

security: ## Analyse de sécurité (bandit + safety + pip-audit)
	bandit --quiet --recursive --skip=B101 config/ core/ services/ rag/ ui/
	safety check --bare 2>/dev/null || true
	pip-audit 2>/dev/null || true

clean: ## Nettoie les artefacts Python
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .coverage htmlcov

docker-build: ## Build l'image Docker
	docker compose build

docker-push: ## Push l'image sur ghcr.io
	docker compose push

docker-pull: ## Télécharge le modèle Ollama
	docker compose run --rm ollama ollama pull tinyllama

docker-up: ## Démarre les conteneurs
	docker compose up --build -d

docker-down: ## Arrête les conteneurs
	docker compose down

all: check test coverage security ## Exécute toutes les vérifications
	@echo "✅ Tout est OK"
