import json

from app.llm.dummy_llm import DummyLLMClient

DEFAULT_NUM_QUERIES = 3
MAX_NUM_QUERIES = 5


class MultiQueryGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def generate(self, original_query: str, rewritten_query: str, intent: str | None = None) -> list[str]:
        del intent
        if isinstance(self.llm_client, DummyLLMClient):
            return [rewritten_query]
        prompt = f"""Generate {DEFAULT_NUM_QUERIES} search query variants for retrieving engineering blog articles.
Return ONLY a valid JSON array of strings. No explanation, no markdown.

Original query: {original_query}
Rewritten query: {rewritten_query}

Example: ["query 1", "query 2", "query 3"]
"""
        try:
            parsed = json.loads(self.llm_client.generate(prompt))
            if not isinstance(parsed, list):
                return [rewritten_query]
            queries = [item for item in parsed if isinstance(item, str) and item.strip()]
            return queries[:MAX_NUM_QUERIES] or [rewritten_query]
        except Exception:
            return [rewritten_query]
