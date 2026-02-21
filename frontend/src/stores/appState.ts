import { writable } from 'svelte/store';

export type ViewName = 'menu' | 'player';

const savedView = (localStorage.getItem('activeView') as ViewName) || 'menu';

export const activeView = writable<ViewName>(savedView);
export const wsStatus = writable<'connecting' | 'open' | 'closed'>('connecting');
export const latestPing = writable<string>('none yet');

activeView.subscribe((value) => {
  localStorage.setItem('activeView', value);
});
