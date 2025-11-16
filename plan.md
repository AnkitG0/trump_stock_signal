1. High-level design

Goal:
A small web app that:

Fetches Donald Trump’s latest Truth Social posts (via the API you already have).

Runs an ML pipeline to classify each post into bullish / bearish / neutral sentiment toward the market.

Derives a “Buy / Hold / Sell” indicator (for demo purposes, not real financial advice).

Shows all of that on an attractive landing page deployed to Vercel.

You can architect it like this:

Frontend (Next.js on Vercel)

Landing page explaining what the app does.

“Latest Signals” section (cards with post text + sentiment + recommendation).

Simple chart or badges (e.g., % bullish vs bearish, last X posts).

Calls a backend API (hosted separately or as Vercel serverless) to get data.

Backend (Python)

GET /api/latest-signals:

Fetches latest Truth Social posts through your current API client.

Runs them through an ML model (pretrained finance sentiment model).

Maps sentiment → simple trading signal (e.g., bullish → “Buy”).

Returns JSON to the frontend.

Future (not for this weekend):

Replace “API call for posts” with Scrapy-based crawler. Maintain same internal interface so the frontend doesn’t care.

2. Tech stack (opinionated but weekend-friendly)

Backend (Python)

Framework: FastAPI

Easy, async, great docs, built-in OpenAPI docs.

HTTP client (if needed): httpx or requests.

ML:

HuggingFace Transformers + a pretrained finance sentiment model (e.g., FinBERT-like).

You’re not training from scratch this weekend. You’re using a pretrained model and maybe building a thin rule layer on top.

Environment & tooling:

uv or poetry or just pip + venv (whatever is fastest for you).

Pydantic models for request/response schemas (FastAPI uses this anyway).

Frontend (web, on Vercel)

Next.js (the default Vercel stack).

Styling:

Tailwind CSS (fast, utility-first).

Optional: a component library like shadcn/ui or any minimal UI kit.

Data fetching:

fetch from your Python backend.

Or, if you deploy the Python API as Vercel serverless (via something like FastAPI-on-serverless), keep URLs simple.

Data & infra

For a weekend MVP, you can skip a database.

Fetch posts on request, process in-memory, return.

If you want caching, simple in-memory cache (on a small server) or a JSON file written periodically.