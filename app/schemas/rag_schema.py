from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    companies: list[str] | None = None
    category_names: list[str] | None = None
    top_k: int = 10
    return_sources: bool = True


class CitedSourceResponse(BaseModel):
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


class QueryPlanResponse(BaseModel):
    original_query: str
    rewritten_query: str
    intent: str
    return_type: str
    filters: dict
    generated_queries: list[str]


class AskResponse(BaseModel):
    answer: str
    sources: list[CitedSourceResponse]
    query_plan: QueryPlanResponse | None = None
