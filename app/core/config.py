from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/engigraph.db"
    vector_store: str = "in_memory"
    embedder: str = "dummy"
    embedder_model: str = Field(
        default="BAAI/bge-m3",
        validation_alias=AliasChoices("EMBEDDER_MODEL", "EMBEDDING_MODEL"),
    )
    llm_provider: str = "dummy"
    llm_model: str = "dummy"
    openai_api_key: str | None = None
    qdrant_url: str | None = None
    http_verify_ssl: bool = True
    max_article_workers: int = 5
    max_db_writers: int = 1
    max_embedding_workers: int = 2

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
