export type HelloPayload = {
  message: string;
  server_time: string;
  version: string;
};

export type AuthUser = {
  username: string;
  isAuthenticated: boolean;
  isMaster: boolean;
};

export type UserSettings = {
  selectedStyleFolder: string;
  availableStyleFolders: string[];
  backgrounds: Record<string, string>;
};

type AuthPayload = {
  message: string;
  user: AuthUser;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { credentials: 'include' });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

async function postJson<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : undefined
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function toAbsoluteMediaUrl(path: string): string {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return `${API_BASE}${path}`;
}

export const apiClient = {
  getHello: () => getJson<HelloPayload>('/api/hello'),
  getHealth: () => getJson<{ status: string; uptime_hint: string }>('/api/health'),
  getCurrentUser: () => getJson<AuthUser>('/api/auth/me'),
  signup: (username: string, password: string, isMaster: boolean) =>
    postJson<AuthPayload>('/api/auth/signup', { username, password, isMaster }),
  login: (username: string, password: string) =>
    postJson<AuthPayload>('/api/auth/login', { username, password }),
  logout: () => postJson<AuthPayload>('/api/auth/logout'),
  getSettings: () => getJson<UserSettings>('/api/settings'),
  updateSettings: (selectedStyleFolder: string) =>
    postJson<UserSettings>('/api/settings', { selectedStyleFolder }),
  requestCacheClear: () => postJson<{ message: string }>('/api/settings/cache/clear'),
  toAbsoluteMediaUrl
};
