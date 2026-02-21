import { describe, expect, it } from 'vitest';
import { CACHE_VERSION, needsCacheReset } from '../src/lib/cache/cacheVersion';

describe('cache version helper', () => {
  it('flags reset when version changes', () => {
    expect(needsCacheReset('old-version')).toBe(true);
    expect(needsCacheReset(CACHE_VERSION)).toBe(false);
  });
});
