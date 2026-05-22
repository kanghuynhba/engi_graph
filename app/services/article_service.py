class ArticleService:
    def __init__(self, article_repository, chunk_repository, vector_store):
        self.article_repository = article_repository
        self.chunk_repository = chunk_repository
        self.vector_store = vector_store

    def list_articles(self, limit: int = 100, offset: int = 0):
        return self.article_repository.list_all(limit, offset)

    def get_article(self, article_id: int):
        return self.article_repository.get_by_id(article_id)

    def get_article_chunks(self, article_id: int):
        return self.chunk_repository.list_by_article(article_id)

    def delete_article(self, article_id: int) -> None:
        self.vector_store.delete_by_article(article_id)
        self.article_repository.delete(article_id)
