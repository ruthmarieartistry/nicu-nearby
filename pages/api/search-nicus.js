const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { createClient } = require('redis');
const metrics = require(path.join(process.cwd(), 'lib', 'metrics'));

// helper: fetch with retries and exponential backoff
async function fetchWithRetries(url, attempts = 3, baseDelay = 200) {
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try {
      const resp = await axios.get(url);
      return resp;
    } catch (err) {
      lastErr = err;
      const delay = baseDelay * Math.pow(2, i);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw lastErr;
}

// Rate limiter: use Redis to limit Google API calls per-minute when REDIS_URL is set.
async function googleRateLimit(apiName, maxPerMinute) {
  try {
    const client = await ensureRedis();
    if (!client) return true; // no redis -> allow
    const minuteKey = Math.floor(Date.now() / 60000);
    const key = `quota:google:${apiName}:${minuteKey}`;
    const count = await client.incr(key);
    if (count === 1) await client.expire(key, 61);
    if (maxPerMinute && count > maxPerMinute) return false;
    return true;
  } catch (err) {
    return true; // fail open
  }
}

// optional simple on-disk cache (process-wide) when PERSIST_CACHE=true
const CACHE_DIR = path.resolve(process.cwd(), '.cache');
function ensureCacheDir() {
  try { fs.mkdirSync(CACHE_DIR, { recursive: true }); } catch (e) { /* ignore */ }
}
async function fileCacheGet(key) {
  try {
    const file = path.join(CACHE_DIR, encodeURIComponent(key));
    const stat = await fs.promises.stat(file).catch(() => null);
    if (!stat) return null;
    const raw = await fs.promises.readFile(file, 'utf8');
    const obj = JSON.parse(raw);
    if (obj.expiry && Date.now() > obj.expiry) {
      await fs.promises.unlink(file).catch(() => {});
      return null;
    }
    return obj.value;
  } catch (err) {
    return null;
  }
}
async function fileCacheSet(key, value, ttlMs) {
  try {
    ensureCacheDir();
    const file = path.join(CACHE_DIR, encodeURIComponent(key));
    const obj = { value, expiry: ttlMs ? Date.now() + ttlMs : null };
    await fs.promises.writeFile(file, JSON.stringify(obj), 'utf8');
  } catch (err) {
    // ignore cache write failures
  }
}

// Redis client wrapper (optional). If REDIS_URL is set, we'll try to use Redis for shared caching.
let redisClient = null;
async function ensureRedis() {
  if (redisClient) return redisClient;
  const url = process.env.REDIS_URL || process.env.REDIS_TLS_URL;
  if (!url) return null;
  try {
    const client = createClient({ url });
    client.on('error', () => {});
    await client.connect();
    redisClient = client;
    return redisClient;
  } catch (err) {
    // fail open: do not throw, fall back to file/in-memory caches
    redisClient = null;
    return null;
  }
}

async function redisGet(key) {
  try {
    const client = await ensureRedis();
    if (!client) return null;
    const raw = await client.get(key);
    return raw ? JSON.parse(raw) : null;
  } catch (err) {
    return null;
  }
}

async function redisSetEx(key, ttlSec, value) {
  try {
    const client = await ensureRedis();
    if (!client) return;
    await client.setEx(key, ttlSec, JSON.stringify(value));
  } catch (err) {
    // ignore
  }
}

module.exports = async function handler(req, res) {
  const location = req.query.location;
  const radius = req.query.radius || 60;
  const apiKey = process.env.GOOGLE_MAPS_API_KEY;

  // Mock mode: return canned results for local UI/testing without calling Google APIs.
  if (process.env.MOCK_MODE === 'true' || process.env.MOCK_MODE === '1') {
    const mockResults = [
      { name: 'Mock NICU Hospital A', address: '123 Mock St, Testville', distance: '1.2', distanceValue: 1931, rating: 4.5, reviews: 12, placeId: 'mock-1', phone: '555-0101' },
      { name: 'Mock NICU Hospital B', address: '456 Example Rd, Demo City', distance: '5.6', distanceValue: 9012, rating: 4.0, reviews: 5, placeId: 'mock-2', phone: null }
    ];
    return res.status(200).json({ results: mockResults });
  }

  if (!apiKey) {
    return res.status(500).json({ error: 'API key not configured' });
  }

  if (!location) {
    return res.status(400).json({ error: 'Location parameter is required' });
  }

  try {
    const geocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + encodeURIComponent(location) + '&key=' + apiKey;
    const geocodeResponse = await axios.get(geocodeUrl);

    if (!geocodeResponse.data.results || geocodeResponse.data.results.length === 0) {
      return res.status(404).json({ error: 'Location not found' });
    }

    const coords = geocodeResponse.data.results[0].geometry.location;
    const lat = coords.lat;
    const lng = coords.lng;
    const radiusMeters = parseFloat(radius) * 1609.34;

    const placesUrl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + lat + ',' + lng + '&radius=' + radiusMeters + '&type=hospital&keyword=NICU+neonatal+intensive+care&key=' + apiKey;
    const placesResponse = await axios.get(placesUrl);

    const places = placesResponse.data.results.slice(0, 20);

    // Simple in-memory TTL caches (process-local). Useful for warm serverless containers.
    // Keys: place details by place_id, distances by origin:place_id
    if (!global._nf_cache) {
      global._nf_cache = {
        placeDetails: new Map(),
        distances: new Map()
      };
    }
    const placeDetailsCache = global._nf_cache.placeDetails;
    const distancesCache = global._nf_cache.distances;

    const cacheGet = (map, key) => {
      const v = map.get(key);
      if (!v) return null;
      if (v.expiry && Date.now() > v.expiry) { map.delete(key); return null; }
      return v.value;
    };
    const cacheSet = (map, key, value, ttlMs) => {
      map.set(key, { value, expiry: ttlMs ? Date.now() + ttlMs : null });
    };

    // Build a single Distance Matrix call for up to 25 destinations (we only have up to 20)
    const destPlaceIds = places.map(p => 'place_id:' + p.place_id).join('|');
    const distanceUrl = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + lat + ',' + lng + '&destinations=' + destPlaceIds + '&units=imperial&key=' + apiKey;

  // Try to use cached distance result per origin+dest list key
  const distanceCacheKey = lat + ',' + lng + '::' + destPlaceIds;
  let distanceResponse = cacheGet(distancesCache, distanceCacheKey);
  if (distanceResponse) metrics.incr('cache.dist.memory.hit'); else metrics.incr('cache.dist.memory.miss');
    if (!distanceResponse) {
      // try Redis first
  const r = await redisGet('dist::' + distanceCacheKey).catch(() => null);
  if (r) { distanceResponse = r; cacheSet(distancesCache, distanceCacheKey, distanceResponse, 1000 * 60 * 60); metrics.incr('cache.dist.redis.hit'); }
    }

    if (!distanceResponse) {
      // try on-disk cache first when enabled
      if (process.env.PERSIST_CACHE === 'true' || process.env.PERSIST_CACHE === '1') {
        const ondisk = await fileCacheGet(distanceCacheKey).catch(() => null);
        if (ondisk) { distanceResponse = ondisk; cacheSet(distancesCache, distanceCacheKey, distanceResponse, 1000 * 60 * 60); metrics.incr('cache.dist.disk.hit'); }
      }
    }

      if (!distanceResponse) {
        const allowed = await googleRateLimit('distancematrix', parseInt(process.env.GOOGLE_API_MAX_PER_MINUTE || '0') || null);
        if (!allowed) {
          // refuse to call Google; continue without distances (will result in no results)
          console.error('Rate limit exceeded for Distance Matrix');
          return res.status(503).json({ error: 'Rate limit exceeded, try again later' });
        }
  metrics.incr('api.distancematrix.call');
  const resp = await fetchWithRetries(distanceUrl, 3, 200);
      distanceResponse = resp.data;
      // cache distances briefly (1 hour)
      cacheSet(distancesCache, distanceCacheKey, distanceResponse, 1000 * 60 * 60);
      if (process.env.PERSIST_CACHE === 'true' || process.env.PERSIST_CACHE === '1') {
        await fileCacheSet(distanceCacheKey, distanceResponse, 1000 * 60 * 60).catch(() => {});
      }
      // store to Redis if available
      await redisSetEx('dist::' + distanceCacheKey, 60 * 60, distanceResponse).catch(() => {});
    }

    const rows = (distanceResponse && distanceResponse.rows && distanceResponse.rows[0] && distanceResponse.rows[0].elements) || [];
    const parsed = [];

    for (let i = 0; i < places.length; i++) {
      const place = places[i];
      const element = rows[i] || {};
      const distanceText = element.distance ? element.distance.text : 'N/A';
      const distanceValue = element.distance ? element.distance.value : 0;
      const distanceMiles = distanceValue / 1609.34;
      parsed.push({ place, distanceText, distanceValue, distanceMiles });
    }

    // Filter by radius
    const maxRadius = parseFloat(radius);
    let filtered = parsed.filter(p => p.distanceMiles <= maxRadius);

    // Support per-request override to include Place Details: ?includeDetails=1 takes precedence over env
    const includeDetails = (req.query.includeDetails === '1') || (process.env.INCLUDE_PLACE_DETAILS === 'true' || process.env.INCLUDE_PLACE_DETAILS === '1');

    // If details requested, fetch Place Details concurrently with a small pool and cache results (24h)
    const placeDetailsTTL = 1000 * 60 * 60 * 24; // 24 hours
    const concurrency = 4;
    const pool = async (items, worker, concurrency) => {
      const results = new Array(items.length);
      let i = 0;
      const runner = async () => {
        while (true) {
          const idx = i++;
          if (idx >= items.length) return;
          try {
            results[idx] = await worker(items[idx], idx);
          } catch (err) {
            results[idx] = { error: err };
          }
        }
      };
      const runners = [];
      for (let j = 0; j < Math.min(concurrency, items.length); j++) runners.push(runner());
      await Promise.all(runners);
      return results;
    };

    let detailsByPlaceId = {};
    if (includeDetails && filtered.length > 0) {
      const toFetch = filtered.map(p => p.place.place_id);
      // worker uses cache
      const worker = async (placeId) => {
        const cached = cacheGet(placeDetailsCache, placeId);
        if (cached) return cached;
        // try Redis first
  const r = await redisGet('place::' + placeId).catch(() => null);
  if (r) { cacheSet(placeDetailsCache, placeId, r, placeDetailsTTL); metrics.incr('cache.place.redis.hit'); return r; }
        // try on-disk cache when enabled
        if (process.env.PERSIST_CACHE === 'true' || process.env.PERSIST_CACHE === '1') {
            const ondisk = await fileCacheGet(placeId).catch(() => null);
            if (ondisk) { cacheSet(placeDetailsCache, placeId, ondisk, placeDetailsTTL); metrics.incr('cache.place.disk.hit'); return ondisk; }
        }
        const detailsUrl = 'https://maps.googleapis.com/maps/api/place/details/json?place_id=' + placeId + '&fields=formatted_phone_number,formatted_address,opening_hours,website&key=' + apiKey;
        const allowed = await googleRateLimit('placedetails', parseInt(process.env.GOOGLE_API_MAX_PER_MINUTE || '0') || null);
        if (!allowed) {
          console.error('Rate limit exceeded for Place Details');
          return null;
        }
  metrics.incr('api.placedetails.call');
  const resp = await fetchWithRetries(detailsUrl, 3, 200);
        const details = resp.data.result || {};
        cacheSet(placeDetailsCache, placeId, details, placeDetailsTTL);
        if (process.env.PERSIST_CACHE === 'true' || process.env.PERSIST_CACHE === '1') {
          await fileCacheSet(placeId, details, placeDetailsTTL).catch(() => {});
        }
  // write to redis
  await redisSetEx('place::' + placeId, 24 * 60 * 60, details).catch(() => {});
  metrics.incr('cache.place.redis.set');
        return details;
      };

      const detailResults = await pool(toFetch, worker, concurrency);
      for (let i = 0; i < toFetch.length; i++) {
        const pid = toFetch[i];
        if (detailResults[i] && !detailResults[i].error) {
          detailsByPlaceId[pid] = detailResults[i];
        }
      }
    }

    // Build results
    const results = filtered.map(p => {
      const place = p.place;
      const details = detailsByPlaceId[place.place_id] || {};
      const phone = details.formatted_phone_number || place.formatted_phone_number || null;
      const address = details.formatted_address || place.vicinity;
      return {
        name: place.name,
        address: address,
        distance: (p.distanceText || 'N/A').toString().replace(' mi', ''),
        distanceValue: p.distanceValue,
        rating: place.rating,
        reviews: place.user_ratings_total,
        placeId: place.place_id,
        phone: phone,
        website: details.website || null,
        opening_hours: details.opening_hours || null
      };
    });

    results.sort((a, b) => a.distanceValue - b.distanceValue);

    return res.status(200).json({ results: results });
  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({ error: 'Failed to search for NICU facilities' });
  }
};