COMPANIES = ["Netflix", "Meta", "Google", "Microsoft", "Discord", "Uber", "Airbnb", "Cloudflare", "Stripe", "LinkedIn", "AWS", "Slack"]
CATEGORY_HINTS = {
    "cdn": "Content Delivery / CDN",
    "distributed systems": "Distributed Systems",
    "infrastructure": "Infrastructure",
    "ml": "Machine Learning / AI",
    "machine learning": "Machine Learning / AI",
    "ai": "Machine Learning / AI",
    "security": "Security",
    "database": "Databases",
    "observability": "Observability",
}


class QueryAnalyzer:
    def analyze(self, query: str) -> dict:
        lowered = query.lower()
        companies = [company for company in COMPANIES if company.lower() in lowered]
        categories = [name for hint, name in CATEGORY_HINTS.items() if hint in lowered]
        if any(phrase in lowered for phrase in ["give me the blog", "full article", "read"]):
            return_type = "full_article"
        elif any(phrase in lowered for phrase in ["list", "show me articles", "what blogs"]):
            return_type = "article_list"
        elif any(phrase in lowered for phrase in ["how does", "explain", "what is"]):
            return_type = "llm_answer"
        else:
            return_type = "chunk_search"
        intent = "question_answering" if return_type == "llm_answer" else "article_search" if companies or categories else "exploration"
        return {"intent": intent, "return_type": return_type, "companies": companies, "topics": [], "categories": sorted(set(categories))}
