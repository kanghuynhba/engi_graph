from sentence_transformers import SentenceTransformer

from app.embeddings.base import Embedder


class LocalEmbedder(Embedder):
    def __init__(self, model_name: str = "BAAI/bge-m3") -> None:
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )
        return embedding.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=8,
        )
        return [embedding.tolist() for embedding in embeddings]
