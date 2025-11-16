// frontend/app/page.tsx
import SignalCard from "@/components/SignalCard";

type Signal = {
  post: {
    id: string;
    created_at: string;
    text: string;
  };
  sentiment: string;
  signal: string;
};

async function getSignals(): Promise<Signal[]> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const res = await fetch(`${baseUrl}/api/latest-signals`, {
    cache: "no-store",
  });

  if (!res.ok) {
    console.error("Failed to fetch signals", await res.text());
    throw new Error("Failed to fetch signals");
  }

  return res.json();
}

export default async function Home() {
  const signals = await getSignals();

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <header className="space-y-2">
          <h1 className="text-3xl md:text-4xl font-bold">
            Trump Truth Signals
          </h1>
          <p className="text-slate-300 max-w-2xl">
            A fun machine learning demo that turns Donald Trump&apos;s Truth Social
            posts into playful BUY / SELL / HOLD sentiment signals.
          </p>
          <p className="text-xs text-slate-500">
            This is not financial advice.
          </p>
        </header>

        <section className="space-y-4">
          <h2 className="text-xl font-semibold">Latest Signals</h2>
          <div className="space-y-4">
            {signals.map((s) => (
              <SignalCard key={s.post.id} signal={s} />
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
