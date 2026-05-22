from app.domain.results import ClassificationResult, IndexingResult


class ArticleIndexingPipeline:
    def __init__(
        self,
        fetcher,
        extractor,
        cleaner,
        deduplicator,
        classifier,
        chunker,
        embedder,
        persistence,
        category_repository,
    ):
        self.fetcher = fetcher
        self.extractor = extractor
        self.cleaner = cleaner
        self.deduplicator = deduplicator
        self.classifier = classifier
        self.chunker = chunker
        self.embedder = embedder
        self.persistence = persistence
        self.category_repository = category_repository

    async def index_url(self, source, url: str) -> IndexingResult:
        try:
            html, final_url = await self.fetcher.fetch(url)
            extracted = self.extractor.extract(html=html, url=final_url)
            clean_text = self.cleaner.clean(extracted.raw_text)
            content_hash = self.deduplicator.hash_content(clean_text)
            existing = self.persistence.article_repository.get_by_content_hash(content_hash)
            if existing:
                return IndexingResult(status="skipped_duplicate", article_id=existing.id, url=url)

            categories = self.category_repository.list_all()
            try:
                classification = self.classifier.classify(
                    title=extracted.title or "",
                    excerpt=extracted.excerpt or "",
                    clean_text_preview=clean_text[:2000],
                    categories=categories,
                )
            except Exception:
                uncategorized = self.category_repository.get_by_slug("uncategorized")
                classification = ClassificationResult(
                    category_id=uncategorized.id if uncategorized else None,
                    category_name="Uncategorized",
                    confidence=0.0,
                    reasoning="classification failed",
                )

            chunk_texts = self.chunker.split(clean_text)
            vectors = self.embedder.embed_texts(chunk_texts)
            return await self.persistence.save_article_and_chunks(
                source=source,
                extracted=extracted,
                clean_text=clean_text,
                content_hash=content_hash,
                classification=classification,
                chunks=chunk_texts,
                vectors=vectors,
            )
        except Exception as exc:
            return IndexingResult(status="failed", article_id=None, url=url, error_message=str(exc))
