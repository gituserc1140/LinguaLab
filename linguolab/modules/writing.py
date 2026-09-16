"""Writing analytics module."""

from __future__ import annotations

from collections import Counter

from linguolab import nlp_utils


PASSIVE_HINTS = {"was", "were", "is", "are", "been", "be", "being"}


def analyze(text: str) -> dict:
    sents = nlp_utils.sentences(text)
    words = nlp_utils.words(text)
    vocab = Counter(words)
    avg_sentence_len = round(len(words) / len(sents), 2) if sents else 0.0

    passive_count = 0
    for sentence in sents:
        tokens = nlp_utils.words(sentence)
        for i in range(len(tokens) - 1):
            if tokens[i] in PASSIVE_HINTS and tokens[i + 1].endswith("ed"):
                passive_count += 1
                break

    grammar_hints = []
    if "  " in text:
        grammar_hints.append("Double spaces detected.")
    if any(s and s[0].islower() for s in sents):
        grammar_hints.append("Some sentences do not start with capitalization.")

    complex_sentences = [s for s in sents if len(nlp_utils.words(s)) >= 20]

    return {
        "readability": nlp_utils.readability_score(text),
        "vocabulary_richness": round(nlp_utils.lexical_diversity(text), 3),
        "grammar_insights": grammar_hints or ["No obvious grammar flags detected."],
        "sentence_complexity": {
            "average_sentence_length": avg_sentence_len,
            "complex_sentence_count": len(complex_sentences),
        },
        "passive_voice_detection": {
            "estimated_passive_sentences": passive_count,
            "passive_ratio": round(passive_count / len(sents), 3) if sents else 0.0,
        },
        "top_vocabulary": vocab.most_common(10),
    }
