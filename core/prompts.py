"""Définitions des prompts LangChain utilisés par les chaînes."""

from langchain_core.prompts import ChatPromptTemplate


def build_chat_prompt() -> ChatPromptTemplate:
    """Construit le prompt de conversation simple en français.

    Returns:
        ChatPromptTemplate avec un message système et un tour humain ({question}).
    """
    return ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant utile. Réponds en français de manière claire et concise."),
        ("human", "{question}"),
    ])


def build_rag_prompt() -> ChatPromptTemplate:
    """Construit le prompt RAG : répond uniquement à partir du contexte fourni.

    Returns:
        ChatPromptTemplate avec variables {context} et {question}.
    """
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "Tu es un assistant utile. Réponds en français uniquement à partir du contexte fourni. "
            "Si la réponse ne se trouve pas dans le contexte, dis-le clairement.\n\n"
            "Contexte :\n{context}",
        ),
        ("human", "{question}"),
    ])
