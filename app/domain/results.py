from dataclasses import dataclass
from datetime import datetime


@dataclass
class ArticleExtractionResult:
    url: str
    canonical_url: str | None
    title: str | None
    author_name: str | None
    published_at: datetime | None
    updated_at: datetime | None
    raw_text: str
    excerpt: str | None
    language: str | None


@dataclass
class ClassificationResult:
    category_id: int | None
    category_name: str
    confidence: float
    reasoning: str | None


@dataclass
class IndexingResult:
    status: str
    article_id: int | None
    url: str
    error_message: str | None = None


@dataclass
class RetrievedChunk:
    chunk_id: int
    article_id: int
    source_id: int
    company: str
    category_id: int | None
    category_name: str | None
    title: str
    url: str
    text: str
    score: float
    chunk_index: int
    published_at: str | None
    heading: str | None


@dataclass
class RankedArticle:
    article_id: int
    title: str
    company: str
    category_name: str | None
    url: str
    matched_chunk_count: int
    best_score: float
    aggregate_score: float


@dataclass
class CitedSource:
    article_id: int
    chunk_id: int
    title: str
    url: str
    company: str
    source_name: str
    category_name: str | None
    published_at: str | None
    chunk_excerpt: str
    score: float


@dataclass
class QueryPlan:
    original_query: str
    rewritten_query: str
    intent: str
    return_type: str
    filters: dict
    generated_queries: list[str]
