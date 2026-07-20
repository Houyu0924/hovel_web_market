from dataclasses import dataclass
import os


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AIConfig:
    enabled: bool = False
    model: str = "gpt-5"
    timeout_seconds: float = 90.0
    max_retries: int = 2
    fallback_enabled: bool = True

    @classmethod
    def from_env(cls) -> "AIConfig":
        return cls(
            enabled=_as_bool(os.getenv("HOVEL_AI_ENABLED"), False),
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            timeout_seconds=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "90")),
            max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "2")),
            fallback_enabled=_as_bool(os.getenv("HOVEL_AI_FALLBACK_ENABLED"), True),
        )
