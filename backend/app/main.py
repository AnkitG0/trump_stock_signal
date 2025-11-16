from fastapi import FastAPI
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
async def latest_signals(limit: int = 4):
    """Get the latest Trump Truth Signals"""
    posts = await fetch_trump_posts()
    signals: list[Signal] = []
    for post in posts:
        sentiment = classify_sentiment(post.get("text"))
        signal = map_sentiment_to_signal(sentiment)
        signals.append(Signal(post=post, sentiment=sentiment, signal=signal))
    return signals

@app.get("/health")
def health():
    return {"status": "ok"}

