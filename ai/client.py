from dataclasses import dataclass
from typing import Any

from .config import AIConfig


class AIClientError(RuntimeError):
    pass


@dataclass
class AIResult:
    text: str
    model: str
    response_id: str | None = None


class OpenAIResponsesClient:
    def __init__(self, config: AIConfig, client: Any | None = None):
        self.config = config
        if client is not None:
            self._client = client
            return
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AIClientError(
                "openai package is not installed. Run: python3 -m pip install -r requirements-ai.txt"
            ) from exc
        self._client = OpenAI(
            timeout=config.timeout_seconds,
            max_retries=config.max_retries,
        )

    def generate(self, instructions: str, prompt: str) -> AIResult:
        try:
            response = self._client.responses.create(
                model=self.config.model,
                instructions=instructions,
                input=prompt,
            )
        except Exception as exc:
            raise AIClientError(f"OpenAI request failed: {exc}") from exc

        text = getattr(response, "output_text", None)
        if not text or not text.strip():
            raise AIClientError("OpenAI returned an empty response")
        return AIResult(
            text=text.strip(),
            model=getattr(response, "model", self.config.model),
            response_id=getattr(response, "id", None),
        )
