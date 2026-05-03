from __future__ import annotations

import os


class GeminiLLMClient:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate(self, prompt: str) -> str:
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("google-genai nao esta instalado. Rode `python run.py setup`.") from exc

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY nao configurada.")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=self.model, contents=prompt)
        return response.text or ""

