# Trump Truth Signals 🟢🔴

Turn Donald Trump's latest Truth Social posts into playful **market sentiment signals** using a Python (FastAPI) backend and a Next.js + Tailwind frontend.

> ⚠️ **Disclaimer:** This project is for learning and entertainment only.  
> It is **not** financial advice and should not be used for real trading decisions.

---

## 🚀 Project Overview

Single repo, two apps:

- **Backend** (`backend/`)
  - Python + FastAPI
  - Fetches latest Truth Social posts (via API wrapper)
  - Runs a sentiment model (e.g., FinBERT-style) over post text
  - Maps sentiment → simple trading signal: `BUY`, `HOLD`, `SELL`
  - Exposes `GET /api/latest-signals` for the frontend

- **Frontend** (`frontend/`)
  - Next.js (App Router) + React + Tailwind CSS
  - Hosted on Vercel
  - Landing page with explanation of the project
  - “Latest Signals” section showing:
    - Post text
    - Sentiment (bullish / bearish / neutral)
    - Suggested signal (BUY / SELL / HOLD)
    - Timestamp

---

## 🧱 Directory Structure

```text
trump-truth-signals/
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ truth_client.py
│  │  ├─ ml_pipeline.py
│  │  └─ config.py
│  ├─ tests/
│  │  ├─ test_api.py
│  │  └─ test_ml_pipeline.py
│  ├─ requirements.txt
│  └─ .env.example
│
├─ frontend/
│  ├─ app/
│  │  └─ page.tsx
│  ├─ components/
│  │  ├─ SignalCard.tsx
│  │  └─ Layout.tsx
│  ├─ public/
│  ├─ styles/
│  │  └─ globals.css
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ next.config.mjs
│  ├─ postcss.config.mjs
│  └─ tailwind.config.mjs
│
├─ .gitignore
└─ README.md
