let _reqCount = 0;

export default function handler(req, res) {
  _reqCount += 1;
  const mem = process.memoryUsage();
  res.status(200).json({
    uptimeSeconds: Math.round(process.uptime()),
    requests: _reqCount,
    memory: {
      rss: mem.rss,
      heapTotal: mem.heapTotal,
      heapUsed: mem.heapUsed,
      external: mem.external,
    },
    timestamp: Date.now(),
  });
}
