import re


class MetadataFilterExtractor:
    def __init__(self, category_repository):
        self.category_repository = category_repository

    def extract(self, query: str, analysis: dict) -> dict:
        category_names = analysis.get("categories") or None
        category_ids = None
        if category_names:
            category_ids = []
            for name in category_names:
                category = self.category_repository.get_by_name(name)
                if category:
                    category_ids.append(category.id)
        published_after = None
        published_before = None
        after_match = re.search(r"(?:after|since)\s+(\d{4})", query, re.IGNORECASE)
        before_match = re.search(r"before\s+(\d{4})", query, re.IGNORECASE)
        if after_match:
            published_after = f"{after_match.group(1)}-01-01"
        if before_match:
            published_before = f"{before_match.group(1)}-01-01"
        return {
            "companies": analysis.get("companies") or None,
            "category_names": category_names,
            "category_ids": category_ids or None,
            "published_after": published_after,
            "published_before": published_before,
        }
