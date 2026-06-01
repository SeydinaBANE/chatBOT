"""Assemblage des chaînes LCEL (simple et RAG)."""

from typing import Any

from langchain_community.chat_models import ChatOllama
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever

from core.prompts import build_chat_prompt, build_rag_prompt


def build_chain(llm: ChatOllama) -> Runnable:
    """Construit la chaîne de chat simple : prompt | llm | parser.

    Args:
        llm: Instance ChatOllama injectée depuis la factory.

    Returns:
        Runnable exposant .invoke(), .stream() et .batch().
    """
    return build_chat_prompt() | llm | StrOutputParser()


def build_rag_chain(llm: ChatOllama, retriever: VectorStoreRetriever) -> Runnable:
    """Construit la chaîne RAG : récupère le contexte puis génère la réponse.

    Le contexte est récupéré depuis le vector store à partir de la question,
    puis injecté dans le prompt avant la génération.

    Args:
        llm: Instance ChatOllama injectée depuis la factory.
        retriever: Retriever ChromaDB exposant la recherche sémantique.

    Returns:
        Runnable acceptant {"question": str} et retournant la réponse str.
    """

    def _format_docs(docs: list[Document]) -> str:
        return "\n\n".join(d.page_content for d in docs)

    format_docs = RunnableLambda[list[Document], str](_format_docs)

    def _extract_question(x: dict[str, Any]) -> str:
        return x["question"]

    return (
        RunnablePassthrough.assign(
            context=RunnableLambda[dict[str, Any], str](_extract_question) | retriever | format_docs
        )
        | build_rag_prompt()
        | llm
        | StrOutputParser()
    )
