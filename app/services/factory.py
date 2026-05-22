import asyncio

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.embeddings.dummy_embedder import DummyEmbedder
from app.ingestion.chunker import Chunker
from app.ingestion.classifier import CategoryClassifier
from app.ingestion.cleaner import ArticleCleaner
from app.ingestion.deduplicator import Deduplicator
from app.ingestion.extractor import FallbackContentExtractor
from app.ingestion.fetcher import AsyncHTMLFetcher
from app.ingestion.orchestrator import AsyncIngestionOrchestrator
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
from app.vectorstores.in_memory_store import InMemoryVectorStore


_vector_store = InMemoryVectorStore()
_db_write_semaphore: asyncio.Semaphore | None = None


def get_embedder():
    return DummyEmbedder()


def get_llm_client():
    return DummyLLMClient()


def get_vector_store():
    return _vector_store


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


def build_orchestrator(db: Session, http_client) -> AsyncIngestionOrchestrator:
    return AsyncIngestionOrchestrator(
        build_indexing_pipeline(db, http_client),
        CrawlItemRepository(db),
        CrawlRunRepository(db),
        max_workers=get_settings().max_article_workers,
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
