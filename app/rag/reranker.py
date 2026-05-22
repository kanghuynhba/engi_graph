from abc import ABC, abstractmethod

from app.domain.results import RetrievedChunk


class Reranker(ABC):
    @abstractmethod
    def rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        raise NotImplementedError


class ScoreReranker(Reranker):
    def rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        del query
        return sorted(chunks, key=lambda c: c.score, reverse=True)
