from app.domain.results import RankedArticle, RetrievedChunk


class ArticleAggregator:
    def aggregate(self, chunks: list[RetrievedChunk]) -> list[RankedArticle]:
        grouped: dict[int, list[RetrievedChunk]] = {}
        for chunk in chunks:
            grouped.setdefault(chunk.article_id, []).append(chunk)
        articles = []
        for article_id, article_chunks in grouped.items():
            first = article_chunks[0]
            scores = sorted((chunk.score for chunk in article_chunks), reverse=True)
            articles.append(
                RankedArticle(
                    article_id=article_id,
                    title=first.title,
                    company=first.company,
                    category_name=first.category_name,
                    url=first.url,
                    matched_chunk_count=len(article_chunks),
                    best_score=scores[0],
                    aggregate_score=sum(scores[:3]),
                )
            )
        return sorted(articles, key=lambda item: item.aggregate_score, reverse=True)
