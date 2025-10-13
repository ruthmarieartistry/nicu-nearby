#!/usr/bin/env python3
"""
Fetch phone numbers for all hospitals using Google Places API
One-time operation to add phone numbers to database
"""

import json
import requests
import os
import time
import sys

def search_place_and_get_phone(name, address, api_key):
    """Search for a place and get its phone number"""
    try:
        # First, search for the place to get place_id
        search_query = f"{name}, {address}"
        search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        search_params = {
            'input': search_query,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'key': api_key
        }

        search_resp = requests.get(search_url, params=search_params, timeout=10)
        search_data = search_resp.json()

        if search_data.get('status') != 'OK' or not search_data.get('candidates'):
            return None

        place_id = search_data['candidates'][0]['place_id']

        # Now get phone number using place_id
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'fields': 'formatted_phone_number',
            'key': api_key
        }

        details_resp = requests.get(details_url, params=details_params, timeout=10)
        details_data = details_resp.json()

        if details_data.get('status') == 'OK' and details_data.get('result'):
            return details_data['result'].get('formatted_phone_number')

        return None

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def main():
    # Load API key
    api_key = os.environ.get('GoogleMaps')
    if not api_key:
        print("Error: GoogleMaps API key not found in environment")
        sys.exit(1)

    # Load database
    db_path = 'data/nicu-database.json'
    with open(db_path, 'r') as f:
        db = json.load(f)

    print(f"Loaded database with {len(db['nicus'])} hospitals")

    # Find hospitals that need phone numbers
    need_phone = [n for n in db['nicus'] if not n.get('phone')]
    print(f"Need to fetch phone numbers for {len(need_phone)} hospitals\n")

    # Fetch phone numbers
    success_count = 0
    fail_count = 0

    for i, nicu in enumerate(need_phone, 1):
        # Build address string
        if nicu.get('formatted_address'):
            address = nicu['formatted_address']
        else:
            address = f"{nicu.get('county', '')}, {nicu.get('state', '')}"

        print(f"[{i}/{len(need_phone)}] {nicu['name'][:45]}", end=' ', flush=True)

        phone = search_place_and_get_phone(nicu['name'], address, api_key)

        if phone:
            nicu['phone'] = phone
            success_count += 1
            print(f"-> {phone}")
        else:
            fail_count += 1
            print("-> Not found")

        # Save progress every 50 hospitals
        if i % 50 == 0:
            print("Saving progress...")
            with open(db_path, 'w') as f:
                json.dump(db, f, indent=2)

        # Rate limiting - 0.05 seconds between requests
        time.sleep(0.05)

    # Save final results
    print("\nSaving final...")
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)

    print(f"\nDONE! Success: {success_count}, Failed: {fail_count}")

if __name__ == '__main__':
    main()
