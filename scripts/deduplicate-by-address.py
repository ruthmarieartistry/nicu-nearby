#!/usr/bin/env python3
"""
Remove duplicate hospitals with the same address.
For each address, keep the hospital with the highest NICU level.
"""

import json
from collections import defaultdict

# Load database
with open('data/nicu-database.json', 'r') as f:
    db = json.load(f)

print(f'Starting with {len(db["nicus"])} hospitals\n')

# Group by formatted_address OR coordinates
by_location = defaultdict(list)

for nicu in db['nicus']:
    addr = nicu.get('formatted_address')
    lat = nicu.get('lat')
    lng = nicu.get('lng')

    # Use address if available, otherwise use coordinates
    if addr:
        key = f'addr:{addr}'
    elif lat and lng:
        # Round to 4 decimal places (~11 meters precision)
        key = f'coord:{round(lat, 4)},{round(lng, 4)}'
    else:
        # No location info at all
        key = f'no-location:{nicu.get("name", "unknown")}'

    by_location[key].append(nicu)

# Deduplicate
kept = []
removed = []

# Level ranking (higher is better)
level_rank = {
    'Level IV': 4,
    'Level III': 3,
    'Level II': 2,
    'Level I': 1,
}

for location_key, hospitals in by_location.items():
    if len(hospitals) == 1:
        # No duplicates, keep it
        kept.append(hospitals[0])
    else:
        # Multiple hospitals at same location - keep the one with highest level
        # Sort by level (highest first), then by name length (shorter first)
        sorted_hospitals = sorted(
            hospitals,
            key=lambda h: (
                -level_rank.get(h.get('nicuLevel', ''), 0),  # Higher level first
                len(h.get('name', ''))  # Shorter name first (likely parent hospital)
            )
        )

        # Keep the best one
        best = sorted_hospitals[0]
        kept.append(best)

        # Track what we're removing
        for h in sorted_hospitals[1:]:
            removed.append(h)
            location_info = location_key.split(':', 1)[1] if ':' in location_key else location_key
            print(f'Removing: {h["name"]} (Level {h.get("nicuLevel", "N/A")})')
            print(f'  Keeping: {best["name"]} (Level {best.get("nicuLevel", "N/A")})')
            print(f'  Location: {location_info}')
            print()

print(f'\n\nSummary:')
print(f'Started with: {len(db["nicus"])} hospitals')
print(f'Removed: {len(removed)} duplicates')
print(f'Remaining: {len(kept)} hospitals')

# Update database
db['nicus'] = kept
db['total'] = len(kept)

# Save
with open('data/nicu-database.json', 'w') as f:
    json.dump(db, f, indent=2)

print(f'\nDatabase updated!')
