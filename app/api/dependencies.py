from dataclasses import dataclass
from functools import cached_property

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.ingestion.crawler import Crawler
from app.repositories.article_chunk_repository import ArticleChunkRepository
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.crawl_run_repository import CrawlRunRepository
from app.repositories.source_repository import SourceRepository
from app.services.article_service import ArticleService
from app.services.category_service import CategoryService
from app.services.factory import build_crawl_run_article_processor, build_indexing_pipeline, build_rag_parts, get_vector_store
from app.services.ingestion_service import IngestionService
from app.services.rag_service import RAGService
from app.services.search_service import SearchService
from app.services.source_service import SourceService


def build_ingestion_service(db: Session, http_client) -> IngestionService:
    return IngestionService(
        SourceRepository(db),
        CrawlRunRepository(db),
        Crawler(http_client),
        build_crawl_run_article_processor(db, http_client),
        build_indexing_pipeline(db, http_client),
    )


@dataclass
class Services:
    db: Session
    request: Request

    @cached_property
    def articles(self) -> ArticleService:
        return ArticleService(ArticleRepository(self.db), ArticleChunkRepository(self.db), get_vector_store())

    @cached_property
    def categories(self) -> CategoryService:
        return CategoryService(CategoryRepository(self.db))

    @cached_property
    def ingestion(self) -> IngestionService:
        return build_ingestion_service(self.db, self.request.app.state.http_client)

    @cached_property
    def rag(self) -> RAGService:
        return RAGService(build_rag_parts(self.db), ArticleRepository(self.db), ArticleChunkRepository(self.db))

    @cached_property
    def search(self) -> SearchService:
        return SearchService(build_rag_parts(self.db), ArticleRepository(self.db))

    @cached_property
    def sources(self) -> SourceService:
        return SourceService(SourceRepository(self.db))


def get_services(request: Request, db: Session = Depends(get_db)) -> Services:
    return Services(db=db, request=request)
