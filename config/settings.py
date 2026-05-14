"""Configuration centralisée chargée depuis les variables d'environnement (.env)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Paramètres de l'application, surchargeables via .env."""

    # LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "tinyllama"
    ollama_temperature: float = 0.7

    # RAG
    chroma_persist_dir: str = "./chroma_db"
    embed_model: str = "BAAI/bge-small-en-v1.5"
    rag_chunk_size: int = 1000
    rag_chunk_overlap: int = 200
    rag_retriever_k: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
