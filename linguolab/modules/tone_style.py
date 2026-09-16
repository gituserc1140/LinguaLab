"""Tone and style analysis module."""

from __future__ import annotations

from nltk.sentiment import SentimentIntensityAnalyzer

from linguolab import nlp_utils

FORMAL_WORDS = {"therefore", "furthermore", "moreover", "consequently", "regarding", "please"}
INFORMAL_WORDS = {"gonna", "wanna", "kinda", "lol", "yeah", "cool"}
EMOTION_WORDS = {
    "joy": {"happy", "joy", "delight", "glad", "excited"},
    "anger": {"angry", "mad", "furious", "annoyed"},
    "sadness": {"sad", "upset", "down", "depressed"},
    "fear": {"fear", "afraid", "worry", "anxious"},
}


def _sia() -> SentimentIntensityAnalyzer | None:
    nlp_utils.ensure_nltk_resource("sentiment/vader_lexicon", "vader_lexicon")
    try:
        return SentimentIntensityAnalyzer()
    except Exception:
        return None


def analyze(text: str) -> dict:
    tokens = nlp_utils.words(text)
    if not tokens:
        return {
            "formality_score": 0.0,
            "sentiment": {"compound": 0.0},
            "emotional_tone": {},
            "audience_suitability": "No text provided.",
        }

    formal = sum(1 for t in tokens if t in FORMAL_WORDS)
    informal = sum(1 for t in tokens if t in INFORMAL_WORDS)
    formality = max(0.0, min(1.0, (formal + 1) / (formal + informal + 2)))

    sia = _sia()
    sentiment = sia.polarity_scores(text) if sia else {"compound": 0.0}

    emotion = {
        k: sum(1 for t in tokens if t in terms)
        for k, terms in EMOTION_WORDS.items()
    }

    suitability = "General audience"
    if formality > 0.7:
        suitability = "Professional / academic audience"
    elif formality < 0.4:
        suitability = "Casual audience"

    return {
        "formality_score": round(formality, 3),
        "sentiment": sentiment,
        "emotional_tone": emotion,
        "audience_suitability": suitability,
    }
