"""Word explorer module."""

from __future__ import annotations

from nltk.corpus import wordnet

from linguolab.modules.linguistics import etymology_lookup


def explore(word: str) -> dict:
    target = word.strip().lower()
    if not target:
        return {
            "definitions": [],
            "synonyms": [],
            "semantic_relationships": [],
            "usage_examples": [],
            "historical_language_information": "",
        }

    try:
        synsets = wordnet.synsets(target)
    except LookupError:
        synsets = []

    defs = [s.definition() for s in synsets[:5]]
    examples = []
    synonyms = set()
    hypernyms = set()

    for syn in synsets[:5]:
        examples.extend(syn.examples())
        synonyms.update(lemma.name().replace("_", " ") for lemma in syn.lemmas())
        hypernyms.update(h.name().split(".")[0].replace("_", " ") for h in syn.hypernyms())

    return {
        "definitions": defs,
        "synonyms": sorted(synonyms)[:20],
        "semantic_relationships": sorted(hypernyms)[:10],
        "usage_examples": examples[:5],
        "historical_language_information": etymology_lookup(target),
    }
