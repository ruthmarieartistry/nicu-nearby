#!/usr/bin/env python3
"""
Geocode all hospitals in the NICU database and add latitude/longitude coordinates.
Strategy: Try to get address from nicudata.com URL first, then fall back to name+county+state.
"""

import json
import time
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

def scrape_address_from_url(url):
    """Scrape the actual hospital address from nicudata.com"""
    if not url:
        return None

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find address in common HTML patterns
            text = soup.get_text()

            # Pattern: Street address with number
            address_pattern = r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Parkway|Pkwy)[,\s]+[\w\s]+,\s*[A-Z]{2}\s+\d{5}'
            match = re.search(address_pattern, text, re.IGNORECASE)

            if match:
                return match.group(0).strip()

        return None
    except Exception as e:
        return None

def geocode_address(address, api_key=None):
    """Geocode an address using Google Maps or Nominatim"""

    # Try Google Maps first if API key is available
    if api_key:
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': address,
                'key': api_key
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('results'):
                location = data['results'][0]['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'source': 'google',
                    'formatted_address': data['results'][0].get('formatted_address')
                }
        except Exception as e:
            print(f"    Google geocoding error: {e}")

    # Fallback to Nominatim (free, but rate-limited)
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'format': 'json',
            'q': address,
            'limit': 1
        }
        headers = {
            'User-Agent': 'NICU-Finder-App/1.0'
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        if data:
            return {
                'lat': float(data[0]['lat']),
                'lng': float(data[0]['lon']),
                'source': 'nominatim',
                'formatted_address': data[0].get('display_name')
            }
    except Exception as e:
        print(f"    Nominatim geocoding error: {e}")

    return None

def main():
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / 'data' / 'nicu-database.json'

    # Check for Google Maps API key
    api_key = os.environ.get('GoogleMaps') or os.environ.get('GOOGLE_MAPS_API_KEY')

    if api_key:
        print(f"✓ Using Google Maps API for geocoding")
    else:
        print(f"⚠ No Google Maps API key found, using Nominatim (slower, rate-limited)")

    # Load database
    print(f"\nLoading database from {db_path}")
    with open(db_path, 'r', encoding='utf-8') as f:
        database = json.load(f)

    nicus = database.get('nicus', [])
    print(f"Found {len(nicus)} hospitals to geocode")

    # Count how many already have coordinates
    already_geocoded = sum(1 for n in nicus if n.get('lat') and n.get('lng'))
    print(f"Already geocoded: {already_geocoded}")
    print(f"Need to geocode: {len(nicus) - already_geocoded}")

    if already_geocoded == len(nicus):
        print(f"\n✓ All hospitals already have coordinates!")
        return

    # Geocode each hospital
    geocoded_count = 0
    failed_count = 0
    skipped_count = 0
    from_url_count = 0
    from_fallback_count = 0

    for i, nicu in enumerate(nicus):
        # Skip if already has coordinates
        if nicu.get('lat') and nicu.get('lng'):
            skipped_count += 1
            if (i + 1) % 100 == 0:
                print(f"[{i+1}/{len(nicus)}] Progress check...")
            continue

        print(f"\n[{i+1}/{len(nicus)}] {nicu['name']} ({nicu['state']})")

        # Strategy 1: Try to scrape address from URL
        address_from_url = None
        if nicu.get('url'):
            print(f"  Trying to scrape address from URL...")
            address_from_url = scrape_address_from_url(nicu['url'])
            if address_from_url:
                print(f"  Found address: {address_from_url}")
            time.sleep(0.5)  # Be nice to nicudata.com

        # Strategy 2: Use name + county + state as fallback
        fallback_address = f"{nicu['name']}, {nicu.get('county', '')}, {nicu['state']}, USA"

        # Try geocoding with scraped address first, then fallback
        coords = None
        if address_from_url:
            coords = geocode_address(address_from_url, api_key)
            if coords:
                from_url_count += 1
                coords['address_source'] = 'scraped'

        if not coords:
            print(f"  Using fallback...")
            coords = geocode_address(fallback_address, api_key)
            if coords:
                from_fallback_count += 1
                coords['address_source'] = 'fallback'

        if coords:
            nicu['lat'] = coords['lat']
            nicu['lng'] = coords['lng']
            nicu['geocode_source'] = coords['source']
            nicu['address_source'] = coords['address_source']
            if coords.get('formatted_address'):
                nicu['geocoded_address'] = coords['formatted_address']
            geocoded_count += 1
            print(f"  ✓ {coords['lat']:.6f}, {coords['lng']:.6f} (via {coords['source']}, from {coords['address_source']})")

            # Save progress every 20 hospitals
            if geocoded_count % 20 == 0:
                print(f"\n  💾 Saving progress... ({geocoded_count} geocoded so far)")
                with open(db_path, 'w', encoding='utf-8') as f:
                    json.dump(database, f, indent=2, ensure_ascii=False)
        else:
            failed_count += 1
            print(f"  ✗ Failed to geocode")

        # Rate limiting
        if not api_key:
            time.sleep(1.5)  # Nominatim requires 1 req/sec
        else:
            time.sleep(0.2)  # Be nice even with Google

    # Final save
    print(f"\n\n💾 Saving final results...")
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Geocoding complete!")
    print(f"  Successfully geocoded: {geocoded_count}")
    print(f"    - From scraped URLs: {from_url_count}")
    print(f"    - From fallback (name+county+state): {from_fallback_count}")
    print(f"  Skipped (already had coords): {skipped_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total with coordinates: {sum(1 for n in nicus if n.get('lat') and n.get('lng'))}/{len(nicus)}")

if __name__ == '__main__':
    main()
