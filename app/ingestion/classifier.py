from app.domain.results import ClassificationResult
from app.llm.dummy_llm import DummyLLMClient
from app.models.category import Category

CLASSIFIER_MAX_PREVIEW_TOKENS = 500
CLASSIFIER_MIN_CONFIDENCE = 0.4
UNCATEGORIZED_ID = 1


class CategoryClassifier:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def classify(
        self,
        title: str,
        excerpt: str | None,
        clean_text_preview: str,
        categories: list[Category],
    ) -> ClassificationResult:
        uncategorized = self._uncategorized(categories)
        if isinstance(self.llm_client, DummyLLMClient):
            return ClassificationResult(uncategorized.id, uncategorized.name, 0.0, "dummy llm")

        preview = " ".join(clean_text_preview.split()[:CLASSIFIER_MAX_PREVIEW_TOKENS])
        category_list = "\n".join(f"- {category.id}: {category.name}" for category in categories)
        prompt = f"""You are an engineering article classifier. Given an article's title, excerpt, and a short text preview,
classify it into exactly one of the provided categories.

Article title: {title}
Article excerpt: {excerpt}
Text preview (first 500 tokens): {preview}

Available categories:
{category_list}

Return ONLY a valid JSON object with these keys:
- category_id (int): the id of the best matching category
- category_name (str): the name of the category
- confidence (float between 0.0 and 1.0)
- reasoning (str): one sentence explaining the choice

If you are unsure, use the Uncategorized category.
"""
        try:
            result = self.llm_client.generate_json(prompt)
            category_id = int(result["category_id"])
            confidence = float(result.get("confidence", 0.0))
            category = next((item for item in categories if item.id == category_id), uncategorized)
            if confidence < CLASSIFIER_MIN_CONFIDENCE:
                return ClassificationResult(uncategorized.id, uncategorized.name, confidence, result.get("reasoning"))
            return ClassificationResult(category.id, category.name, confidence, result.get("reasoning"))
        except Exception:
            return ClassificationResult(uncategorized.id, uncategorized.name, 0.0, "parse error")

    def _uncategorized(self, categories: list[Category]) -> Category:
        return next((category for category in categories if category.slug == "uncategorized"), categories[0])
