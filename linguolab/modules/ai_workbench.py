"""AI language workbench module."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AIResult:
    summarisation: str
    simplification: str
    tone_transformation: str
    rewriting: str
    translation_comparison: dict


def local_transform(text: str) -> AIResult:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    summary = ". ".join(sentences[:2]) + ("." if sentences else "")

    simple = " ".join(text.split())
    simple = simple.replace("utilize", "use").replace("approximately", "about")

    formal_tone = "Please note: " + simple[:300]
    rewrite = simple[::-1][:300]

    translation = {
        "spanish_demo": "[demo] " + summary,
        "french_demo": "[demo] " + summary,
        "notes": "Use OpenAI/Azure OpenAI credentials for model-based translation comparison.",
    }

    return AIResult(
        summarisation=summary,
        simplification=simple[:500],
        tone_transformation=formal_tone,
        rewriting=rewrite,
        translation_comparison=translation,
    )
