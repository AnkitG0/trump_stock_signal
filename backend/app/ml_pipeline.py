# backend/app/ml_pipeline.py

import os
import requests
from typing import Tuple

HUGGINGFACE_API_URL = (
    "https://api-inference.huggingface.co/models/yiyanghkust/finbert-tone"
)
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")


def _hf_request(text: str) -> dict:
    if not HUGGINGFACE_API_TOKEN:
        raise RuntimeError("HUGGINGFACE_API_TOKEN is not set")

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Accept": "application/json",
    }
    payload = {"inputs": text}

    resp = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def classify_sentiment(text: str) -> str:
    """
    Use remote FinBERT to classify text.

    Returns:
        "bullish" | "bearish" | "neutral"
    """
    data = _hf_request(text)

    # Hugging Face inference API returns a list of lists of dicts:
    # [[{"label": "positive", "score": 0.9}, {"label": "neutral", ...}, ...]]
    if not data or not isinstance(data, list):
        raise RuntimeError(f"Unexpected HF response: {data}")

    top = data[0][0]  # highest score
    label = top["label"].lower()  # "positive" | "negative" | "neutral"

    if "pos" in label:
        return "bullish"
    elif "neg" in label:
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
    ]

    for text in examples:
        s = classify_sentiment(text)
        sig = map_sentiment_to_signal(s)
        print(f"{text!r} -> sentiment={s}, signal={sig}")
