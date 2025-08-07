import { useEffect, useRef, useState } from "react";

export default function ChatPage() {
  // === UI state ===
  const [toId, setToId] = useState("");
  const [msg, setMsg] = useState("");
  const [log, setLog] = useState([]); // {from, message}|{sys}

  // === WebSocket ===
  const wsRef = useRef(null);

  useEffect(() => {
    // Use same‑origin so cookies (user_id) lecą automatycznie
    const ws = new WebSocket(`${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws/dm`);
    wsRef.current = ws;

    ws.addEventListener("message", (e) => {
      try {
        const pkt = JSON.parse(e.data);
        setLog((l) => [...l, pkt]);
      } catch (_) {
        // fallback gdy backend wyśle plain‑text
        setLog((l) => [...l, { sys: e.data }]);
      }
    });

    ws.addEventListener("close", () => {
      // prosty auto‑reconnect po 2 s
      setTimeout(() => window.location.reload(), 2000);
    });

    return () => ws.close();
  }, []);

  // === helpers ===
  const send = () => {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    const to = parseInt(toId, 10);
    if (!to) return;

    ws.send(JSON.stringify({ to, message: msg }));
    setLog((l) => [...l, { from: "you", message: msg }]);
    setMsg("");
  };

  return (
    <div className="h-screen flex flex-col p-4 max-w-xl mx-auto">
      <h1 className="text-xl font-semibold mb-2">DM Chat</h1>

      {/* log */}
      <ul className="flex-1 overflow-y-auto bg-gray-50 rounded p-2 mb-3 space-y-1">
        {log.map((entry, idx) => (
          <li key={idx} className="text-sm whitespace-pre-wrap break-words">
            {entry.sys ? (
              <em className="text-gray-500">{entry.sys}</em>
            ) : (
              <>
                <span className="font-medium mr-1">{entry.from}:</span>
                {entry.message}
              </>
            )}
          </li>
        ))}
      </ul>

      {/* controls */}
      <div className="flex gap-2">
        <input
          type="number"
          min="1"
          value={toId}
          onChange={(e) => setToId(e.target.value)}
          placeholder="do (id)"
          className="w-24 rounded border p-2 text-sm"
        />
        <input
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="wiadomość…"
          className="flex-1 rounded border p-2 text-sm"
        />
        <button
          onClick={send}
          className="rounded bg-blue-600 text-white px-4 py-2 shrink-0 hover:bg-blue-700 transition"
        >
          Wyślij
        </button>
      </div>
    </div>
  );
}
