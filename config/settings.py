"""Configuration centralisée chargée depuis les variables d'environnement (.env)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Paramètres de l'application, surchargeables via .env."""

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "tinyllama"
    ollama_temperature: float = 0.7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
