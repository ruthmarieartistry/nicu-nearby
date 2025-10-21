const axios = require("axios");

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
          nicuLevel: null,
          hasNicU: false,
        });
      }
    }

    preliminary.sort((a, b) => a.distanceValue - b.distanceValue);
    return res.status(200).json({ results: preliminary });
  } catch (err) {
    console.error("Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}

module.exports = handler;
