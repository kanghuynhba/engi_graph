from app.embeddings.base import Embedder


class DummyEmbedder(Embedder):
    def embed_text(self, text: str) -> list[float]:
        del text
        return [0.0] * 384

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]
