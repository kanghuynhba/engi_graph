class SearchService:
    def __init__(self, parts: dict, article_repository):
        self.parts = parts
        self.article_repository = article_repository

    def search_chunks(self, query: str, filters: dict | None, top_k: int):
        analysis = self.parts["analyzer"].analyze(query)
        rewritten = self.parts["rewriter"].rewrite(query, analysis)
        queries = self.parts["generator"].generate(query, rewritten, analysis["intent"])
        extracted_filters = self.parts["filters"].extract(query, analysis)
        extracted_filters.update({key: value for key, value in (filters or {}).items() if value is not None})
        chunks = self.parts["retriever"].retrieve(queries, extracted_filters, top_k)
        if not chunks and (extracted_filters.get("category_ids") or extracted_filters.get("category_names")):
            relaxed_filters = extracted_filters.copy()
            relaxed_filters["category_ids"] = None
            relaxed_filters["category_names"] = None
            chunks = self.parts["retriever"].retrieve(queries, relaxed_filters, top_k)
        return self.parts["reranker"].rerank(query, chunks)

    def search_articles(self, query: str, filters: dict | None, top_k: int):
        chunks = self.search_chunks(query, filters, top_k * 5)
        return self.parts["aggregator"].aggregate(chunks)[:top_k]

    def get_best_full_article(self, query: str, filters: dict | None):
        articles = self.search_articles(query, filters, 10)
        return self.article_repository.get_by_id(articles[0].article_id) if articles else None
