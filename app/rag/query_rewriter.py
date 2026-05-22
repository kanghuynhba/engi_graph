from app.llm.dummy_llm import DummyLLMClient


class QueryRewriter:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def rewrite(self, query: str, analysis: dict) -> str:
        if isinstance(self.llm_client, DummyLLMClient):
            return query
        prompt = f"""Rewrite the following user query into a precise technical search query for engineering blog articles.
Preserve company names. Use engineering terminology. Be specific.

User query: {query}
Detected companies: {analysis.get("companies", [])}

Return only the rewritten query string, nothing else.
"""
        return self.llm_client.generate(prompt).strip() or query
