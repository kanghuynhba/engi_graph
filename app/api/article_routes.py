from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import Services, get_services
from app.schemas.article_schema import ArticleChunkResponse, ArticleDetailResponse, ArticleResponse

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("", response_model=list[ArticleResponse])
def list_articles(limit: int = 100, offset: int = 0, services: Services = Depends(get_services)):
    return [ArticleResponse.from_article(article) for article in services.articles.list_articles(limit, offset)]


@router.get("/{article_id}", response_model=ArticleDetailResponse)
def get_article(article_id: int, services: Services = Depends(get_services)):
    article = services.articles.get_article(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleDetailResponse(**ArticleResponse.from_article(article).model_dump(), clean_text=article.clean_text, summary=article.summary)


@router.get("/{article_id}/chunks", response_model=list[ArticleChunkResponse])
def get_article_chunks(article_id: int, services: Services = Depends(get_services)):
    return services.articles.get_article_chunks(article_id)


@router.delete("/{article_id}")
def delete_article(article_id: int, services: Services = Depends(get_services)):
    services.articles.delete_article(article_id)
    return {"status": "deleted"}
