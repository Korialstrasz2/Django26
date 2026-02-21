import { writable } from 'svelte/store';
import type { AuthUser, UserSettings } from '../lib/api/client';

export type ViewName = 'menu' | 'player' | 'coderHelp';

const savedView = (localStorage.getItem('activeView') as ViewName) || 'menu';

export const activeView = writable<ViewName>(savedView);
export const wsStatus = writable<'connecting' | 'open' | 'closed'>('connecting');
export const latestPing = writable<string>('none yet');
export const authUser = writable<AuthUser>({
  username: '',
  isAuthenticated: false,
  isMaster: false
});

export const userSettings = writable<UserSettings>({
  selectedStyleFolder: '',
  availableStyleFolders: [],
  backgrounds: {}
});

activeView.subscribe((value) => {
  localStorage.setItem('activeView', value);
});
