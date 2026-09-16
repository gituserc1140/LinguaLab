from linguolab.modules import corpus
import pytest


def test_corpus_analysis_returns_expected_keys():
    docs = ["Language models analyse text.", "Text analysis improves writing."]
    result = corpus.analyze(docs, ngram_size=2)

    assert "n_gram_analysis" in result
    assert "keyword_extraction" in result
    assert isinstance(result["lexical_diversity_metrics"], list)


def test_corpus_analysis_rejects_invalid_ngram_size():
    with pytest.raises(ValueError):
        corpus.analyze(["a b c"], ngram_size=0)
