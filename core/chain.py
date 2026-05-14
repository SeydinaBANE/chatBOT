from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from core.prompts import build_chat_prompt


def build_chain(llm: ChatOllama) -> Runnable:
    return build_chat_prompt() | llm | StrOutputParser()
