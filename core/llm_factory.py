"""Factory de création du modèle de langage (LLM)."""

from langchain_community.chat_models import ChatOllama

from config.settings import Settings


def create_llm(settings: Settings) -> ChatOllama:
    """Instancie un ChatOllama à partir de la configuration.

    Args:
        settings: Objet Settings contenant l'URL, le modèle et la température.

    Returns:
        Instance ChatOllama prête à l'emploi.
    """
    return ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        temperature=settings.ollama_temperature,
    )
