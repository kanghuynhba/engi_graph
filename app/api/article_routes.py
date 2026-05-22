from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.article_chunk_repository import ArticleChunkRepository
from app.repositories.article_repository import ArticleRepository
from app.schemas.article_schema import ArticleChunkResponse, ArticleDetailResponse, ArticleResponse
from app.services.article_service import ArticleService
from app.services.factory import get_vector_store

router = APIRouter(prefix="/api/articles", tags=["articles"])


def get_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(ArticleRepository(db), ArticleChunkRepository(db), get_vector_store())


@router.get("", response_model=list[ArticleResponse])
def list_articles(limit: int = 100, offset: int = 0, service: ArticleService = Depends(get_service)):
    return [ArticleResponse.from_article(article) for article in service.list_articles(limit, offset)]


@router.get("/{article_id}", response_model=ArticleDetailResponse)
def get_article(article_id: int, service: ArticleService = Depends(get_service)):
    article = service.get_article(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleDetailResponse(**ArticleResponse.from_article(article).model_dump(), clean_text=article.clean_text, summary=article.summary)


@router.get("/{article_id}/chunks", response_model=list[ArticleChunkResponse])
def get_article_chunks(article_id: int, service: ArticleService = Depends(get_service)):
    return service.get_article_chunks(article_id)


@router.delete("/{article_id}")
def delete_article(article_id: int, service: ArticleService = Depends(get_service)):
    service.delete_article(article_id)
    return {"status": "deleted"}
