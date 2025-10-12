# NICU Finder — Local development notes

Quick start

1. Copy a Google API key into `.env.local`:

```bash
GoogleMaps=your_real_api_key_here
```

2. (Optional) Start a local Redis for caching:

```bash
docker compose up -d
export REDIS_URL=redis://127.0.0.1:6379
```

5. Update Copilot instructions to mention docker-compose for Redis.

6. Run the Next dev server:

```bash
npm run dev
```

4. Or test the API handler directly without Next:

```bash
npm run test-api
# or request place details for that run
node ./scripts/test-api.js 10001 20 1 1
```

Flags

- `MOCK_MODE=true` returns canned results without calling Google.
- `INCLUDE_PLACE_DETAILS=true` or per-request `?includeDetails=1` enables Place Details API calls.
- `PERSIST_CACHE=true` enables on-disk .cache/ persistence.
- `REDIS_URL` enables Redis caching and the rate limiter.
