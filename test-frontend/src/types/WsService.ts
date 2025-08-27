export type WsEvents = {
  open?: () => void;
  close?: (ev?: CloseEvent) => void;
  error?: (ev?: Event) => void;
  message?: (data: any) => void;  // już zparsowane JSON albo string
};


export default class WsService {
    private ws: WebSocket | null = null;

    connect(url: string, handlers: WsEvents ) {
        this.close();  // zamknij poprzednie połączenie, jeśli istnieje
        this.ws = new WebSocket(url);
        this.ws.onopen = () => {handlers.open?.()};
        this.ws.onclose = (ev) => {handlers.close?.(ev)};
        this.ws.onerror = (ev) => {handlers.error?.(ev)};
        this.ws.onmessage = (event) => {
            let data: any;
            try{
                data = JSON.parse(event.data);
            } catch (e) {
                handlers.message?.(String(event.data));
            }
        };
    }

    send(obj: unknown) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            return;
        }
        this.ws.send(JSON.stringify(obj));
    }

    close(code?: number, reason?: string) {
        if (this.ws) {
            this.ws.close(code, reason);
            this.ws = null;
        }
    }
}

