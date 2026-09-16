"""Literary analysis module."""

from __future__ import annotations

import re
from collections import defaultdict

from linguolab import nlp_utils


LITERARY_PATTERNS = {
    "simile": re.compile(r"\b(like|as\s+\w+\s+as)\b", re.IGNORECASE),
    "alliteration": re.compile(r"\b(\w)\w*\s+\1\w*\b", re.IGNORECASE),
}


def analyze(text: str) -> dict:
    sents = nlp_utils.sentences(text)
    devices = {}
    for name, pattern in LITERARY_PATTERNS.items():
        devices[name] = len(pattern.findall(text))

    themes = [w for w, _ in nlp_utils.token_counts(text).most_common(8)]

    characters = _extract_characters(text)
    relationships = _cooccurrence_relationships(sents, characters)

    narrative = {
        "paragraph_count": len([p for p in text.split("\n\n") if p.strip()]),
        "sentence_count": len(sents),
        "opening": sents[0] if sents else "",
        "closing": sents[-1] if sents else "",
    }

    return {
        "literary_devices": devices,
        "themes": themes,
        "character_relationships": relationships,
        "narrative_structure": narrative,
    }


def _extract_characters(text: str) -> list[str]:
    found = re.findall(r"\b[A-Z][a-z]{2,}\b", text)
    ignore = {"The", "This", "That", "And", "But", "When"}
    uniq = []
    for item in found:
        if item in ignore or item in uniq:
            continue
        uniq.append(item)
    return uniq[:10]


def _cooccurrence_relationships(sentences: list[str], characters: list[str]) -> list[dict]:
    graph = defaultdict(int)
    for sentence in sentences:
        present = [c for c in characters if c in sentence]
        for i, src in enumerate(present):
            for dst in present[i + 1 :]:
                key = tuple(sorted((src, dst)))
                graph[key] += 1
    return [
        {"character_a": a, "character_b": b, "mentions_together": count}
        for (a, b), count in sorted(graph.items(), key=lambda x: x[1], reverse=True)
    ]
