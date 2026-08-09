"""NLP analysis — TextBlob, langdetect, YAKE with heuristic fallbacks."""

from __future__ import annotations

import re

from app.models.schemas import (
    EmotionResponse,
    EmotionScore,
    EntitiesResponse,
    Entity,
    KeywordsResponse,
    LanguageResponse,
    SentimentResponse,
    SummarizeResponse,
)

POSITIVE = {
    "great", "good", "love", "excellent", "amazing", "perfect", "happy", "beautiful",
    "fast", "incredible", "silent", "crisp", "sharp", "warm", "solid", "wonderful",
    "best", "enjoy", "bueno", "excelente", "feliz", "increíble",
}
NEGATIVE = {
    "bad", "terrible", "hate", "slow", "broken", "awful", "poor", "sad", "angry",
    "worst", "disappointing", "malo", "triste", "lento", "roto",
}
EMOTION_LEXICON: dict[str, list[str]] = {
    "Joy": ["happy", "joy", "love", "great", "amazing", "excited", "delighted", "wonderful", "feliz", "alegría"],
    "Anger": ["angry", "hate", "furious", "annoyed", "terrible", "worst", "enojado", "furioso"],
    "Sadness": ["sad", "unhappy", "cry", "lonely", "disappointing", "loss", "triste"],
    "Fear": ["afraid", "fear", "scared", "worried", "anxious", "nervous", "miedo"],
    "Surprise": ["surprised", "wow", "unexpected", "incredible", "shocked", "amazing", "sorpresa"],
}
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with", "is", "are",
    "was", "it", "this", "that", "at", "as", "by", "be", "de", "la", "el", "los", "las", "y",
    "en", "un", "una", "para", "con", "es",
}
SPANISH_HINTS = {
    "el", "la", "los", "las", "de", "que", "y", "en", "un", "una", "por", "con", "para", "es",
    "está", "más", "pero", "como", "muy",
}
KNOWN_ORGS = ["OpenAI", "Google", "Vercel", "Microsoft", "Amazon", "Meta", "Groq", "PostgreSQL", "Aurora"]
KNOWN_LOCATIONS = [
    "Bogotá", "Bogota", "Medellín", "Medellin", "Colombia", "Argentina", "Brazil", "Chile",
    "Peru", "Mexico", "Lima", "Santiago", "Quito",
]
MONTHS = [
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
]


def _tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-záéíóúñ]+", text.lower()) if t]


def _fallback_sentiment(text: str) -> SentimentResponse:
    tokens = _tokenize(text)
    pos = sum(1 for t in tokens if t in POSITIVE)
    neg = sum(1 for t in tokens if t in NEGATIVE)
    total = pos + neg
    if total == 0:
        return SentimentResponse(label="Neutral", score=0.55)
    if pos >= neg:
        label = "Neutral" if pos == neg else "Positive"
        return SentimentResponse(label=label, score=min(0.95, 0.55 + pos / (total + 2)))
    return SentimentResponse(label="Negative", score=min(0.95, 0.55 + neg / (total + 2)))


def analyze_sentiment(text: str) -> SentimentResponse:
    try:
        from textblob import TextBlob

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return SentimentResponse(label="Positive", score=min(0.95, 0.55 + abs(polarity) * 0.4))
        if polarity < -0.1:
            return SentimentResponse(label="Negative", score=min(0.95, 0.55 + abs(polarity) * 0.4))
        return SentimentResponse(label="Neutral", score=0.55 + abs(polarity) * 0.1)
    except Exception:
        return _fallback_sentiment(text)


def analyze_emotion(text: str) -> EmotionResponse:
    tokens = _tokenize(text)
    raw = []
    for emotion, terms in EMOTION_LEXICON.items():
        count = sum(1 for t in tokens if t in terms)
        raw.append((emotion, count))
    total_hits = sum(c for _, c in raw)
    emotions = [
        EmotionScore(
            emotion=emotion,  # type: ignore[arg-type]
            score=(count / total_hits) if total_hits else (0.35 if emotion == "Joy" else 0.15),
        )
        for emotion, count in raw
    ]
    emotions.sort(key=lambda e: e.score, reverse=True)
    return EmotionResponse(emotions=emotions)


def detect_language(text: str) -> LanguageResponse:
    try:
        from langdetect import detect_langs

        results = detect_langs(text)
        if results:
            top = results[0]
            lang_names = {"en": "English", "es": "Spanish", "pt": "Portuguese", "fr": "French", "de": "German"}
            return LanguageResponse(
                language=lang_names.get(top.lang, top.lang.upper()),
                code=top.lang,
                confidence=min(0.97, float(top.prob)),
            )
    except Exception:
        pass

    tokens = _tokenize(text)
    hits = sum(1 for t in tokens if t in SPANISH_HINTS)
    accent = bool(re.search(r"[áéíóúñ]", text, re.I))
    spanish_score = hits + (2 if accent else 0)
    if spanish_score >= 2:
        return LanguageResponse(language="Spanish", code="es", confidence=min(0.97, 0.6 + spanish_score * 0.08))
    return LanguageResponse(language="English", code="en", confidence=0.9)


def extract_keywords(text: str) -> KeywordsResponse:
    try:
        import yake

        kw_extractor = yake.KeywordExtractor(lan="en", n=2, top=8)
        keywords = [kw for kw, _ in kw_extractor.extract_keywords(text)]
        if keywords:
            return KeywordsResponse(keywords=keywords)
    except Exception:
        pass

    tokens = [t for t in _tokenize(text) if len(t) > 3 and t not in STOPWORDS]
    freq: dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    keywords = [w for w, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:8]]
    return KeywordsResponse(keywords=keywords)


def extract_entities(text: str) -> EntitiesResponse:
    entities: list[Entity] = []

    def push(match: re.Match[str], entity_type: str) -> None:
        entities.append(
            Entity(text=match.group(0), type=entity_type, start=match.start(), end=match.end())  # type: ignore[arg-type]
        )

    cap_seq = re.finditer(r"\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)\b", text)
    for m in cap_seq:
        value = m.group(0)
        if any(loc in value for loc in KNOWN_LOCATIONS):
            push(m, "LOCATION")
        elif any(org in value for org in KNOWN_ORGS):
            push(m, "ORG")
        else:
            push(m, "PERSON")

    for term in KNOWN_ORGS:
        for m in re.finditer(rf"\b{re.escape(term)}\b", text):
            if not any(e.start <= m.start() < e.end for e in entities):
                push(m, "ORG")

    for term in KNOWN_LOCATIONS:
        for m in re.finditer(rf"\b{re.escape(term)}\b", text):
            if not any(e.start <= m.start() < e.end for e in entities):
                push(m, "LOCATION")

    date_re = re.compile(rf"\b(20\d{{2}}|19\d{{2}}|{'|'.join(MONTHS)})\b", re.I)
    for m in date_re.finditer(text):
        if not any(e.start <= m.start() < e.end for e in entities):
            push(m, "DATE")

    entities.sort(key=lambda e: e.start)
    return EntitiesResponse(entities=entities)


def summarize_text(text: str) -> SummarizeResponse:
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]?", text.replace("\n", " ")) if s.strip()]
    if len(sentences) <= 2:
        return SummarizeResponse(summary=text.strip() or "Enter more text to generate a summary.")

    kw = set(extract_keywords(text).keywords)
    scored = []
    for i, s in enumerate(sentences):
        tokens = _tokenize(s)
        score = sum(1 for t in tokens if t in kw) + (1 if i == 0 else 0)
        scored.append((s, score, i))

    top_count = max(1, round(len(sentences) * 0.35))
    top = sorted(sorted(scored, key=lambda x: x[1], reverse=True)[:top_count], key=lambda x: x[2])
    return SummarizeResponse(summary=" ".join(s for s, _, _ in top))
