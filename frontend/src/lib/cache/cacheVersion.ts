export const CACHE_VERSION = 'v1';

export function needsCacheReset(previousVersion: string | null): boolean {
  return previousVersion !== CACHE_VERSION;
}
