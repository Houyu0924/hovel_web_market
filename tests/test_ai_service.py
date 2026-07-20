import unittest

from ai.client import AIClientError, AIResult
from ai.config import AIConfig
from ai.service import AIService


class SuccessClient:
    def generate(self, instructions, prompt):
        return AIResult(text="# AI output", model="test-model", response_id="resp_test")


class FailureClient:
    def generate(self, instructions, prompt):
        raise AIClientError("temporary failure")


class AIServiceTests(unittest.TestCase):
    def test_disabled_uses_deterministic_output(self):
        service = AIService(AIConfig(enabled=False))
        result = service.generate("market", "topic", {}, "fallback")
        self.assertEqual(result.text, "fallback")
        self.assertEqual(result.provider, "deterministic")

    def test_enabled_uses_openai_client(self):
        service = AIService(AIConfig(enabled=True), client=SuccessClient())
        result = service.generate("market", "topic", {}, "fallback")
        self.assertEqual(result.text, "# AI output")
        self.assertEqual(result.provider, "openai")
        self.assertEqual(result.response_id, "resp_test")

    def test_failure_falls_back(self):
        service = AIService(
            AIConfig(enabled=True, fallback_enabled=True),
            client=FailureClient(),
        )
        result = service.generate("market", "topic", {}, "fallback")
        self.assertEqual(result.text, "fallback")
        self.assertEqual(result.provider, "deterministic-fallback")
        self.assertIn("temporary failure", result.error)

    def test_failure_can_be_strict(self):
        service = AIService(
            AIConfig(enabled=True, fallback_enabled=False),
            client=FailureClient(),
        )
        with self.assertRaises(AIClientError):
            service.generate("market", "topic", {}, "fallback")


if __name__ == "__main__":
    unittest.main()
