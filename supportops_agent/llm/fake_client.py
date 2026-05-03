from __future__ import annotations


class FakeLLMClient:
    def generate(self, prompt: str) -> str:
        if "TCK-4821" in prompt:
            return "permission_cache_after_role_change"
        if "ignore" in prompt.lower():
            return "possible_prompt_injection"
        return "needs_more_context"

