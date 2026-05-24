import httpx
import certifi
from fastapi import FastAPI

from app.api import article_routes, category_routes, ingestion_routes, rag_routes, search_routes, source_routes
from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine
from app.core.logging import configure_logging
from app.services.factory import rebuild_in_memory_vector_store
from data.seeds import seed_categories_and_sources


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="EngiGraph", version="1.0.0")
    app.include_router(source_routes.router)
    app.include_router(category_routes.router)
    app.include_router(ingestion_routes.router)
    app.include_router(article_routes.router)
    app.include_router(search_routes.router)
    app.include_router(rag_routes.router)

    @app.on_event("startup")
    async def startup() -> None:
        settings = get_settings()
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_categories_and_sources(db)
            rebuild_in_memory_vector_store(db)
        finally:
            db.close()
        app.state.http_client = httpx.AsyncClient(
            timeout=30.0,
            verify=certifi.where() if settings.http_verify_ssl else False,
        )

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await app.state.http_client.aclose()

    return app


app = create_app()
