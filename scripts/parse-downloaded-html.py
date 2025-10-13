#!/usr/bin/env python3
"""
Parse the downloaded HTML file to extract all 1432 NICU hospitals
"""

from bs4 import BeautifulSoup
import json
import re

html_file = '/Users/ruthellis/Downloads/00. ALCEA/NICUNEARBY/Database – NICU Data.html'

print("Reading HTML file...")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

print("Parsing HTML...")
soup = BeautifulSoup(html_content, 'html.parser')

nicus = []

# Try to find all the hospital data
# Look for patterns in the HTML that contain hospital info

# Method 1: Look for table rows
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 4:
            name = cells[0].get_text(strip=True)
            state = cells[1].get_text(strip=True)
            county = cells[2].get_text(strip=True) if len(cells) > 2 else ''
            level = cells[3].get_text(strip=True) if len(cells) > 3 else ''

            if name and state and name != 'Hospital Name':
                # Convert numeric level to "Level X"
                if level.isdigit():
                    level_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV'}
                    level = f"Level {level_map.get(level, level)}"
                elif level and not level.startswith('Level'):
                    level_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV'}
                    level = f"Level {level_map.get(level, level)}"

                nicus.append({
                    'name': name,
                    'state': state,
                    'county': county,
                    'nicuLevel': level,
                    'beds': None
                })

# Method 2: Look for divs with hospital data
if not nicus:
    print("No tables found, trying div extraction...")
    # Look for patterns like: hospital name, state, county, level
    text = soup.get_text()
    lines = text.split('\n')

    # Simple pattern matching
    for i, line in enumerate(lines):
        line = line.strip()
        if line and len(line) > 3:
            # Check if next few lines might be state, county, level
            if i + 3 < len(lines):
                potential_state = lines[i + 1].strip()
                potential_county = lines[i + 2].strip()
                potential_level = lines[i + 3].strip()

                # If potential_state is 2 letters and potential_level is a digit
                if len(potential_state) == 2 and potential_level.isdigit():
                    level_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV'}
                    level = f"Level {level_map.get(potential_level, potential_level)}"

                    nicus.append({
                        'name': line,
                        'state': potential_state,
                        'county': potential_county,
                        'nicuLevel': level,
                        'beds': None
                    })

# Remove duplicates
seen = set()
unique_nicus = []
for nicu in nicus:
    key = f"{nicu['name']}|{nicu['state']}"
    if key not in seen:
        seen.add(key)
        unique_nicus.append(nicu)

print(f"\nExtracted {len(unique_nicus)} hospitals")

if unique_nicus:
    # Save to file
    output = {
        'nicus': unique_nicus,
        'total': len(unique_nicus),
        'source': 'nicudata.com',
        'scraped_at': '2025-10-12'
    }

    with open('data/nicudata-hospitals.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Saved to data/nicudata-hospitals.json")

    # Show sample
    print("\nSample entries:")
    for nicu in unique_nicus[:10]:
        print(f"  - {nicu['name']} ({nicu['state']}, {nicu['county']}): {nicu['nicuLevel']}")

    # Show states
    states = {}
    for nicu in unique_nicus:
        state = nicu['state']
        states[state] = states.get(state, 0) + 1

    print(f"\nStates covered ({len(states)}):")
    for state in sorted(states.keys()):
        print(f"  {state}: {states[state]} hospitals")
else:
    print("\nNo hospitals extracted. The HTML might use a different structure.")
    print("Try opening the file and copying the visible table text instead.")
