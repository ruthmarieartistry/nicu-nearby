#!/usr/bin/env python3
"""
Simplified geocoding - batch process all hospitals
"""
import json
import time
import os
import sys
import requests

def geocode(name, county, state, api_key):
    """Geocode a single hospital"""
    query = f"{name}, {county}, {state}, USA"
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
        response = requests.get(url, params={'address': query, 'key': api_key}, timeout=10)
        data = response.json()

        if data.get('results'):
            loc = data['results'][0]['geometry']['location']
            addr = data['results'][0].get('formatted_address')
            return {'lat': loc['lat'], 'lng': loc['lng'], 'address': addr}
    except:
        pass

    return None

def main():
    api_key = os.environ.get('GoogleMaps')
    if not api_key:
        print("ERROR: GoogleMaps env var not set")
        sys.exit(1)

    print("Loading database...")
    sys.stdout.flush()

    with open('data/nicu-database.json', 'r') as f:
        db = json.load(f)

    total = len(db['nicus'])
    need_geocoding = sum(1 for n in db['nicus'] if not n.get('lat'))

    print(f"Total: {total}, Need geocoding: {need_geocoding}")
    sys.stdout.flush()

    done = 0
    failed = 0

    for i, nicu in enumerate(db['nicus']):
        if nicu.get('lat'):
            continue

        coords = geocode(nicu['name'], nicu.get('county', ''), nicu['state'], api_key)

        if coords:
            nicu['lat'] = coords['lat']
            nicu['lng'] = coords['lng']
            if coords.get('address'):
                nicu['formatted_address'] = coords['address']
            done += 1

            if done % 10 == 0:
                print(f"[{done}/{need_geocoding}] {nicu['name'][:40]} -> {coords['lat']:.4f},{coords['lng']:.4f}")
                sys.stdout.flush()

            if done % 50 == 0:
                print(f"Saving progress...")
                sys.stdout.flush()
                with open('data/nicu-database.json', 'w') as f:
                    json.dump(db, f, indent=2)
        else:
            failed += 1
            print(f"FAILED: {nicu['name']}")
            sys.stdout.flush()

        time.sleep(0.05)

    print(f"\nSaving final...")
    sys.stdout.flush()
    with open('data/nicu-database.json', 'w') as f:
        json.dump(db, f, indent=2)

    print(f"\nDONE! Geocoded: {done}, Failed: {failed}")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
