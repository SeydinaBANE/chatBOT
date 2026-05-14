# ChatBot Ollama + LangChain

Chatbot en Python avec architecture modulaire, utilisant LangChain (LCEL), le modèle LLaMA via Ollama, et une interface Streamlit.

## Fonctionnalités

- Questions en langage naturel avec réponses en français
- Modèle LLM local via Ollama (aucune API externe)
- Interface web Streamlit avec historique de conversation
- Architecture modulaire extensible (scaffold RAG inclus)
- Configuration externalisée via `.env`

## Prérequis

- Python 3.10+
- [Ollama](https://ollama.com) installé et en cours d'exécution

## Installation

```bash
git clone https://github.com/ton_utilisateur/nom_du_depot.git
cd nom_du_depot

cp .env.example .env
pip install -r requirements.txt
ollama pull tinyllama
```

## Utilisation

```bash
streamlit run main.py
```

## Configuration

Les paramètres sont dans `.env` (copié depuis `.env.example`) :

| Variable | Défaut | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | URL du serveur Ollama |
| `OLLAMA_MODEL` | `tinyllama` | Modèle à utiliser |
| `OLLAMA_TEMPERATURE` | `0.7` | Température de génération |

## Structure du projet

```
main.py              ← point d'entrée
config/settings.py   ← configuration centralisée
core/                ← logique LangChain (LCEL)
services/            ← API publique du chatbot
ui/                  ← interface Streamlit
rag/                 ← scaffold RAG (PDF + embeddings + vector store)
```
