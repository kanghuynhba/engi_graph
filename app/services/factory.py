import asyncio
import logging

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.embeddings.dummy_embedder import DummyEmbedder
from app.ingestion.chunker import Chunker
from app.ingestion.classifier import CategoryClassifier
from app.ingestion.cleaner import ArticleCleaner
from app.ingestion.crawler import Crawler
from app.ingestion.deduplicator import Deduplicator
from app.ingestion.extractor import FallbackContentExtractor
from app.ingestion.fetcher import AsyncHTMLFetcher
from app.ingestion.crawl_run_article_processor import CrawlRunArticleProcessor
from app.ingestion.persistence import PersistenceCoordinator
from app.ingestion.pipeline import ArticleIndexingPipeline
from app.llm.dummy_llm import DummyLLMClient
from app.rag.answer_generator import AnswerGenerator
from app.rag.article_aggregator import ArticleAggregator
from app.rag.context_builder import ContextBuilder
from app.rag.filter_extractor import MetadataFilterExtractor
from app.rag.multi_query_generator import MultiQueryGenerator
from app.rag.query_analyzer import QueryAnalyzer
from app.rag.query_rewriter import QueryRewriter
from app.rag.reranker import ScoreReranker
from app.rag.retriever import Retriever
from app.repositories.article_chunk_repository import ArticleChunkRepository
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.crawl_item_repository import CrawlItemRepository
from app.repositories.crawl_run_repository import CrawlRunRepository
from app.repositories.rag_query_repository import RAGQueryRepository
from app.repositories.rag_result_repository import RAGResultRepository
from app.repositories.source_repository import SourceRepository
from app.services.ingestion_service import IngestionService
from app.vectorstores.in_memory_store import InMemoryVectorStore
from app.models.article_chunk import ArticleChunk


_vector_store = InMemoryVectorStore()
_db_write_semaphore: asyncio.Semaphore | None = None
_embedder = None
logger = logging.getLogger(__name__)


def get_embedder():
    global _embedder
    if _embedder is not None:
        return _embedder

    settings = get_settings()

    if settings.embedder == "local":
        try:
            from app.embeddings.local_embedder import LocalEmbedder

            _embedder = LocalEmbedder(model_name=settings.embedder_model)
            return _embedder
        except ModuleNotFoundError as exc:
            if exc.name != "sentence_transformers":
                raise
            logger.warning("EMBEDDER=local requires sentence-transformers; falling back to DummyEmbedder")

    _embedder = DummyEmbedder()
    return _embedder

def get_llm_client():
    return DummyLLMClient()


def get_vector_store():
    return _vector_store


def rebuild_in_memory_vector_store(db: Session) -> int:
    vector_store = get_vector_store()
    if not isinstance(vector_store, InMemoryVectorStore) or vector_store.count() > 0:
        return 0

    chunks = db.query(ArticleChunk).order_by(ArticleChunk.id).all()
    if not chunks:
        return 0

    embedder = get_embedder()
    vectors = embedder.embed_texts([chunk.text for chunk in chunks])
    rebuilt = 0
    for chunk, vector in zip(chunks, vectors):
        article = chunk.article
        if article is None:
            continue
        source = article.source
        category = article.category
        vector_id = chunk.vector_id or f"article-{article.id}-chunk-{chunk.id}"
        chunk.vector_id = vector_id
        vector_store.upsert_vector(
            vector_id=vector_id,
            vector=vector,
            payload={
                "source_id": article.source_id,
                "article_id": article.id,
                "chunk_id": chunk.id,
                "company": article.company,
                "source_name": source.name if source else article.company,
                "category_id": article.category_id,
                "category_name": category.name if category else None,
                "title": article.title,
                "url": article.url,
                "canonical_url": article.canonical_url,
                "published_at": article.published_at.isoformat() if article.published_at else None,
                "chunk_index": chunk.chunk_index,
                "heading": chunk.heading,
                "text": chunk.text,
            },
        )
        rebuilt += 1
    db.commit()
    logger.info("Rebuilt %s in-memory vectors from SQLite", rebuilt)
    return rebuilt


def get_db_write_semaphore() -> asyncio.Semaphore:
    global _db_write_semaphore
    if _db_write_semaphore is None:
        _db_write_semaphore = asyncio.Semaphore(get_settings().max_db_writers)
    return _db_write_semaphore


def build_indexing_pipeline(db: Session, http_client) -> ArticleIndexingPipeline:
    article_repo = ArticleRepository(db)
    chunk_repo = ArticleChunkRepository(db)
    category_repo = CategoryRepository(db)
    persistence = PersistenceCoordinator(article_repo, chunk_repo, get_vector_store(), get_db_write_semaphore())
    return ArticleIndexingPipeline(
        AsyncHTMLFetcher(http_client),
        FallbackContentExtractor(),
        ArticleCleaner(),
        Deduplicator(),
        CategoryClassifier(get_llm_client()),
        Chunker(),
        get_embedder(),
        persistence,
        category_repo,
    )


def build_crawl_run_article_processor(
    db: Session,
    http_client,
    indexing_pipeline: ArticleIndexingPipeline | None = None,
) -> CrawlRunArticleProcessor:
    return CrawlRunArticleProcessor(
        indexing_pipeline or build_indexing_pipeline(db, http_client),
        CrawlItemRepository(db),
        CrawlRunRepository(db),
        max_workers=get_settings().max_article_workers,
    )


def build_ingestion_service(db: Session, http_client) -> IngestionService:
    pipeline = build_indexing_pipeline(db, http_client)
    return IngestionService(
        SourceRepository(db),
        CrawlRunRepository(db),
        Crawler(http_client),
        build_crawl_run_article_processor(db, http_client, pipeline),
        pipeline,
    )


def build_rag_parts(db: Session) -> dict:
    llm = get_llm_client()
    analyzer = QueryAnalyzer()
    rewriter = QueryRewriter(llm)
    generator = MultiQueryGenerator(llm)
    filters = MetadataFilterExtractor(CategoryRepository(db))
    retriever = Retriever(get_embedder(), get_vector_store())
    reranker = ScoreReranker()
    return {
        "analyzer": analyzer,
        "rewriter": rewriter,
        "generator": generator,
        "filters": filters,
        "retriever": retriever,
        "reranker": reranker,
        "aggregator": ArticleAggregator(),
        "context_builder": ContextBuilder(),
        "answer_generator": AnswerGenerator(llm),
        "rag_query_repo": RAGQueryRepository(db),
        "rag_result_repo": RAGResultRepository(db),
    }
