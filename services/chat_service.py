from langchain_core.runnables import Runnable


class ChatService:
    def __init__(self, chain: Runnable) -> None:
        self._chain = chain

    def poser_question(self, question: str) -> str:
        return self._chain.invoke({"question": question})
