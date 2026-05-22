"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("sources", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(), nullable=False), sa.Column("company", sa.String(), nullable=False), sa.Column("base_url", sa.String(), nullable=False), sa.Column("feed_url", sa.String()), sa.Column("sitemap_url", sa.String()), sa.Column("allowed_domains", sa.String(), nullable=False), sa.Column("crawl_mode", sa.String(), nullable=False), sa.Column("enabled", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_table("categories", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(), nullable=False, unique=True), sa.Column("slug", sa.String(), nullable=False, unique=True), sa.Column("description", sa.Text()), sa.Column("created_by", sa.String(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_table("articles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=False), sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id")), sa.Column("company", sa.String(), nullable=False), sa.Column("title", sa.String()), sa.Column("url", sa.String(), nullable=False), sa.Column("canonical_url", sa.String(), nullable=False), sa.Column("author_name", sa.String()), sa.Column("published_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()), sa.Column("raw_html", sa.Text()), sa.Column("clean_text", sa.Text(), nullable=False), sa.Column("summary", sa.Text()), sa.Column("content_hash", sa.String(), nullable=False, unique=True), sa.Column("status", sa.String(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_table("article_chunks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("article_id", sa.Integer(), sa.ForeignKey("articles.id"), nullable=False), sa.Column("chunk_index", sa.Integer(), nullable=False), sa.Column("heading", sa.String()), sa.Column("text", sa.Text(), nullable=False), sa.Column("token_count", sa.Integer(), nullable=False), sa.Column("content_hash", sa.String(), nullable=False), sa.Column("vector_id", sa.String()), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("crawl_runs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=False), sa.Column("started_at", sa.DateTime(), nullable=False), sa.Column("finished_at", sa.DateTime()), sa.Column("status", sa.String(), nullable=False), sa.Column("articles_found", sa.Integer(), nullable=False), sa.Column("articles_created", sa.Integer(), nullable=False), sa.Column("articles_updated", sa.Integer(), nullable=False), sa.Column("articles_skipped", sa.Integer(), nullable=False), sa.Column("articles_failed", sa.Integer(), nullable=False), sa.Column("error_message", sa.Text()))
    op.create_table("crawl_items", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("crawl_run_id", sa.Integer(), sa.ForeignKey("crawl_runs.id"), nullable=False), sa.Column("source_id", sa.Integer(), sa.ForeignKey("sources.id"), nullable=False), sa.Column("url", sa.String(), nullable=False), sa.Column("status", sa.String(), nullable=False), sa.Column("article_id", sa.Integer(), sa.ForeignKey("articles.id")), sa.Column("retry_count", sa.Integer(), nullable=False), sa.Column("max_retries", sa.Integer(), nullable=False), sa.Column("error_message", sa.Text()), sa.Column("last_error_at", sa.DateTime()), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("rag_queries", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("original_query", sa.Text(), nullable=False), sa.Column("rewritten_query", sa.Text()), sa.Column("intent", sa.String()), sa.Column("return_type", sa.String()), sa.Column("filters_json", sa.Text()), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("rag_results", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("rag_query_id", sa.Integer(), sa.ForeignKey("rag_queries.id"), nullable=False), sa.Column("article_id", sa.Integer(), sa.ForeignKey("articles.id"), nullable=False), sa.Column("chunk_id", sa.Integer(), sa.ForeignKey("article_chunks.id"), nullable=False), sa.Column("score", sa.Float(), nullable=False), sa.Column("rank", sa.Integer(), nullable=False), sa.Column("result_type", sa.String(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))


def downgrade() -> None:
    for table in ["rag_results", "rag_queries", "crawl_items", "crawl_runs", "article_chunks", "articles", "categories", "sources"]:
        op.drop_table(table)
