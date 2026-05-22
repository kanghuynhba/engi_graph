from app.domain.results import CitedSource, RetrievedChunk


class ContextBuilder:
    def build(self, question: str, chunks: list[RetrievedChunk], max_tokens: int = 6000) -> tuple[str, list[CitedSource]]:
        del question
        parts = []
        sources = []
        token_count = 0
        for index, chunk in enumerate(chunks):
            chunk_tokens = len(chunk.text.split())
            if token_count + chunk_tokens > max_tokens:
                break
            token_count += chunk_tokens
            category = chunk.category_name or "Uncategorized"
            parts.append(f"[Source {index + 1}] {chunk.title} - {chunk.company} [{category}]\nURL: {chunk.url}\n{chunk.text}\n---")
            sources.append(
                CitedSource(
                    article_id=chunk.article_id,
                    chunk_id=chunk.chunk_id,
                    title=chunk.title,
                    url=chunk.url,
                    company=chunk.company,
                    source_name=chunk.company,
                    category_name=chunk.category_name,
                    published_at=chunk.published_at,
                    chunk_excerpt=chunk.text[:500],
                    score=chunk.score,
                )
            )
        return "\n".join(parts), sources
