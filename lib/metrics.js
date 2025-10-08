// Simple process-local metrics for cache hits/misses and API call counts.
// Meant to be lightweight and safe for serverless warm containers.
const globalKey = '_nf_metrics';
if (!global[globalKey]) {
  global[globalKey] = { counts: {} };
}

function incr(name, n = 1) {
  const m = global[globalKey];
  m.counts[name] = (m.counts[name] || 0) + n;
}

function snapshot() {
  return Object.assign({}, global[globalKey].counts);
}

function reset() {
  global[globalKey].counts = {};
}

module.exports = { incr, snapshot, reset };
