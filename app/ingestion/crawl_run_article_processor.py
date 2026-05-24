import asyncio


class CrawlRunArticleProcessor:
    def __init__(
        self,
        indexing_pipeline,
        crawl_item_repository,
        crawl_run_repository,
        max_workers: int = 5,
    ):
        self.indexing_pipeline = indexing_pipeline
        self.crawl_item_repository = crawl_item_repository
        self.crawl_run_repository = crawl_run_repository
        self.max_workers = max_workers

    async def process_urls(self, source, crawl_run, article_urls: list[str]) -> dict:
        queue: asyncio.Queue[int] = asyncio.Queue()
        for url in article_urls:
            crawl_item = self.crawl_item_repository.create(
                {
                    "crawl_run_id": crawl_run.id,
                    "source_id": source.id,
                    "url": url,
                    "status": "discovered",
                }
            )
            await queue.put(crawl_item.id)

        workers = [
            asyncio.create_task(self._worker(source, queue))
            for _ in range(min(self.max_workers, len(article_urls)))
        ]
        await queue.join()
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
        return self._build_summary(crawl_run.id)

    async def _worker(self, source, queue: asyncio.Queue):
        while True:
            crawl_item_id = await queue.get()
            try:
                self.crawl_item_repository.mark_processing(crawl_item_id)
                crawl_item = self.crawl_item_repository.get_by_id(crawl_item_id)
                result = await self.indexing_pipeline.index_url(source=source, url=crawl_item.url)
                if result.status == "processed":
                    self.crawl_item_repository.mark_processed(crawl_item_id, result.article_id)
                    self.crawl_run_repository.increment_stat(crawl_item.crawl_run_id, "articles_created")
                elif result.status == "skipped_duplicate":
                    self.crawl_item_repository.mark_skipped_duplicate(crawl_item_id, result.article_id)
                    self.crawl_run_repository.increment_stat(crawl_item.crawl_run_id, "articles_skipped")
                else:
                    self.crawl_item_repository.mark_failed(crawl_item_id, result.error_message or "indexing failed")
                    self.crawl_run_repository.increment_stat(crawl_item.crawl_run_id, "articles_failed")
            except Exception as exc:
                crawl_item = self.crawl_item_repository.get_by_id(crawl_item_id)
                if crawl_item and crawl_item.retry_count < crawl_item.max_retries:
                    self.crawl_item_repository.increment_retry(crawl_item_id, str(exc))
                elif crawl_item:
                    self.crawl_item_repository.mark_failed(crawl_item_id, str(exc))
                    self.crawl_run_repository.increment_stat(crawl_item.crawl_run_id, "articles_failed")
            finally:
                queue.task_done()

    def _build_summary(self, crawl_run_id: int) -> dict:
        run = self.crawl_run_repository.get_by_id(crawl_run_id)
        return {
            "articles_found": run.articles_found,
            "articles_created": run.articles_created,
            "articles_updated": run.articles_updated,
            "articles_skipped": run.articles_skipped,
            "articles_failed": run.articles_failed,
        }
