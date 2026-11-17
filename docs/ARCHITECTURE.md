# CineRwa Architecture

## Overview
CineRwa is a movie discovery and authorized streaming platform. Phase 01 delivers the frontend experience and backend foundation.

## Frontend
- Vue 3 (Composition API, `<script setup>`)
- Vite
- Tailwind CSS (installed; custom design tokens in `src/assets/styles/`)
- Vue Router
- Pinia

### Key folders
- `src/components/` — reusable UI (navigation, movie, player, common).
- `src/pages/` — route-level views.
- `src/services/` — data services and content provider adapters.
- `src/stores/` — Pinia stores (watchlist, ui).
- `src/data/` — demonstration data.
- `src/router/` — route definitions.

### Data flow
Components call services (`movieService`, `searchService`, `seriesService`). Services return demo data now; can be swapped for HTTP calls to the backend/TMDB without changing components.

### Content providers
`services/contentProvider.js` defines `ContentProviderAdapter` and a `providerRegistry`. Each provider (Demo, future licensed) implements metadata/watch-link/availability. No provider-specific logic in components.

## Backend
- FastAPI, REST, API versioning under `/api/v1`.
- Settings via pydantic-settings + `.env`.
- SQLAlchemy + MySQL-ready (SQLite default for dev).
- JWT auth prepared (not yet implemented).
- Health check: `GET /api/v1/health`.

### Folders
```
backend/app/
  api/        routes
  core/       config, database
  models/     SQLAlchemy models (future)
  schemas/    Pydantic schemas (future)
  services/   business logic (future)
  integrations/  TMDB, providers (future)
  main.py
```

## Movie data model
Fields: id, title, overview, poster, backdrop, releaseDate, genres, language, rating, runtime, contentType, source, playbackType, availabilityStatus, translator (for Agasobanuye/translated films).
