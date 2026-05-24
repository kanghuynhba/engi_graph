from app.ingestion.crawler import Crawler


class IngestionService:
    def __init__(
        self,
        source_repository,
        crawl_run_repository,
        crawler: Crawler,
        article_processor,
        indexing_pipeline,
    ):
        self.source_repository = source_repository
        self.crawl_run_repository = crawl_run_repository
        self.crawler = crawler
        self.article_processor = article_processor
        self.indexing_pipeline = indexing_pipeline

    async def crawl_source(self, source_id: int):
        source, crawl_run = self.create_crawl_run(source_id)
        await self.process_crawl_run(source, crawl_run)
        return self.crawl_run_repository.get_by_id(crawl_run.id)

    def create_crawl_run(self, source_id: int):
        source = self.source_repository.get_by_id(source_id)
        if source is None:
            raise ValueError("Source not found")
        return source, self.crawl_run_repository.create(source_id)

    async def process_crawl_run_by_id(self, source_id: int, crawl_run_id: int):
        source = self.source_repository.get_by_id(source_id)
        crawl_run = self.crawl_run_repository.get_by_id(crawl_run_id)
        if source is None:
            raise ValueError("Source not found")
        if crawl_run is None:
            raise ValueError("Crawl run not found")
        return await self.process_crawl_run(source, crawl_run)

    async def process_crawl_run(self, source, crawl_run):
        try:
            urls = await self.crawler.discover_urls(source)
            self.crawl_run_repository.update_articles_found(crawl_run.id, len(urls))
            summary = await self.article_processor.process_urls(source, crawl_run, urls)
            if summary["articles_failed"]:
                self.crawl_run_repository.mark_partial_success(crawl_run.id, summary)
            else:
                self.crawl_run_repository.mark_success(crawl_run.id, summary)
        except Exception as exc:
            self.crawl_run_repository.mark_failed(crawl_run.id, str(exc))
        return self.crawl_run_repository.get_by_id(crawl_run.id)

    async def ingest_url(self, source_id: int, url: str):
        source = self.source_repository.get_by_id(source_id)
        if source is None:
            raise ValueError("Source not found")
        return await self.indexing_pipeline.index_url(source, url)
