# backend/app/ml_pipeline.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def classify_sentiment(text: str) -> str:
    """
    Use VADER sentiment analysis.

    Returns:
        "bullish" | "bearish" | "neutral"
    """
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]  # in [-1, 1]

    # Standard VADER thresholds
    if compound >= 0.05:
        return "bullish"
    elif compound <= -0.05:
        return "bearish"
    else:
        return "neutral"


def map_sentiment_to_signal(sentiment: str) -> str:
    """
    Map sentiment to a simple demo trading signal.
    """
    if sentiment == "bullish":
        return "BUY"
    elif sentiment == "bearish":
        return "SELL"
    else:
        return "HOLD"


if __name__ == "__main__":
    examples = [
        "The stock market is doing fantastically well. Huge gains!",
        "This is the worst economy in history. Total disaster.",
        "No big changes in the market today.",
        "good time to buy",
        "applied 100% tariffs on China"
    ]

    for text in examples:
        s = classify_sentiment(text)
        sig = map_sentiment_to_signal(s)
        print(f"{text!r} -> sentiment={s}, signal={sig}")
