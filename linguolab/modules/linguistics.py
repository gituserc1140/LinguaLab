"""Linguistics lab module."""

from __future__ import annotations

from collections import Counter

from nltk.corpus import wordnet

from linguolab import nlp_utils

IPA_MAP = {
    "a": "æ", "e": "ɛ", "i": "ɪ", "o": "ɒ", "u": "ʌ",
    "th": "θ", "sh": "ʃ", "ch": "tʃ", "ng": "ŋ", "r": "ɹ",
}

ETYMOLOGY_LOOKUP = {
    "language": "From Old French langage and Latin lingua.",
    "analysis": "From Greek analysis meaning a breaking up.",
    "syntax": "From Greek syntaxis meaning arrangement.",
}


def analyze(text: str) -> dict:
    tokens = nlp_utils.words(text)
    tagged = nlp_utils.pos_tag_tokens(text)

    morphology = Counter(_morph_tag(tok) for tok in tokens)
    syntax = tagged[:40]
    dependencies = _pseudo_dependencies(tokens)

    sample_words = tokens[:8]
    ipa = {w: ipa_transcribe(w) for w in sample_words}
    etymology = {w: etymology_lookup(w) for w in sample_words if etymology_lookup(w)}

    return {
        "morphology_analysis": dict(morphology),
        "syntax_parsing": syntax,
        "dependency_trees": dependencies,
        "ipa_transcription": ipa,
        "etymology_lookup": etymology,
    }


def _morph_tag(token: str) -> str:
    if token.endswith("ing"):
        return "gerund_or_participle"
    if token.endswith("ed"):
        return "past_tense_or_participle"
    if token.endswith("ly"):
        return "adverb"
    if token.endswith("ness") or token.endswith("tion"):
        return "nominalization"
    return "base_or_other"


def _pseudo_dependencies(tokens: list[str]) -> list[dict]:
    if len(tokens) < 2:
        return []
    edges = []
    for i in range(1, min(len(tokens), 30)):
        edges.append({"head": tokens[i - 1], "dependent": tokens[i], "relation": "next"})
    return edges


def ipa_transcribe(word: str) -> str:
    w = word.lower()
    out = w
    for src, dst in sorted(IPA_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        out = out.replace(src, dst)
    return out


def etymology_lookup(word: str) -> str:
    w = word.lower()
    if w in ETYMOLOGY_LOOKUP:
        return ETYMOLOGY_LOOKUP[w]
    try:
        synsets = wordnet.synsets(w)
        if synsets:
            return f"WordNet gloss: {synsets[0].definition()}"
    except LookupError:
        return ""
    return ""
