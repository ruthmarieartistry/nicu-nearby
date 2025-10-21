export const runtime = 'edge';

let _reqCount = 0;

export default function handler(req, res) {
  _reqCount += 1;
  // Note: process.memoryUsage() and process.uptime() not available in Edge Runtime
  res.status(200).json({
    requests: _reqCount,
    timestamp: Date.now(),
    runtime: 'edge'
  });
}
