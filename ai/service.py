from dataclasses import dataclass
import json

from .client import AIClientError, OpenAIResponsesClient
from .config import AIConfig


SYSTEM_INSTRUCTIONS = """You are an AI agent in the HOVEL marketing workflow.
Write in Japanese. Prioritize reader benefit and factual accuracy.
Do not fabricate product use, prices, studies, citations, or medical claims.
Clearly mark facts that require external verification.
Return Markdown only. Do not publish content or claim human approval.
"""


@dataclass
class Generation:
    text: str
    provider: str
    model: str | None = None
    response_id: str | None = None
    error: str | None = None


class AIService:
    def __init__(self, config: AIConfig | None = None, client=None):
        self.config = config or AIConfig.from_env()
        self.client = client

    def _prompt(self, stage: str, topic: str, inputs: dict, fallback: str) -> str:
        prior = {key: value for key, value in inputs.items() if not key.startswith("_")}
        return f"""# Task
Stage: {stage}
Topic: {topic}

Improve or replace the deterministic draft below for this stage.
Preserve the stage's purpose and handoff value.
Do not include unsupported citations or unverifiable specifics.

## Previous stage outputs
{json.dumps(prior, ensure_ascii=False, indent=2)}

## Deterministic fallback draft
{fallback}
"""

    def generate(self, stage: str, topic: str, inputs: dict, fallback: str) -> Generation:
        if not self.config.enabled:
            return Generation(text=fallback, provider="deterministic")

        try:
            client = self.client or OpenAIResponsesClient(self.config)
            result = client.generate(
                instructions=SYSTEM_INSTRUCTIONS,
                prompt=self._prompt(stage, topic, inputs, fallback),
            )
            return Generation(
                text=result.text,
                provider="openai",
                model=result.model,
                response_id=result.response_id,
            )
        except AIClientError as exc:
            if not self.config.fallback_enabled:
                raise
            return Generation(
                text=fallback,
                provider="deterministic-fallback",
                error=str(exc),
            )
