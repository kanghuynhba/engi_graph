from pydantic import BaseModel


class SearchChunksRequest(BaseModel):
    query: str
    companies: list[str] | None = None
    category_names: list[str] | None = None
    published_after: str | None = None
    published_before: str | None = None
    top_k: int = 10


class SearchChunkResponse(BaseModel):
    chunk_id: int
    article_id: int
    title: str
    company: str
    category_name: str | None
    url: str
    text: str
    score: float
    rank: int


class SearchArticlesRequest(BaseModel):
    query: str
    companies: list[str] | None = None
    category_names: list[str] | None = None
    top_k: int = 10


class SearchArticleResponse(BaseModel):
    article_id: int
    title: str
    company: str
    category_name: str | None
    url: str
    matched_chunk_count: int
    best_score: float
