type Signal = {
    post: {
        text: string;
        created_at: string;
        id: number;
    };
sentiment: string;
signal: string;
}; 

export default function SignalCard({ signal }: { signal: Signal }) {
    const created = new Date(signal.post.created_at);
  
    const sentimentColor =
      signal.sentiment === "bullish"
        ? "bg-emerald-500"
        : signal.sentiment === "bearish"
        ? "bg-red-500"
        : "bg-slate-500";
  
    const signalColor =
      signal.signal === "BUY"
        ? "text-emerald-400"
        : signal.signal === "SELL"
        ? "text-red-400"
        : "text-slate-300";
  
    return (
      <div className="border border-slate-800 rounded-xl p-4 bg-slate-900/70 shadow-sm">
        <div className="flex items-center justify-between mb-2 text-xs text-slate-400">
          <span>{created.toLocaleString()}</span>
          <span
            className={`px-2 py-0.5 rounded-full text-[10px] uppercase tracking-wide text-white ${sentimentColor}`}
          >
            {signal.sentiment}
          </span>
        </div>
        <p className="text-sm text-slate-100 whitespace-pre-wrap">
          {signal.post.text}
        </p>
        <div className="mt-3 text-xs">
          <span className="text-slate-400 mr-1">Model signal:</span>
          <span className={`font-semibold ${signalColor}`}>{signal.signal}</span>
        </div>
      </div>
    );
  }