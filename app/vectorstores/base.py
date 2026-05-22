from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    def upsert_vector(self, vector_id: str, vector: list[float], payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query_vector: list[float], filters: dict, top_k: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def delete_vector(self, vector_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_article(self, article_id: int) -> None:
        raise NotImplementedError
