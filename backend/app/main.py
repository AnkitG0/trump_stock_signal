from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import Signal
from .truth_client import fetch_trump_posts
from .ml_pipeline import classify_sentiment, map_sentiment_to_signal
from .config import get_settings

settings = get_settings()

app = FastAPI(title="Trump Truth Signals API")

origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/latest-signals", response_model=list[Signal])
def latest_signals():
    """
    1. Fetch latest Truth Social posts via truth_client
    2. Run FinBERT sentiment on each
    3. Map sentiment -> BUY / HOLD / SELL
    """
    try:
        posts = fetch_trump_posts()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching posts: {e}")

    signals: List[Signal] = []

    for p in posts:
        sentiment = classify_sentiment(p.text)
        signal = map_sentiment_to_signal(sentiment)
        signals.append(Signal(post=p, sentiment=sentiment, signal=signal))

    return signals

@app.get("/health")
def health():
    return {"status": "ok"}

