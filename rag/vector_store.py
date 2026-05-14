from langchain_core.vectorstores import VectorStoreRetriever


class VectorStore:
    def get_retriever(self) -> VectorStoreRetriever:
        raise NotImplementedError("RAG — vector store non encore implémenté")
