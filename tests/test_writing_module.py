from linguolab.modules import writing


def test_writing_analysis_basics():
    text = "This is a simple sentence. The report was completed yesterday."
    result = writing.analyze(text)

    assert "readability" in result
    assert result["sentence_complexity"]["average_sentence_length"] > 0
    assert result["passive_voice_detection"]["estimated_passive_sentences"] >= 1
