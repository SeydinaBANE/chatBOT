from langchain_community.chat_models import ChatOllama
from config.settings import Settings


def create_llm(settings: Settings) -> ChatOllama:
    return ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        temperature=settings.ollama_temperature,
    )
