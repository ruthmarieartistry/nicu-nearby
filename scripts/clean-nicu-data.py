#!/usr/bin/env python3
"""
Clean the NICU database to remove metadata from hospital names
"""

import json
import re

# Load the database
with open('data/nicu-database.json', 'r') as f:
    data = json.load(f)

cleaned_nicus = []

for nicu in data['nicus']:
    # Extract clean hospital name (everything before "NICU Level" or similar markers)
    name = nicu['name']

    # Remove everything after markers like "NICU Level", "Practice Type", etc.
    clean_name = re.split(r'\s+(NICU Level|Practice Type|MD Contact|\|)', name)[0].strip()

    # Also try to extract the level and beds if they're in the name
    level_match = re.search(r'Level\s+(IV|III|II|I)', name, re.IGNORECASE)
    beds_match = re.search(r'(\d+)\s*Beds?', name, re.IGNORECASE)

    nicu_level = nicu.get('nicuLevel')
    beds = nicu.get('beds')

    # If level/beds are in the name but not in the fields, extract them
    if level_match and not nicu_level:
        level = level_match.group(1).upper()
        nicu_level = f'Level {level}'

    if beds_match and not beds:
        beds = int(beds_match.group(1))

    cleaned_nicus.append({
        'name': clean_name,
        'state': nicu['state'],
        'nicuLevel': nicu_level,
        'beds': beds
    })

# Save cleaned data
cleaned_data = {
    'nicus': cleaned_nicus,
    'total': len(cleaned_nicus),
    'scraped_at': data.get('scraped_at'),
    'cleaned_at': '2025-10-12'
}

with open('data/nicu-database.json', 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Cleaned {len(cleaned_nicus)} NICU entries")
print("\nSample cleaned entries:")
for nicu in cleaned_nicus[:5]:
    print(f"  - {nicu['name']} ({nicu['state']}): {nicu['nicuLevel']}, {nicu['beds']} beds")
