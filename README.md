# LAN Multiplayer Game Web App Skeleton (Hello World)

A production-oriented, local-first starter architecture for a LAN multiplayer web app.

## What this project is

This repo is a **rewrite skeleton** with a clear split:
- **Backend**: Django + Django Ninja + Channels (API + WebSocket)
- **Frontend**: Svelte + TypeScript + Vite SPA + PWA
- **Local-first data**: IndexedDB (Dexie) + localStorage for tiny UI prefs

## Architecture overview

- `frontend` serves one SPA shell.
- SPA calls backend `/api/hello` + `/api/health`.
- SPA writes `/api/hello` payload into IndexedDB and displays cached data immediately on reload.
- SPA persists active view (`menu` or `player`) in `localStorage`.
- SPA connects to `/ws/ping` for heartbeat messages.
- Service worker caches built assets + `/media/*` demo assets with Cache API strategy.

## Folder highlights

- `backend/` Django ASGI app
- `frontend/` Vite + Svelte SPA/PWA
- `docs/` architecture and maintenance guides

## Exact run commands

### Linux/macOS

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

New terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev -- --host 0.0.0.0 --port 5173
```

### Windows (PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

New terminal:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev -- --host 0.0.0.0 --port 5173
```


## Grandma mode (double-click startup on Windows)

If you want non-technical users to avoid terminals entirely:

1. Do one-time setup on the **host PC only** (developer/admin): install backend dependencies and run `npm install` in `frontend`.
2. Then users only need to **double-click** `launch_lan_app.bat` from the project root.
3. The launcher will:
   - auto-create `.venv` on first run if needed
   - auto-install backend/frontend dependencies on first run
   - run Django migrations automatically
   - start Django on `0.0.0.0:8000`
   - start Vite on `0.0.0.0:5173`
   - open the browser automatically

4. The launcher window closes itself after startup, so only two service windows stay open (`LAN Backend` + `LAN Frontend`).

Important: other LAN users do **not** need the repo, Python, Node, or a venv. They only open the shared URL in a browser.

To stop the app, close the two command windows titled `LAN Backend` and `LAN Frontend`.

## SPA navigation

Navigation is handled by Svelte store state (`activeView`) and component switching in `App.svelte`. Buttons in `NavTabs.svelte` only update store state, so there are no full page reloads.

## Caching model

- **Service worker + Cache API**: Vite PWA plugin precaches build assets and runtime caches `/media/*`.
- **IndexedDB (Dexie)**: stores latest hello payload.
- **localStorage**: stores tiny UI state (`activeView`) + cache version marker (`cacheVersion`).
- **Invalidation example**: update `CACHE_VERSION` in `src/lib/cache/cacheVersion.ts` to force version rollover behavior.

## WebSocket flow

- Backend Channels consumer at `/ws/ping` pushes heartbeat every 2 seconds.
- Frontend module in `src/lib/ws/pingSocket.ts` updates connection status and latest message store.

## How to extend this skeleton

1. Add feature-specific API schema + route in `backend/core`.
2. Add typed client call under `frontend/src/lib/api`.
3. Add cache policy in `frontend/src/lib/db` and/or `src/lib/cache`.
4. Add view under `src/views` and drive with store state.
5. Keep payloads small for low-end PC + LAN constraints.

## Known limitations of v1

- In-memory Channels layer (single process, no Redis).
- SQLite only (no Postgres migrations in code yet).
- Basic auth/security posture; no production auth implemented.
- Minimal tests and no E2E browser automation in this skeleton.

## Troubleshooting

- If CORS errors occur, check `CORS_ALLOWED_ORIGINS` in backend `.env`.
- If WebSocket fails, verify backend is running as ASGI (`runserver` with Channels installed).
- If stale PWA cache appears, increment cache version constant and rebuild frontend.
- If hello data not persisted, clear browser storage and confirm IndexedDB `lanGameDB` exists.

## Dependency/tool overview

- Backend: Django, Django Ninja, Channels, django-cors-headers
- Frontend: Svelte, Vite, TypeScript, Dexie, vite-plugin-pwa, Vitest

## Legacy migration roadmap (short)

1. Extract legacy Django templates into API responses.
2. Build equivalent SPA views one-by-one in Svelte.
3. Keep old routes alive while new SPA route consumes new APIs.
4. Move polling interactions to WebSocket events where needed.
5. Decommission server-rendered pages after feature parity.
