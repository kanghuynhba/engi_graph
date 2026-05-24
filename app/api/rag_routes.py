from dataclasses import asdict

from fastapi import APIRouter, Depends

from app.api.dependencies import Services, get_services
from app.schemas.rag_schema import AskRequest, AskResponse, CitedSourceResponse, QueryPlanResponse

router = APIRouter(prefix="/api/rag", tags=["rag"])


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, services: Services = Depends(get_services)):
    answer, sources, plan = services.rag.ask(
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
def query_plan(payload: AskRequest, services: Services = Depends(get_services)):
    return QueryPlanResponse(**asdict(services.rag.create_query_plan(payload.question)))


@router.post("/answer-from-article/{article_id}", response_model=AskResponse)
def answer_from_article(article_id: int, payload: AskRequest, services: Services = Depends(get_services)):
    answer, sources, plan = services.rag.answer_from_article(article_id, payload.question)
    return AskResponse(
        answer=answer,
        sources=[CitedSourceResponse(**asdict(source)) for source in sources] if payload.return_sources else [],
        query_plan=QueryPlanResponse(**asdict(plan)),
    )
