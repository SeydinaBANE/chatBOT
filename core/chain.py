"""Assemblage de la chaîne LCEL (LangChain Expression Language)."""

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from core.prompts import build_chat_prompt


def build_chain(llm: ChatOllama) -> Runnable:
    """Construit la chaîne LCEL : prompt | llm | parser.

    Args:
        llm: Instance ChatOllama injectée depuis la factory.

    Returns:
        Runnable exposant .invoke(), .stream() et .batch().
    """
    return build_chat_prompt() | llm | StrOutputParser()
