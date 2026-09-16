"""Service layer that orchestrates module execution and persistence."""

from __future__ import annotations

import json

from linguolab.config import settings
from linguolab.db import recent_analyses, save_analysis
from linguolab.modules import ai_workbench, corpus, literary, linguistics, tone_style, word_explorer, writing
from linguolab import openai_client


class LinguaLabService:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.sqlite_path

    def writing_analytics(self, text: str) -> dict:
        result = writing.analyze(text)
        self._save("writing_analytics", text, result)
        return result

    def tone_style(self, text: str) -> dict:
        result = tone_style.analyze(text)
        self._save("tone_style", text, result)
        return result

    def literary_analysis(self, text: str) -> dict:
        result = literary.analyze(text)
        self._save("literary_analysis", text, result)
        return result

    def linguistics_lab(self, text: str) -> dict:
        result = linguistics.analyze(text)
        self._save("linguistics_lab", text, result)
        return result

    def corpus_analysis(self, docs: list[str], ngram_size: int = 2) -> dict:
        raw = "\n\n".join(docs)
        result = corpus.analyze(docs, ngram_size=ngram_size)
        self._save("corpus_analysis", raw, result)
        return result

    def corpus_lexical_dataframe(self, docs: list[str]):
        return corpus.lexical_diversity_frame(docs)

    def word_explorer(self, word: str) -> dict:
        result = word_explorer.explore(word)
        self._save("word_explorer", word, result)
        return result

    def ai_language_workbench(self, text: str) -> dict:
        local = ai_workbench.local_transform(text)
        result = {
            "summarisation": local.summarisation,
            "simplification": local.simplification,
            "tone_transformation": local.tone_transformation,
            "rewriting": local.rewriting,
            "translation_comparison": local.translation_comparison,
            "provider": "local-demo",
        }

        if openai_client.available() and text.strip():
            try:
                provider = openai_client.resolve_runtime_provider("auto")
                prompt = (
                    "Return JSON with keys summarisation, simplification, tone_transformation, "
                    "rewriting, translation_comparison for this text:\n" + text
                )
                completion = openai_client.completion(prompt, provider=provider)
                model_result = json.loads(completion)
                if isinstance(model_result, dict):
                    allowed_keys = {
                        "summarisation",
                        "simplification",
                        "tone_transformation",
                        "rewriting",
                        "translation_comparison",
                    }
                    for key in allowed_keys:
                        if key in model_result:
                            result[key] = model_result[key]
                    result["provider"] = provider
            except (RuntimeError, ValueError, TypeError, KeyError, ImportError, ModuleNotFoundError) as exc:
                result["provider_error"] = str(exc)

        self._save("ai_language_workbench", text, result)
        return result

    def history(self, limit: int = 10) -> list[dict]:
        return recent_analyses(self.db_path, limit=limit)

    def _save(self, module: str, input_text: str, result: dict) -> None:
        save_analysis(self.db_path, module, input_text, result)
