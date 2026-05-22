from app.llm.base import LLMClient


class DummyLLMClient(LLMClient):
    def generate(self, prompt: str, system: str | None = None) -> str:
        del prompt, system
        return "[DummyLLM] This is a placeholder answer."

    def generate_json(self, prompt: str, system: str | None = None) -> dict:
        del prompt, system
        return {"queries": [], "intent": "unknown", "filters": {}, "category_id": 1, "confidence": 0.0}
