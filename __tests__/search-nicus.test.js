const nock = require('nock');
const handler = require('../pages/api/search-nicus');

describe('search-nicus API', () => {
  beforeAll(() => {
    process.env.GOOGLE_MAPS_API_KEY = 'test-key';
  });

  afterEach(() => nock.cleanAll());

  test('returns results with distance and placeId', async () => {
    // mock geocode
    nock('https://maps.googleapis.com')
      .get(/geocode\/json/)
      .reply(200, { results: [{ geometry: { location: { lat: 40.0, lng: -73.0 } } }] });

    // mock nearbysearch
    nock('https://maps.googleapis.com')
      .get(/place\/nearbysearch\/json/)
      .reply(200, { results: [{ place_id: 'p1', name: 'Hospital A', vicinity: 'Addr A' }] });

    // mock distancematrix
    nock('https://maps.googleapis.com')
      .get(/distancematrix\/json/)
      .reply(200, { rows: [{ elements: [{ distance: { text: '1.2 mi', value: 1931 } }] }] });

    // invoke handler
    const req = { query: { location: '10001', radius: '20' } };
    const res = { _status: 200, status(code) { this._status = code; return this; }, json(obj) { this.body = obj; } };

    await handler(req, res);
    expect(res._status).toBe(200);
    expect(res.body.results).toBeInstanceOf(Array);
    expect(res.body.results[0].placeId).toBe('p1');
    expect(res.body.results[0].distance).toBeDefined();
  });
});
