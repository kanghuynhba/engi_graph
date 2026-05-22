class AnswerGenerator:
    SYSTEM_PROMPT = """You are EngiGraph, an engineering knowledge assistant.
Answer the user's question using ONLY the provided source articles.
Cite sources by referencing the source number like [Source 1], [Source 2].
If the context does not contain enough information to answer, say so clearly.
Do not answer from your own knowledge when context is insufficient.
"""

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def generate(self, question: str, context: str, sources: list) -> tuple[str, list]:
        if not context.strip():
            return "I do not have enough indexed source context to answer that question.", []
        prompt = f"Question: {question}\n\nSources:\n{context}"
        return self.llm_client.generate(prompt, system=self.SYSTEM_PROMPT), sources
