#!/usr/bin/env python3
"""
Simple geocoding script - geocode all hospitals using name+county+state.
Fast, reliable, and costs about $8 for all 1,597 hospitals.
"""

import json
import time
import os
from pathlib import Path
import requests

def geocode_hospital(name, county, state, api_key):
    """Geocode using Google Maps Geocoding API"""
    try:
        query = f"{name}, {county}, {state}, USA"
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': query,
            'key': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get('results'):
            location = data['results'][0]['geometry']['location']
            return {
                'lat': location['lat'],
                'lng': location['lng'],
                'formatted_address': data['results'][0].get('formatted_address')
            }
    except Exception as e:
        print(f"    Error: {e}")

    return None

def main():
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / 'data' / 'nicu-database.json'

    # Check for API key
    api_key = os.environ.get('GoogleMaps') or os.environ.get('GOOGLE_MAPS_API_KEY')

    if not api_key:
        print("ERROR: GoogleMaps API key not found!")
        print("Please set the GoogleMaps environment variable")
        return

    print(f"✓ Using Google Maps Geocoding API")
    print(f"  Estimated cost: ~$8 for 1,597 hospitals\n")

    # Load database
    print(f"Loading database from {db_path}")
    with open(db_path, 'r', encoding='utf-8') as f:
        database = json.load(f)

    nicus = database.get('nicus', [])
    print(f"Found {len(nicus)} hospitals\n")

    # Count existing
    already_geocoded = sum(1 for n in nicus if n.get('lat') and n.get('lng'))
    print(f"Already geocoded: {already_geocoded}")
    print(f"Need to geocode: {len(nicus) - already_geocoded}\n")

    if already_geocoded == len(nicus):
        print("✓ All hospitals already have coordinates!")
        return

    # Geocode
    geocoded = 0
    failed = 0
    skipped = 0

    for i, nicu in enumerate(nicus):
        if nicu.get('lat') and nicu.get('lng'):
            skipped += 1
            continue

        if geocoded % 50 == 0 and geocoded > 0:
            print(f"\n[{i+1}/{len(nicus)}] Progress: {geocoded} geocoded, {failed} failed")

        coords = geocode_hospital(nicu['name'], nicu.get('county', ''), nicu['state'], api_key)

        if coords:
            nicu['lat'] = coords['lat']
            nicu['lng'] = coords['lng']
            if coords.get('formatted_address'):
                nicu['formatted_address'] = coords['formatted_address']
            geocoded += 1

            # Print occasional updates
            if geocoded % 10 == 0:
                print(f"  [{geocoded}] {nicu['name'][:40]} -> {coords['lat']:.4f}, {coords['lng']:.4f}")

            # Save progress every 100
            if geocoded % 100 == 0:
                print(f"\n💾 Saving progress...")
                with open(db_path, 'w', encoding='utf-8') as f:
                    json.dump(database, f, indent=2, ensure_ascii=False)
        else:
            failed += 1
            print(f"  ✗ Failed: {nicu['name']}")

        # Small delay to be respectful
        time.sleep(0.05)

    # Final save
    print(f"\n\n💾 Saving final results...")
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Geocoding complete!")
    print(f"  Successfully geocoded: {geocoded}")
    print(f"  Skipped (already had coords): {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Total with coordinates: {sum(1 for n in nicus if n.get('lat') and n.get('lng'))}/{len(nicus)}")

if __name__ == '__main__':
    main()
