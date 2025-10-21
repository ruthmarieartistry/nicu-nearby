export const runtime = 'edge';

// Import database directly (works in Edge Runtime)
import nicuDatabaseImport from '../../data/nicu-database.json';
const nicuDatabase = nicuDatabaseImport;

// Calculate distance between two points using Haversine formula
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 3959; // Earth's radius in miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  return distance;
}

// Function to match a hospital name with NICU database
function matchNicuData(hospitalName, state) {
  if (!nicuDatabase || !nicuDatabase.nicus) return null;

  // Clean the hospital name for matching - be more aggressive
  const cleanName = (name) => name
    .toLowerCase()
    .replace(/the\s+/gi, '')  // Remove "the"
    .replace(/\s+(hospital|medical center|health|healthcare|regional|memorial|medical|center|clinic|children'?s?|women'?s?|university|inpatient|hospital center)\s*/gi, ' ')
    .replace(/[^\w\s]/g, ' ')  // Replace punctuation with space
    .replace(/\s+/g, ' ')  // Collapse multiple spaces
    .trim();

  const searchName = cleanName(hospitalName);
  const searchWords = searchName.split(' ').filter(w => w.length > 2); // Words longer than 2 chars

  let bestMatch = null;
  let bestScore = 0;

  // Try to find best match in the database
  for (const nicu of nicuDatabase.nicus) {
    const dbName = cleanName(nicu.name);
    const dbWords = dbName.split(' ').filter(w => w.length > 2);

    // Count matching words
    let matchCount = 0;
    for (const word of searchWords) {
      if (dbWords.some(dbWord => dbWord.includes(word) || word.includes(dbWord))) {
        matchCount++;
      }
    }

    // Calculate match score
    const score = matchCount / Math.max(searchWords.length, dbWords.length);

    // Check if this is a better match and meets minimum threshold
    if (score > bestScore && score >= 0.5) {
      // Prefer matches from the same state if available
      const stateMatch = !state ||
        nicu.state.toLowerCase().includes(state.toLowerCase()) ||
        state.toLowerCase().includes(nicu.state.toLowerCase());

      if (stateMatch || score >= 0.7) {  // Higher threshold if state doesn't match
        bestScore = score;
        bestMatch = nicu;
      }
    }
  }

  if (bestMatch) {
    return {
      name: bestMatch.name,
      nicuLevel: bestMatch.nicuLevel,
      beds: bestMatch.beds,
      county: bestMatch.county,
      state: bestMatch.state,
      url: bestMatch.url
    };
  }

  return null;
}

async function handler(req, res) {
  if (process.env.MOCK_MODE === "1" || process.env.MOCK_MODE === "true") {
    return res
      .status(200)
      .json({
        results: [
          {
            name: "Mock NICU",
            address: "123 Mock St",
            distance: "N/A",
            distanceValue: 0,
            rating: null,
            reviews: null,
            placeId: null,
            phone: null,
            nicuLevel: null,
            hasNicU: true,
          },
        ],
      });
  }

  const location = req.query.location;
  const radius = req.query.radius || 60;
  const apiKey = process.env.GoogleMaps;

  if (!apiKey) return res.status(500).json({ error: "API key not configured" });
  if (!location)
    return res.status(400).json({ error: "Location parameter is required" });

  try {
    // Try Google Maps Geocoding first
    let geocodeResponse;
    let coords;
    let userState = null;

    try {
      const geocodeUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(location)}&key=${apiKey}`;
      const geocodeRes = await fetch(geocodeUrl);
      geocodeResponse = { data: await geocodeRes.json() };

      if (
        geocodeResponse.data.results &&
        geocodeResponse.data.results.length > 0
      ) {
        coords = geocodeResponse.data.results[0].geometry.location;

        // Extract state from address components
        const addressComponents = geocodeResponse.data.results[0].address_components;
        for (const component of addressComponents) {
          if (component.types.includes('administrative_area_level_1')) {
            userState = component.long_name;
            break;
          }
        }
      }
    } catch (geocodeErr) {
      console.error("Google Geocoding failed:", geocodeErr.message);
    }

    // Fallback to free Nominatim geocoding if Google fails (due to billing, etc.)
    if (!coords) {
      console.log("Using fallback geocoding service...");
      try {
        // Add USA to zip codes to avoid international conflicts
        const searchQuery = /^\d{5}(-\d{4})?$/.test(location.trim()) ? `${location} USA` : location;
        const nominatimUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=1`;
        const nominatimRes = await fetch(nominatimUrl, {
          headers: {
            'User-Agent': 'NICU-Finder-App/1.0'
          }
        });
        const nominatimData = await nominatimRes.json();

        if (nominatimData && nominatimData.length > 0) {
          coords = {
            lat: parseFloat(nominatimData[0].lat),
            lng: parseFloat(nominatimData[0].lon)
          };
          console.log("Fallback geocoding successful:", coords, "for", searchQuery);
        } else {
          return res.status(404).json({ error: "Location not found" });
        }
      } catch (nominatimErr) {
        console.error("Fallback geocoding failed:", nominatimErr.message);
        return res.status(404).json({ error: "Location not found" });
      }
    }

    const lat = coords.lat;
    const lng = coords.lng;

    // DISABLED: Google Maps Places search to avoid fuzzy matching errors
    // Now using ONLY the curated NICU database for accurate results
    // This prevents dialysis centers and other non-NICU facilities from appearing
    const preliminary = [];

    console.log(`Searching ${nicuDatabase.nicus.length} NICUs from curated database (Google Maps search disabled)`);

    // Skip Google Maps matching entirely
    if (false) {
      const place = null;
      let distanceText = "N/A";
      let distanceValue = 0;
      let distanceMiles = 0;

      // Try Google Distance Matrix API first
      try {
        const distanceUrl = `https://maps.googleapis.com/maps/api/distancematrix/json?origins=${lat},${lng}&destinations=place_id:${place.place_id}&units=imperial&key=${apiKey}`;
        const distanceRes = await fetch(distanceUrl);
        const distanceData = await distanceRes.json();
        const element =
          (distanceData.rows &&
            distanceData.rows[0] &&
            distanceData.rows[0].elements &&
            distanceData.rows[0].elements[0]) ||
          {};

        if (element.distance) {
          distanceText = element.distance.text;
          distanceValue = element.distance.value;
          distanceMiles = distanceValue / 1609.34;
        }
      } catch (distErr) {
        // Distance Matrix API failed (likely billing issue), use fallback calculation
      }

      // Fallback: Calculate straight-line distance using Haversine formula
      if (distanceValue === 0 && place.geometry && place.geometry.location) {
        const placeLat = place.geometry.location.lat;
        const placeLng = place.geometry.location.lng;
        distanceMiles = calculateDistance(lat, lng, placeLat, placeLng);
        distanceValue = distanceMiles * 1609.34; // Convert to meters for sorting
        distanceText = distanceMiles.toFixed(1);
      }

      if (distanceMiles <= parseFloat(radius)) {
        // Try to match with NICU database - pass user state for better matching
        const nicuData = matchNicuData(place.name, userState || place.vicinity || place.formatted_address);

        // ONLY add hospitals that matched in our NICU database
        if (nicuData) {
          // Extract coordinates from Google Maps
          const placeLat = place.geometry && place.geometry.location ? place.geometry.location.lat : null;
          const placeLng = place.geometry && place.geometry.location ? place.geometry.location.lng : null;

          preliminary.push({
            name: place.name, // Use Google Maps name (actual hospital found nearby)
            address: place.vicinity || place.formatted_address || `${nicuData.county}, ${nicuData.state}`,
            distance: distanceText.replace(" mi", ""),
            distanceValue,
            rating: place.rating,
            reviews: place.user_ratings_total,
            placeId: place.place_id,
            phone: null,
            website: nicuData.url,
            nicuLevel: nicuData.nicuLevel,
            beds: nicuData.beds,
            hasNicU: true,
            state: nicuData.state,
            county: nicuData.county,
            databaseName: nicuData.name, // Keep database name for reference
            lat: placeLat, // Save for caching
            lng: placeLng  // Save for caching
          });
        }
      }
    }

    // ALSO search our database directly for NICUs with coordinates
    console.log(`Also searching database for NICUs with coordinates...`);
    const radiusMiles = parseFloat(radius);
    const alreadyAdded = new Set(preliminary.map(p => p.databaseName?.toLowerCase()));

    for (const nicu of nicuDatabase.nicus) {
      // Skip if already added from Google Maps
      if (alreadyAdded.has(nicu.name.toLowerCase())) {
        continue;
      }

      // Skip if no coordinates
      if (!nicu.lat || !nicu.lng) {
        continue;
      }

      // Calculate distance
      const distance = calculateDistance(lat, lng, nicu.lat, nicu.lng);

      if (distance <= radiusMiles) {
        preliminary.push({
          name: nicu.name,
          address: nicu.formatted_address || `${nicu.county}, ${nicu.state}`,
          distance: distance.toFixed(1),
          distanceValue: distance * 1609.34,
          rating: null,
          reviews: null,
          placeId: null,
          phone: nicu.phone || null,
          website: nicu.url,
          nicuLevel: nicu.nicuLevel,
          beds: nicu.beds,
          hasNicU: true,
          state: nicu.state,
          county: nicu.county,
          databaseName: nicu.name,
          lat: nicu.lat,
          lng: nicu.lng,
          source: 'database' // Mark as from database directly
        });
      }
    }

    console.log(`Added ${preliminary.filter(p => p.source === 'database').length} additional NICUs from database`);

    // Note: Phone numbers are now stored in the database, no need for Place Details API calls!
    // This saves ~$0.005-$0.017 per hospital on every "Show All Details" request.

    preliminary.sort((a, b) => a.distanceValue - b.distanceValue);

    console.log(`Returning ${preliminary.length} NICUs (matched from database only)`);

    return res.status(200).json({ results: preliminary });
  } catch (err) {
    console.error("Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}

export default handler;
