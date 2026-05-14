from langchain_community.embeddings import FastEmbedEmbeddings


class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        self._model_name = model_name

    def get_embeddings(self) -> FastEmbedEmbeddings:
        raise NotImplementedError("RAG — embeddings non encore implémentés")
