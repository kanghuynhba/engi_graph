import json

from app.domain.results import QueryPlan, RetrievedChunk


class RAGService:
    def __init__(self, parts: dict, article_repository, chunk_repository):
        self.parts = parts
        self.article_repository = article_repository
        self.chunk_repository = chunk_repository

    def create_query_plan(self, question: str) -> QueryPlan:
        analysis = self.parts["analyzer"].analyze(question)
        rewritten = self.parts["rewriter"].rewrite(question, analysis)
        generated = self.parts["generator"].generate(question, rewritten, analysis["intent"])
        filters = self.parts["filters"].extract(question, analysis)
        return QueryPlan(question, rewritten, analysis["intent"], analysis["return_type"], filters, generated)

    def ask(self, question: str, filters: dict | None, top_k: int):
        plan = self.create_query_plan(question)
        effective_filters = plan.filters.copy()
        effective_filters.update({key: value for key, value in (filters or {}).items() if value is not None})
        query_row = self.parts["rag_query_repo"].create(
            {
                "original_query": question,
                "rewritten_query": plan.rewritten_query,
                "intent": plan.intent,
                "return_type": plan.return_type,
                "filters_json": json.dumps(effective_filters),
            }
        )
        chunks = self.parts["retriever"].retrieve(plan.generated_queries, effective_filters, top_k)
        if not chunks and (effective_filters.get("category_ids") or effective_filters.get("category_names")):
            relaxed_filters = effective_filters.copy()
            relaxed_filters["category_ids"] = None
            relaxed_filters["category_names"] = None
            chunks = self.parts["retriever"].retrieve(plan.generated_queries, relaxed_filters, top_k)
        chunks = self.parts["reranker"].rerank(question, chunks)
        self.parts["rag_result_repo"].bulk_create(
            [
                {"rag_query_id": query_row.id, "article_id": chunk.article_id, "chunk_id": chunk.chunk_id, "score": chunk.score, "rank": i + 1, "result_type": "chunk"}
                for i, chunk in enumerate(chunks)
            ]
        )
        context, sources = self.parts["context_builder"].build(question, chunks)
        answer, sources = self.parts["answer_generator"].generate(question, context, sources)
        return answer, sources, plan

    def answer_from_article(self, article_id: int, question: str):
        article = self.article_repository.get_by_id(article_id)
        chunks = self.chunk_repository.list_by_article(article_id)
        retrieved = [
            RetrievedChunk(chunk.id, article.id, article.source_id, article.company, article.category_id, article.category.name if article.category else None, article.title or "", article.url, chunk.text, 1.0, chunk.chunk_index, article.published_at.isoformat() if article.published_at else None, chunk.heading)
            for chunk in chunks
        ]
        context, sources = self.parts["context_builder"].build(question, retrieved)
        answer, sources = self.parts["answer_generator"].generate(question, context, sources)
        plan = QueryPlan(question, question, "question_answering", "llm_answer", {"article_id": article_id}, [question])
        return answer, sources, plan
