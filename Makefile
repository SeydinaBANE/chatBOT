.PHONY: install setup run test lint format typecheck check docker-up docker-down docker-pull

install:
	pip install -r requirements.txt

setup: install
	pre-commit install

run:
	streamlit run main.py

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy . --ignore-missing-imports

check: lint typecheck
	ruff format --check .

docker-pull:
	docker compose run --rm ollama ollama pull tinyllama

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
