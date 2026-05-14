"""Définitions des prompts LangChain utilisés par la chaîne."""

from langchain_core.prompts import ChatPromptTemplate


def build_chat_prompt() -> ChatPromptTemplate:
    """Construit le prompt de conversation en français.

    Returns:
        ChatPromptTemplate avec un message système et un tour humain ({question}).
    """
    return ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant utile. Réponds en français de manière claire et concise."),
        ("human", "{question}"),
    ])
