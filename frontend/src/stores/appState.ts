import { writable } from 'svelte/store';

export type ViewName = 'menu' | 'player' | 'coderHelp';

export type AuthUser = {
  username: string;
  isAuthenticated: boolean;
  isMaster: boolean;
};

const savedView = (localStorage.getItem('activeView') as ViewName) || 'menu';

export const activeView = writable<ViewName>(savedView);
export const wsStatus = writable<'connecting' | 'open' | 'closed'>('connecting');
export const latestPing = writable<string>('none yet');
export const authUser = writable<AuthUser>({
  username: '',
  isAuthenticated: false,
  isMaster: false
});

activeView.subscribe((value) => {
  localStorage.setItem('activeView', value);
});
