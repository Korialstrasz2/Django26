import Dexie, { type Table } from 'dexie';
import type { HelloPayload } from '../api/client';

export type CachedHello = HelloPayload & { id: string; cached_at: number };

class AppDB extends Dexie {
  hello!: Table<CachedHello, string>;

  constructor() {
    super('lanGameDB');
    this.version(1).stores({
      hello: 'id,cached_at'
    });
  }
}

const db = new AppDB();

export async function getCachedHello(): Promise<CachedHello | undefined> {
  return db.hello.get('hello');
}

export async function setCachedHello(payload: HelloPayload): Promise<void> {
  await db.hello.put({ ...payload, id: 'hello', cached_at: Date.now() });
}
