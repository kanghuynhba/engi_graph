from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/engigraph.db"
    vector_store: str = "in_memory"
    embedder: str = "dummy"
    llm_provider: str = "dummy"
    llm_model: str = "dummy"
    openai_api_key: str | None = None
    qdrant_url: str | None = None
    max_article_workers: int = 5
    max_db_writers: int = 1
    max_embedding_workers: int = 2

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
