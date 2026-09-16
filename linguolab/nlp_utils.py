"""Shared NLP helpers using spaCy and NLTK."""

from __future__ import annotations

import re
from collections import Counter

import nltk
import spacy


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z']+")


def ensure_nltk_resource(path: str, package: str) -> None:
    try:
        nltk.data.find(path)
    except LookupError:
        try:
            nltk.download(package, quiet=True)
        except Exception:
            pass


def sentences(text: str) -> list[str]:
    chunks = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    return chunks or ([text.strip()] if text.strip() else [])


def words(text: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(text)]


def token_counts(text: str) -> Counter[str]:
    return Counter(words(text))


def lexical_diversity(text: str) -> float:
    toks = words(text)
    if not toks:
        return 0.0
    return len(set(toks)) / len(toks)


def readability_score(text: str) -> float:
    sents = sentences(text)
    toks = words(text)
    if not sents or not toks:
        return 0.0
    syllables = sum(_count_syllables(w) for w in toks)
    asl = len(toks) / len(sents)
    asw = syllables / len(toks)
    return round(206.835 - 1.015 * asl - 84.6 * asw, 2)


def _count_syllables(word: str) -> int:
    groups = re.findall(r"[aeiouy]+", word.lower())
    return max(1, len(groups))


def spacy_doc(text: str):
    nlp = spacy.blank("en")
    return nlp(text)


def pos_tag_tokens(text: str) -> list[tuple[str, str]]:
    ensure_nltk_resource("tokenizers/punkt", "punkt")
    ensure_nltk_resource("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger")
    toks = nltk.word_tokenize(text) if text.strip() else []
    if not toks:
        return []
    try:
        return nltk.pos_tag(toks)
    except LookupError:
        return [(t, "NN") for t in toks]
