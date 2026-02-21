# Tooling Self-Help Guide

## Tool responsibilities in this project

- **Django**: backend runtime, settings, URL routing, test runner.
- **Django Ninja**: typed REST-style API endpoints and OpenAPI docs.
- **Django Channels**: ASGI WebSocket endpoint at `/ws/ping`.
- **django-cors-headers**: local dev browser-to-backend CORS handling.
- **Svelte**: SPA UI components and reactive state bindings.
- **TypeScript**: typed client modules and safer refactors.
- **Vite**: fast dev server and production build pipeline.
- **Dexie**: ergonomic IndexedDB wrapper for hello payload cache.
- **vite-plugin-pwa**: service worker generation and cache strategy.
- **Vitest**: lightweight frontend smoke tests.

## How each tool is used (concrete)

- Ninja routes in `backend/core/api.py` expose `/api/hello` and `/api/health`.
- Channels consumer in `backend/core/consumers.py` streams heartbeat messages.
- Dexie DB in `frontend/src/lib/db/index.ts` stores `hello` record.
- PWA runtime cache for `/media/*` configured in `frontend/vite.config.ts`.

## Common commands

### Backend

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
pytest
```

### Frontend

```bash
npm install
npm run dev -- --host 0.0.0.0 --port 5173
npm run build
npm run test
```

## Common mistakes and debugging

- **CORS blocked**: mismatch in frontend origin vs `CORS_ALLOWED_ORIGINS`.
- **WS closed quickly**: backend not running or wrong WS URL.
- **No cached hello on reload**: check IndexedDB entry key (`hello`) and browser privacy mode.
- **PWA cache stale**: bump `CACHE_VERSION`, rebuild, then hard refresh.

## When NOT to use each tool here

- Don’t use localStorage for larger server payloads (use Dexie).
- Don’t use WebSocket for one-off config reads (use API).
- Don’t use service worker runtime cache for mutable API JSON in v1.
- Don’t add advanced task queues (Celery) before real async workloads exist.

## Replacement/upgrade options later

- Django Ninja -> DRF (if richer ecosystem needs outweigh speed/typing simplicity).
- Svelte SPA -> SvelteKit (if SSR/routes become important).
- SQLite -> Postgres (production multi-user write load).
- InMemory channel layer -> Redis channel layer.

## Maintenance checklist

1. Update dependencies in small batches.
2. Run backend tests + frontend tests + frontend build.
3. Verify API schema still matches frontend types.
4. Validate PWA cache version bump policy.
5. Smoke test on low-end hardware/browser profile.
