"""Corpus analysis module."""

from __future__ import annotations

from collections import Counter
from itertools import islice

import pandas as pd

from linguolab import nlp_utils


def analyze(documents: list[str], ngram_size: int = 2) -> dict:
    if ngram_size < 1:
        raise ValueError("ngram_size must be >= 1")

    cleaned_docs = [d for d in documents if d.strip()]
    if not cleaned_docs:
        return {
            "multi_document_comparison": [],
            "n_gram_analysis": [],
            "topic_modelling": [],
            "keyword_extraction": [],
            "lexical_diversity_metrics": [],
        }

    comparison = _comparison(cleaned_docs)
    ngrams = _ngrams(cleaned_docs, ngram_size)
    keywords = Counter()
    for doc in cleaned_docs:
        keywords.update(nlp_utils.words(doc))

    lexical = [
        {"document": i + 1, "lexical_diversity": round(nlp_utils.lexical_diversity(doc), 3)}
        for i, doc in enumerate(cleaned_docs)
    ]

    topics = _simple_topics(keywords)

    return {
        "multi_document_comparison": comparison,
        "n_gram_analysis": ngrams,
        "topic_modelling": topics,
        "keyword_extraction": keywords.most_common(20),
        "lexical_diversity_metrics": lexical,
    }


def lexical_diversity_frame(documents: list[str]) -> pd.DataFrame:
    rows = [
        {
            "document": f"Doc {idx + 1}",
            "tokens": len(nlp_utils.words(doc)),
            "lexical_diversity": round(nlp_utils.lexical_diversity(doc), 3),
        }
        for idx, doc in enumerate(documents)
        if doc.strip()
    ]
    return pd.DataFrame(rows)


def _comparison(documents: list[str]) -> list[dict]:
    sets = [set(nlp_utils.words(d)) for d in documents]
    results = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            union = sets[i] | sets[j]
            inter = sets[i] & sets[j]
            score = round(len(inter) / len(union), 3) if union else 0.0
            results.append({"pair": f"Doc {i+1} vs Doc {j+1}", "jaccard_similarity": score})
    return results


def _ngrams(documents: list[str], n: int) -> list[tuple[str, int]]:
    if n < 1:
        return []

    counter = Counter()
    for doc in documents:
        tokens = nlp_utils.words(doc)
        grams = zip(*(islice(tokens, i, None) for i in range(n))) if len(tokens) >= n else []
        counter.update(" ".join(g) for g in grams)
    return counter.most_common(20)


def _simple_topics(keyword_counts: Counter[str]) -> list[dict]:
    top_terms = [k for k, _ in keyword_counts.most_common(15)]
    buckets = [top_terms[i : i + 5] for i in range(0, len(top_terms), 5)]
    return [{"topic": idx + 1, "terms": terms} for idx, terms in enumerate(buckets) if terms]
