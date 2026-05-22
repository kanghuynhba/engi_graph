from app.vectorstores.base import VectorStore


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._vectors: dict[str, tuple[list[float], dict]] = {}

    def upsert_vector(self, vector_id: str, vector: list[float], payload: dict) -> None:
        self._vectors[vector_id] = (vector, payload)

    def search(self, query_vector: list[float], filters: dict, top_k: int) -> list[dict]:
        del query_vector
        results = []
        for vector_id, (vector, payload) in self._vectors.items():
            del vector
            if self._matches_filters(payload, filters):
                results.append({"id": vector_id, "score": 1.0, "payload": payload})
        return results[:top_k]

    def delete_vector(self, vector_id: str) -> None:
        self._vectors.pop(vector_id, None)

    def delete_by_article(self, article_id: int) -> None:
        for vector_id in [key for key, (_, payload) in self._vectors.items() if payload.get("article_id") == article_id]:
            self.delete_vector(vector_id)

    def _matches_filters(self, payload: dict, filters: dict | None) -> bool:
        if not filters:
            return True
        companies = filters.get("companies")
        if companies and payload.get("company") not in companies:
            return False
        category_ids = filters.get("category_ids")
        if category_ids and payload.get("category_id") not in category_ids:
            return False
        category_names = filters.get("category_names")
        if category_names and payload.get("category_name") not in category_names:
            return False
        published_at = payload.get("published_at")
        if filters.get("published_after") and published_at and published_at < filters["published_after"]:
            return False
        if filters.get("published_before") and published_at and published_at > filters["published_before"]:
            return False
        return True
