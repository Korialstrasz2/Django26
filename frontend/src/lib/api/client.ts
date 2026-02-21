export type HelloPayload = {
  message: string;
  server_time: string;
  version: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const apiClient = {
  getHello: () => getJson<HelloPayload>('/api/hello'),
  getHealth: () => getJson<{ status: string; uptime_hint: string }>('/api/health')
};
