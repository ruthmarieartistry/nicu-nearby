import axios from "axios";

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
  const apiKey = process.env.GOOGLE_MAPS_API_KEY;

  if (!apiKey) return res.status(500).json({ error: "API key not configured" });
  if (!location)
    return res.status(400).json({ error: "Location parameter is required" });

  try {
    const geocodeUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(location)}&key=${apiKey}`;
    const geocodeResponse = await axios.get(geocodeUrl);
    if (
      !geocodeResponse.data.results ||
      geocodeResponse.data.results.length === 0
    )
      return res.status(404).json({ error: "Location not found" });

    const coords = geocodeResponse.data.results[0].geometry.location;
    const lat = coords.lat;
    const lng = coords.lng;
    const radiusMeters = parseFloat(radius) * 1609.34;

    const placesUrl = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${lat},${lng}&radius=${radiusMeters}&type=hospital&keyword=NICU+neonatal+intensive+care&key=${apiKey}`;
    const placesResponse = await axios.get(placesUrl);
    const places = (placesResponse.data.results || []).slice(0, 20);
    const preliminary = [];

    for (let i = 0; i < places.length; i++) {
      const place = places[i];
      const distanceUrl = `https://maps.googleapis.com/maps/api/distancematrix/json?origins=${lat},${lng}&destinations=place_id:${place.place_id}&units=imperial&key=${apiKey}`;
      const distanceResponse = await axios.get(distanceUrl);
      const element =
        (distanceResponse.data.rows &&
          distanceResponse.data.rows[0] &&
          distanceResponse.data.rows[0].elements &&
          distanceResponse.data.rows[0].elements[0]) ||
        {};
      const distanceText = element.distance ? element.distance.text : "N/A";
      const distanceValue = element.distance ? element.distance.value : 0;
      const distanceMiles = distanceValue / 1609.34;
      if (distanceMiles <= parseFloat(radius)) {
        preliminary.push({
          name: place.name,
          address: place.vicinity || place.formatted_address || "",
          distance: distanceText.replace(" mi", ""),
          distanceValue,
          rating: place.rating,
          reviews: place.user_ratings_total,
          placeId: place.place_id,
          phone: null,
          website: null,
          nicuLevel: null,
          hasNicU: false,
        });
      }
    }

    // Always check for NICU level from hospital name (fast, no API calls needed)
    for (let i = 0; i < preliminary.length; i++) {
      const item = preliminary[i];
      const name = item.name.toUpperCase();

      // Look for Level IV, III, II, I or numeric levels in the hospital name
      const levelMatch = item.name.match(/(?:NICU\s*)?Level\s*(IV|III|II|I|4|3|2|1)(?:\s|,|\.|\)|$)/i);
      if (levelMatch) {
        let level = levelMatch[1].toUpperCase();
        // Convert numeric to Roman numerals for consistency
        if (level === '1') level = 'I';
        else if (level === '2') level = 'II';
        else if (level === '3') level = 'III';
        else if (level === '4') level = 'IV';
        item.nicuLevel = 'Level ' + level;
      } else {
        // Fallback: Known hospital NICU levels
        // This is temporary until we integrate with a proper NICU database

        // Level IV NICUs (highest level)
        if (name.includes('MORGAN STANLEY') ||
            (name.includes('NYP') && name.includes('CHILDREN')) ||
            name.includes('CHILDRENS HOSPITAL LOS ANGELES') ||
            name.includes('STANFORD') && name.includes('CHILDREN') ||
            name.includes('UCSF') && name.includes('BENIOFF') ||
            name.includes('UCLA') && name.includes('MATTEL')) {
          item.nicuLevel = 'Level IV';
        }
        // Level III NICUs
        else if (name.includes('BROOKLYN HOSPITAL CENTER') ||
                 name.includes('CEDARS-SINAI') ||
                 name.includes('CEDARS SINAI') ||
                 name.includes('MOUNT SINAI') ||
                 name.includes('NYU LANGONE') ||
                 name.includes('PRESBYTERIAN') ||
                 name.includes('METHODIST') && name.includes('BROOKLYN') ||
                 name.includes('COHEN') && name.includes('CHILDREN') ||
                 name.includes('KAISER')) {
          item.nicuLevel = 'Level III';
        }
      }
    }

    // Fetch Place Details for complete address information (only if requested)
    const includeDetails = req.query.includeDetails === '1' || process.env.INCLUDE_PLACE_DETAILS === '1' || process.env.INCLUDE_PLACE_DETAILS === 'true';
    const concurrency = 4;

    if (includeDetails && preliminary.length > 0) {
      for (let i = 0; i < preliminary.length; i += concurrency) {
        const batch = preliminary.slice(i, i + concurrency).map(async (item) => {
          try {
            const detailsUrl =
              'https://maps.googleapis.com/maps/api/place/details/json?place_id=' +
              item.placeId +
              '&fields=name,formatted_phone_number,formatted_address,website,editorial_summary,types' +
              '&key=' +
              apiKey;
            const detailsResp = await axios.get(detailsUrl);
            const details = detailsResp.data && detailsResp.data.result ? detailsResp.data.result : {};

            if (details.formatted_phone_number) item.phone = details.formatted_phone_number;
            if (details.formatted_address) item.address = details.formatted_address;
            if (details.website) item.website = details.website;

            // If we don't already have a level, try to extract from editorial summary
            if (!item.nicuLevel) {
              const textToScan = [
                details.name || '',
                details.formatted_address || '',
                (details.editorial_summary && details.editorial_summary.overview) || ''
              ].join(' ');

              const levelMatch = textToScan.match(/(?:NICU\s*)?Level\s*(IV|III|II|I|4|3|2|1)(?:\s|,|\.|\)|$)/i);
              if (levelMatch) {
                let level = levelMatch[1].toUpperCase();
                if (level === '1') level = 'I';
                else if (level === '2') level = 'II';
                else if (level === '3') level = 'III';
                else if (level === '4') level = 'IV';
                item.nicuLevel = 'Level ' + level;
              }
            }
          } catch (err) {
            // ignore errors in details fetch
          }
        });
        await Promise.all(batch);
      }
    }

    preliminary.sort((a, b) => a.distanceValue - b.distanceValue);
    return res.status(200).json({ results: preliminary });
  } catch (err) {
    console.error("Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}

export default handler;
