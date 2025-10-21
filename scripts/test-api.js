// Simple test runner for pages/api/search-nicus.js
// Loads .env.local (if present) and invokes the handler function with mocked req/res

require("dotenv").config({ path: ".env.local" });
const handler = require("../pages/api/search-nicus");

const req = {
  query: {
    location: process.argv[2] || "10001",
    radius: process.argv[3] || "20",
  },
};
// optional third arg to request details per-call
if (process.argv[4] === "1" || process.argv[4] === "true") {
  req.query.includeDetails = "1";
}

const res = {
  _status: 200,
  status(code) {
    this._status = code;
    return this;
  },
  json(obj) {
    console.log("STATUS", this._status || 200);
    console.log(JSON.stringify(obj, null, 2));
  },
};

(async () => {
  try {
    await handler(req, res);
  } catch (err) {
    console.error("Handler threw:", err && err.stack ? err.stack : err);
  }
})();
