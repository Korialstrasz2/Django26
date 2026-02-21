# Best Practices and Project Organization

## Folder structure rules and boundaries

- `backend/config`: platform wiring only (settings, urls, asgi).
- `backend/core`: API schemas/routes + websocket consumers.
- `frontend/src/lib/*`: side effects and infrastructure wrappers.
- `frontend/src/views/*`: route-like UI sections.
- `frontend/src/components/*`: reusable presentational pieces.
- `frontend/src/stores/*`: app-level UI/session state.

## Naming conventions

- API endpoints: lowercase paths (`/api/hello`).
- WebSocket events: lowercase nouns (`ping`, `echo`).
- Store names: descriptive singular nouns (`activeView`, `wsStatus`).

## State boundaries

- UI state (selected view, status chips): Svelte stores + localStorage.
- Server state (hello payload): API client + Dexie cache.
- Cache metadata: localStorage version keys and constants.

## Caching and invalidation rules

- Put durable, reusable server data in IndexedDB.
- Put tiny preference state in localStorage only.
- Version all cache policies (`CACHE_VERSION`) and bump on schema changes.

## API design conventions

- Namespace under `/api/*`.
- Use typed Ninja schemas for request/response consistency.
- Keep payloads compact and explicit.
- Versioning strategy: begin with `version` field in payload, introduce `/api/v2/*` when needed.

## WebSocket event naming

- Events are JSON objects with `event` key.
- Heartbeats: `event=ping`.
- Client round-trip debug: `event=echo`.

## Performance budget mindset for older PCs

- Avoid heavy UI dependencies.
- Lazy-load less-used views.
- Keep re-renders minimal and payloads small.
- Prefer native browser primitives (fetch, Cache API, IndexedDB).

## Add-a-feature checklist

1. Define backend schema.
2. Implement endpoint in `core/api.py`.
3. Add frontend typed API method.
4. Decide cache strategy (none/localStorage/IndexedDB/SW).
5. Implement UI view/component.
6. Add tests (backend + frontend smoke).
7. Update docs.

## Testing guidelines

- Backend: endpoint status + schema key assertions.
- Frontend: lightweight utility/store tests with Vitest.
- Add E2E only when interaction complexity increases.

## Code review checklist

- No full page reload navigation.
- API and WS modules separated from views.
- Caching strategy declared and versioned.
- Dependency count still minimal.
- Commands run and documented.

## Anti-patterns to avoid

- Putting fetch logic directly in many components.
- Duplicating server payload into multiple cache layers without purpose.
- Introducing heavy state/query frameworks in v1.

## Migration notes from legacy Django multi-page apps

- Treat each legacy page as a future SPA view.
- Keep backend template logic only as transition scaffolding.
- Move business logic to API layer before UI rewrites.
- Migrate feature-by-feature, not all at once.
