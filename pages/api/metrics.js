const metrics = require('../../lib/metrics');

module.exports = function handler(req, res) {
  return res.status(200).json({ metrics: metrics.snapshot() });
};
