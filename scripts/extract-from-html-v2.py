#!/usr/bin/env python3
"""
Extract hospital data from downloaded HTML - Version 2
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

# Find all h2 tags with hospital names
hospital_titles = soup.find_all('h2', class_='elementor-heading-title')
print(f"Found {len(hospital_titles)} hospital title elements")

# Also find all the data rows
# Pattern: h2 with hospital name, followed by divs with state, county, level
for i, title_elem in enumerate(hospital_titles):
    hospital_name = title_elem.get_text(strip=True)

    # Try to find associated data
    # Look in the parent and sibling elements for state, county, level info
    parent = title_elem.find_parent()

    # Search for state (2-letter abbreviation)
    state = None
    county = None
    level = None

    # Search siblings and nearby elements
    current = title_elem
    for _ in range(20):  # Check next 20 elements
        current = current.find_next()
        if not current:
            break

        text = current.get_text(strip=True)

        # State (2 capital letters)
        if not state and len(text) == 2 and text.isupper() and text.isalpha():
            state = text

        # Level (single digit 1-4)
        if not level and text.isdigit() and text in ['1', '2', '3', '4']:
            level_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV'}
            level = f"Level {level_map[text]}"

        # County (any text that's not too short or long)
        if state and not county and not level:
            if 3 < len(text) < 50 and not text.isdigit():
                county = text

        if state and level:
            break

    if hospital_name and state:
        nicus.append({
            'name': hospital_name,
            'state': state,
            'county': county or '',
            'nicuLevel': level or '',
            'beds': None
        })

print(f"\nExtracted {len(nicus)} hospitals")

if nicus:
    # Save to file
    output = {
        'nicus': nicus,
        'total': len(nicus),
        'source': 'nicudata.com',
        'scraped_at': '2025-10-12'
    }

    with open('data/nicudata-hospitals.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Saved to data/nicudata-hospitals.json")

    # Show sample
    print("\nFirst 20 entries:")
    for nicu in nicus[:20]:
        print(f"  - {nicu['name']} ({nicu['state']}, {nicu['county']}): {nicu['nicuLevel']}")

    # Show states
    states = {}
    for nicu in nicus:
        state = nicu['state']
        states[state] = states.get(state, 0) + 1

    print(f"\nStates covered ({len(states)}):")
    for state in sorted(states.keys()):
        print(f"  {state}: {states[state]} hospitals")
else:
    print("\nNo hospitals extracted.")
