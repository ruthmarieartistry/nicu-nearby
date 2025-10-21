## NICU Finder — Copilot instructions

Short summary

- Next.js (pages router) frontend in `pages/index.js` and a single serverless API in `pages/api/search-nicus.js`.
- Primary integration: Google Maps (Geocode, Places Nearby Search, Distance Matrix). The app looks up hospitals with NICU keywords and returns a sorted list of results to the client.

Quick commands

- Local dev: `npm run dev` (Next.js dev server)
- Build: `npm run build` and `npm run start` for production serve
- Lint: `npm run lint`
- Test API (direct): `npm run test-api` (invokes `scripts/test-api.js` which loads `.env.local` and calls the API handler)

Required environment

- The API expects `GOOGLE_MAPS_API_KEY` in the environment. If missing the API returns 500 with `{ error: 'API key not configured' }`.
- For local development use the Next.js convention: put the key in `.env.local` or export it in your shell before `npm run dev`.

Architecture & data flow (what to read)

- UI: `pages/index.js` — single-page UI implemented using React.createElement (no JSX). Uses Tailwind utility classes from `styles/globals.css`.
- API: `pages/api/search-nicus.js` — client calls `/api/search-nicus?location=...&radius=...`. The handler:
  1. Geocodes `location` via Google Geocode API
  2. Calls Google Places Nearby Search for `type=hospital` and `keyword=NICU+neonatal+intensive+care`
  3. For each place, calls Distance Matrix with `destinations=place_id:...` to get driving distance
  4. Filters by radius (miles -> meters conversion), maps to a result object and returns JSON.

API contract (observed from `pages/api/search-nicus.js`)

- Request: GET `/api/search-nicus?location=<string>&radius=<miles>` (radius defaults to 60)
- Success response: 200 JSON { results: [ { name, address, distance, distanceValue, rating, reviews, placeId, phone } ] }
  - `distance` is a string (code strips ' mi' if present)
  - `distanceValue` is in meters (from Google Distance Matrix)
- Error responses seen in code:
  - 400 if `location` missing
  - 500 if API key missing or an unhandled error occurs

Project-specific patterns and gotchas

- `pages/index.js` uses React.createElement style instead of JSX — keep the same style when making small edits to avoid adding a transpile step.
- API route exports with CommonJS: `module.exports = async function handler(...) {}`. When editing `pages/api/*` preserve CommonJS exports (or convert fully to ES module + update imports consistently).
- `pages/api/search-nicus.js` top line uses `import axios = require('axios');` — unusual syntax (TypeScript-style import assignment) but the codebase includes `axios` dependency; prefer `const axios = require('axios')` or `import axios from 'axios'` if converting the file to ES modules.
- The code expects `place.formatted_phone_number` in the Places response but Nearby Search responses usually don't include phone numbers — phone often ends up `null`. To add phone numbers requires an extra Place Details call.
- Mock mode: set `MOCK_MODE=true` in your environment to make the API return canned results without calling Google APIs (useful for UI testing). The API checks `process.env.MOCK_MODE` and returns sample results.
- Place Details (optional): set `INCLUDE_PLACE_DETAILS=true` to enable fetching `formatted_phone_number`, `formatted_address`, `opening_hours`, and `website` via the Places Details API. This increases accuracy at the cost of extra API calls and latency.
  - New: per-request `?includeDetails=1` overrides the env flag and requests Place Details for this call only.
  - Caching: the API now uses a simple in-memory TTL cache for Place Details (24h) and Distance Matrix responses (1h) to reduce repeated API calls in warm containers.
  - Concurrency: Place Details fetches are concurrency-limited (default 4) to avoid spikes and rate limits.
  - Redis & local dev: a `docker-compose.yml` is included to run Redis locally. Start it with `docker compose up -d` and set `REDIS_URL=redis://127.0.0.1:6379`.
  - Rate limiting: when `REDIS_URL` is set the API uses Redis counters to rate-limit Google API calls per-minute (`GOOGLE_API_MAX_PER_MINUTE` env var, optional).
- UI and API are tightly coupled: `index.js` expects the exact fields returned by the API (see API contract above). Keep field names stable to avoid breaking the client.

Integration & external dependencies

- package.json shows: next@14, react@18.2, axios, tailwind/postcss/autoprefixer. See `package.json` for scripts.
- Google Maps APIs used: Geocoding API, Places API (nearbysearch), Distance Matrix API. These require billing and enabling the APIs in the Google Cloud project.

Debugging tips (what to check first)

- Missing API key -> server returns `{ error: 'API key not configured' }` immediately.
- Use browser DevTools Network tab to inspect `/api/search-nicus` request and the JSON response.
- Server logs: `pages/api/search-nicus.js` catches errors and logs `Error:` to the server console — check terminal where `npm run dev` runs for stack traces.
- If distances or phones look wrong: Nearby Search limits fields; phone numbers are not available without Place Details.

Where to start when changing features

- Small UI tweaks: edit `pages/index.js` (watch for React.createElement pattern).
- API changes: edit `pages/api/search-nicus.js` — preserve request/response shape unless updating the client too.
- Styling: `styles/globals.css` + `tailwind.config.js`.

Files of interest

- `pages/index.js` — main UI and fetch code
- `pages/api/search-nicus.js` — server logic and Google API calls
- `package.json` — scripts and deps
- `public/` — static images used by UI

If anything above is unclear or you'd like more details (example tests, mocks for Google APIs, or converting the API to ES modules/TypeScript), tell me which area and I'll expand the doc.
