from app.domain.results import RetrievedChunk


class Retriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, queries: list[str], filters: dict, top_k: int) -> list[RetrievedChunk]:
        all_chunks = []
        seen_chunk_ids = set()
        for query in queries:
            vector = self.embedder.embed_text(query)
            raw_results = self.vector_store.search(vector, filters, top_k)
            for result in raw_results:
                payload = result["payload"]
                chunk_id = payload["chunk_id"]
                if chunk_id in seen_chunk_ids:
                    continue
                seen_chunk_ids.add(chunk_id)
                all_chunks.append(
                    RetrievedChunk(
                        chunk_id=payload["chunk_id"],
                        article_id=payload["article_id"],
                        source_id=payload["source_id"],
                        company=payload["company"],
                        category_id=payload.get("category_id"),
                        category_name=payload.get("category_name"),
                        title=payload["title"],
                        url=payload["url"],
                        text=payload.get("text", ""),
                        score=result["score"],
                        chunk_index=payload["chunk_index"],
                        published_at=payload.get("published_at"),
                        heading=payload.get("heading"),
                    )
                )
        return all_chunks
