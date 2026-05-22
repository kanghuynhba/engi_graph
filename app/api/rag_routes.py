from dataclasses import asdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.article_chunk_repository import ArticleChunkRepository
from app.repositories.article_repository import ArticleRepository
from app.schemas.rag_schema import AskRequest, AskResponse, CitedSourceResponse, QueryPlanResponse
from app.services.factory import build_rag_parts
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/rag", tags=["rag"])


def get_service(db: Session = Depends(get_db)) -> RAGService:
    return RAGService(build_rag_parts(db), ArticleRepository(db), ArticleChunkRepository(db))


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, service: RAGService = Depends(get_service)):
    answer, sources, plan = service.ask(
        payload.question,
        {"companies": payload.companies, "category_names": payload.category_names},
        payload.top_k,
    )
    return AskResponse(
        answer=answer,
        sources=[CitedSourceResponse(**asdict(source)) for source in sources] if payload.return_sources else [],
        query_plan=QueryPlanResponse(**asdict(plan)),
    )


@router.post("/query-plan", response_model=QueryPlanResponse)
def query_plan(payload: AskRequest, service: RAGService = Depends(get_service)):
    return QueryPlanResponse(**asdict(service.create_query_plan(payload.question)))


@router.post("/answer-from-article/{article_id}", response_model=AskResponse)
def answer_from_article(article_id: int, payload: AskRequest, service: RAGService = Depends(get_service)):
    answer, sources, plan = service.answer_from_article(article_id, payload.question)
    return AskResponse(
        answer=answer,
        sources=[CitedSourceResponse(**asdict(source)) for source in sources] if payload.return_sources else [],
        query_plan=QueryPlanResponse(**asdict(plan)),
    )
