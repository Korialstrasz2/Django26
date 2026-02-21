import { latestPing, wsStatus } from '../../stores/appState';

const wsUrl = import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000/ws/ping';

let socket: WebSocket | null = null;

export function connectPingSocket(): void {
  wsStatus.set('connecting');
  socket = new WebSocket(wsUrl);

  socket.onopen = () => wsStatus.set('open');
  socket.onclose = () => wsStatus.set('closed');
  socket.onerror = () => wsStatus.set('closed');

  socket.onmessage = (event) => {
    latestPing.set(event.data);
  };
}

export function closePingSocket(): void {
  socket?.close();
}
