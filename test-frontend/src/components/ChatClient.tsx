"use client";
import { useEffect, useRef, useState } from "react";
import { Send, Wifi, WifiOff } from "lucide-react";

type Msg = { from: string | number; message: string; ts?: number };

export default function ChatClient({
  targetId,
  backend,
  initialMessages,
}: {
  targetId: string;
  backend: string;
  initialMessages: Msg[];
}) {
  const [log, setLog] = useState<Msg[]>(initialMessages);
  const [message, setMessage] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const boxRef = useRef<HTMLDivElement | null>(null);

  // autoscroll
  useEffect(() => {
    boxRef.current?.scrollTo({
      top: boxRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [log]);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/api/user/ws/dm?to=${targetId}`);
    wsRef.current = ws;

    const onOpen = () => {
      setIsConnected(true);
      setLog((p) => [...p, { from: "system", message: "Połączono z czatem", ts: Date.now() }]);
    };
    const onMessage = (e: MessageEvent) => {
      try {
        const data = JSON.parse(e.data);
        setLog((p) => [
          ...p,
          { from: data.from, message: data.message, ts: data.ts || Date.now() },
        ]);
        console.log("Received message:", data);
      } catch {
        setLog((p) => [...p, { from: "?", message: String(e.data), ts: Date.now() }]);
      }
    };
    const onClose = () => {
      setIsConnected(false);
      setLog((p) => [...p, { from: "system", message: "Rozłączono z czatem", ts: Date.now() }]);
    };

    ws.addEventListener("open", onOpen);
    ws.addEventListener("message", onMessage);
    ws.addEventListener("close", onClose);

    return () => {
      ws.removeEventListener("open", onOpen);
      ws.removeEventListener("message", onMessage);
      ws.removeEventListener("close", onClose);
      try { ws.close(1000, "component unmount"); } catch {}
      wsRef.current = null;
    };
  }, [targetId, backend]);

  const send = () => {
    const ws = wsRef.current;
    const text = message.trim();
    if (!ws || ws.readyState !== WebSocket.OPEN || !text) return;
    
    // Add the message immediately to the log as "sent by me"
    setLog((p) => [...p, { from: "me", message: text, ts: Date.now() }]);
    
    ws.send(JSON.stringify({ message: text }));
    setMessage("");
  };

  const onKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      send();
    }
  };

  const formatMessageFrom = (from: string | number) => {
    if (from === "system") return "System";
    return String(from);
  };

  const isSystemMessage = (from: string | number) => from === "system";
  
  const isOwnMessage = (from: string | number) => {
    // Assuming messages from "me" or current user are own messages
    // You might need to adjust this logic based on your backend response
    return from === "me" || from === "self" || String(from) === "you";
  };

  return (
    <div className="bg-white/80 backdrop-blur-lg rounded-2xl border border-blue-100 shadow-xl overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4">
        <div className="flex items-center justify-between">
          <h3 className="text-white font-semibold text-lg">
            Czat z {targetId}
          </h3>
          <div className="flex items-center space-x-2">
            {isConnected ? (
              <div className="flex items-center space-x-1 text-green-100">
                <Wifi size={16} />
                <span className="text-sm">Połączono</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1 text-red-200">
                <WifiOff size={16} />
                <span className="text-sm">Rozłączono</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div
        ref={boxRef}
        className="h-96 overflow-y-auto p-4 space-y-3 bg-gradient-to-b from-blue-50/30 to-purple-50/30"
      >
        {log.length === 0 ? (
          <div className="text-center text-slate-500 py-8">
            <p>Brak wiadomości. Rozpocznij rozmowę!</p>
          </div>
        ) : (
          log.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                isSystemMessage(msg.from) 
                  ? 'justify-center' 
                  : isOwnMessage(msg.from) 
                    ? 'justify-end' 
                    : 'justify-start'
              }`}
            >
              {isSystemMessage(msg.from) ? (
                <div className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs">
                  {msg.message}
                  {msg.ts && (
                    <span className="ml-2 text-slate-400">
                      {new Date(msg.ts).toLocaleTimeString()}
                    </span>
                  )}
                </div>
              ) : (
                <div className="max-w-[80%]">
                  <div className={`backdrop-blur-sm rounded-2xl px-4 py-3 shadow-sm border ${
                    isOwnMessage(msg.from)
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white border-blue-300'
                      : 'bg-white/90 text-slate-700 border-blue-100'
                  }`}>
                    <div className="flex items-center space-x-2 mb-1">
                      <span className={`font-semibold text-sm ${
                        isOwnMessage(msg.from) ? 'text-blue-100' : 'text-slate-800'
                      }`}>
                        {isOwnMessage(msg.from) ? 'Ty' : formatMessageFrom(msg.from)}
                      </span>
                      {msg.ts && (
                        <span className={`text-xs ${
                          isOwnMessage(msg.from) ? 'text-blue-200' : 'text-slate-500'
                        }`}>
                          {new Date(msg.ts).toLocaleTimeString()}
                        </span>
                      )}
                    </div>
                    <p className={`text-sm leading-relaxed ${
                      isOwnMessage(msg.from) ? 'text-white' : 'text-slate-700'
                    }`}>
                      {msg.message}
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white/60 backdrop-blur-sm border-t border-blue-100">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder="Napisz wiadomość..."
              className="w-full rounded-xl border border-blue-200 bg-white/80 backdrop-blur-sm px-4 py-3 text-slate-700 placeholder-slate-400 outline-none transition-all duration-200 focus:border-purple-400 focus:ring-2 focus:ring-purple-100 focus:bg-white"
              disabled={!isConnected}
            />
          </div>
          <button
            onClick={send}
            disabled={!isConnected || !message.trim()}
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-slate-300 disabled:to-slate-400 text-white rounded-xl px-6 py-3 transition-all duration-200 hover:shadow-lg hover:scale-105 active:scale-95 disabled:cursor-not-allowed disabled:hover:scale-100 disabled:hover:shadow-none flex items-center space-x-2"
          >
            <Send size={16} />
            <span className="font-medium">Wyślij</span>
          </button>
        </div>

        {!isConnected && (
          <p className="text-xs text-red-500 mt-2 text-center">
            Brak połączenia. Sprawdź połączenie internetowe.
          </p>
        )}
      </div>
    </div>
  );
}
