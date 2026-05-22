from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_json(self, prompt: str, system: str | None = None) -> dict:
        raise NotImplementedError
