import asyncio
import hashlib

from app.domain.results import ArticleExtractionResult, ClassificationResult, IndexingResult


class PersistenceCoordinator:
    def __init__(
        self,
        article_repository,
        chunk_repository,
        vector_store,
        db_write_semaphore: asyncio.Semaphore,
    ):
        self.article_repository = article_repository
        self.chunk_repository = chunk_repository
        self.vector_store = vector_store
        self.db_write_semaphore = db_write_semaphore

    async def save_article_and_chunks(
        self,
        source,
        extracted: ArticleExtractionResult,
        clean_text: str,
        content_hash: str,
        classification: ClassificationResult,
        chunks: list[str],
        vectors: list[list[float]],
    ) -> IndexingResult:
        async with self.db_write_semaphore:
            existing = self.article_repository.get_by_content_hash(content_hash)
            if existing:
                return IndexingResult(status="skipped_duplicate", article_id=existing.id, url=extracted.url)

            article = self.article_repository.create(
                {
                    "source_id": source.id,
                    "category_id": classification.category_id,
                    "company": source.company,
                    "title": extracted.title,
                    "url": extracted.url,
                    "canonical_url": extracted.canonical_url or extracted.url,
                    "author_name": extracted.author_name,
                    "published_at": extracted.published_at,
                    "updated_at": extracted.updated_at,
                    "raw_html": None,
                    "clean_text": clean_text,
                    "summary": None,
                    "content_hash": content_hash,
                    "status": "processed",
                }
            )

            saved_chunks = self.chunk_repository.bulk_create(
                [
                    {
                        "article_id": article.id,
                        "chunk_index": i,
                        "heading": None,
                        "text": text,
                        "token_count": len(text.split()),
                        "content_hash": hashlib.sha256(text.encode()).hexdigest(),
                    }
                    for i, text in enumerate(chunks)
                ]
            )

            for chunk, vector in zip(saved_chunks, vectors):
                vector_id = f"article-{article.id}-chunk-{chunk.id}"
                self.vector_store.upsert_vector(
                    vector_id=vector_id,
                    vector=vector,
                    payload={
                        "source_id": source.id,
                        "article_id": article.id,
                        "chunk_id": chunk.id,
                        "company": source.company,
                        "source_name": source.name,
                        "category_id": classification.category_id,
                        "category_name": classification.category_name,
                        "title": article.title,
                        "url": article.url,
                        "canonical_url": article.canonical_url,
                        "published_at": article.published_at.isoformat() if article.published_at else None,
                        "chunk_index": chunk.chunk_index,
                        "heading": chunk.heading,
                        "text": chunk.text,
                    },
                )
                self.chunk_repository.update_vector_id(chunk.id, vector_id)

            return IndexingResult(status="processed", article_id=article.id, url=extracted.url)
