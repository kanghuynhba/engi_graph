from fastapi import APIRouter, Depends

from app.api.dependencies import Services, get_services
from app.schemas.article_schema import ArticleDetailResponse, ArticleResponse
from app.schemas.search_schema import SearchArticleResponse, SearchArticlesRequest, SearchChunkResponse, SearchChunksRequest

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/chunks", response_model=list[SearchChunkResponse])
def search_chunks(payload: SearchChunksRequest, services: Services = Depends(get_services)):
    filters = payload.model_dump(exclude={"query", "top_k"})
    chunks = services.search.search_chunks(payload.query, filters, payload.top_k)
    return [
        SearchChunkResponse(
            chunk_id=chunk.chunk_id,
            article_id=chunk.article_id,
            title=chunk.title,
            company=chunk.company,
            category_name=chunk.category_name,
            url=chunk.url,
            text=chunk.text,
            score=chunk.score,
            rank=index + 1,
        )
        for index, chunk in enumerate(chunks)
    ]


@router.post("/articles", response_model=list[SearchArticleResponse])
def search_articles(payload: SearchArticlesRequest, services: Services = Depends(get_services)):
    filters = payload.model_dump(exclude={"query", "top_k"})
    return [
        SearchArticleResponse(**article.__dict__)
        for article in services.search.search_articles(payload.query, filters, payload.top_k)
    ]


@router.post("/full-article", response_model=ArticleDetailResponse | None)
def full_article(payload: SearchArticlesRequest, services: Services = Depends(get_services)):
    article = services.search.get_best_full_article(payload.query, payload.model_dump(exclude={"query", "top_k"}))
    if article is None:
        return None
    base = ArticleResponse.from_article(article).model_dump()
    return ArticleDetailResponse(**base, clean_text=article.clean_text, summary=article.summary)
