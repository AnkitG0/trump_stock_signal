export type Signal = {
    post: {
      id: string;          // ✅ string — matches backend (Pydantic uses str for id)
      created_at: string;
      text: string;
    };
    sentiment: string;     // "bullish" | "bearish" | "neutral"
    signal: string;        // "BUY" | "HOLD" | "SELL"
  };
  