from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import numpy as np

MODEL_NAME = 'yiyanghkust/finbert-tone'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

label_map = {
    0: 'bearish',
    1: 'neutral',
    2: 'bullish'
}

def classify_sentiment(text: str) -> str:
    """
    Run FinBERT on the given text.

    Returns:
        "bullish" | "bearish" | "neutral"
    """
    result = finbert(text)[0]
    label = result["label"].lower()  # e.g. "positive", "negative", "neutral"

    if "pos" in label:
        return "bullish"
    elif "neg" in label:
        return "bearish"
    else:
        return "neutral"


def map_sentiment_to_signal(sentiment: str) -> str:
    """
    Maps ML output → trading-like signal for your UI.
    Not real financial advice — just rule-based.
    """

    if sentiment == "bullish":
        return "BUY"
    elif sentiment == "bearish":
        return "SELL"
    else:
        return "HOLD"
    
# Quick local test
if __name__ == "__main__":
    examples = [
        "The stock market is doing fantastically well. Huge gains!",
        "This is the worst economy in history. Total disaster.",
        "No big changes in the market today.",
        "good time to buy",
    ]

    for text in examples:
        s = classify_sentiment(text)
        sig = map_sentiment_to_signal(s)
        print(f"{text!r} -> sentiment={s}, signal={sig}")