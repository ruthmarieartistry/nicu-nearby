#!/usr/bin/env python3
"""
Import NICU data from CSV to the nicu-database.json format
"""

import json
import re
from pathlib import Path

def parse_nicu_level(level_str):
    """Convert numeric level (1-4) to Level I-IV format"""
    level_map = {
        '1': 'Level I',
        '2': 'Level II',
        '3': 'Level III',
        '4': 'Level IV'
    }
    return level_map.get(str(level_str).strip(), None)

def get_state_full_name(abbrev):
    """Convert state abbreviation to full name"""
    states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }
    return states.get(abbrev.upper().strip(), abbrev)

def parse_csv_line(line):
    """Parse a line from the CSV file"""
    line = line.strip()

    # Remove BOM if present
    line = line.replace('\ufeff', '')

    if not line:
        return None

    # Extract URL first - it's always at the end in the format: View (URL)
    url_pattern = r'View\s+\((https?://[^\)]+)\)\s*$'
    url_match = re.search(url_pattern, line)
    if not url_match:
        return None

    url = url_match.group(1)
    # Remove the "View (URL)" part
    line_without_url = line[:url_match.start()].strip()

    # Extract NICU level - it's a single digit at the end
    level_pattern = r'\s+(\d)\s*$'
    level_match = re.search(level_pattern, line_without_url)
    if not level_match:
        return None

    level = level_match.group(1)
    # Remove the level
    line_without_level = line_without_url[:level_match.start()].strip()

    # Valid US state abbreviations
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
    }

    # If line starts with quotes, extract the name from quotes
    if line_without_level.startswith('"'):
        # Pattern 1: "Hospital Name" STATE County
        quote_match = re.match(r'"([^"]+)"\s+([A-Z]{2})\s+(.+)$', line_without_level)
        if quote_match and quote_match.group(2) in valid_states:
            name = quote_match.group(1).strip()
            state = quote_match.group(2)
            county = quote_match.group(3).strip()
            return {
                'name': name,
                'state': get_state_full_name(state),
                'county': county,
                'nicuLevel': parse_nicu_level(level),
                'url': url,
                'beds': None
            }

        # Pattern 2: "Hospital Name STATE County" (state is inside quotes)
        # Extract everything in quotes, then find the last STATE abbrev in it
        quote_match2 = re.match(r'"(.+)"$', line_without_level)
        if quote_match2:
            quoted_content = quote_match2.group(1)
            parts = quoted_content.split()

            # Find the last valid state abbreviation
            state_idx = -1
            state = None
            for i in range(len(parts) - 1, -1, -1):
                if parts[i] in valid_states:
                    state_idx = i
                    state = parts[i]
                    break

            if state_idx != -1:
                name = ' '.join(parts[:state_idx]).strip()
                county = ' '.join(parts[state_idx + 1:]).strip()
                if name:
                    return {
                        'name': name,
                        'state': get_state_full_name(state),
                        'county': county if county else 'Unknown',
                        'nicuLevel': parse_nicu_level(level),
                        'url': url,
                        'beds': None
                    }

    # Find the LAST valid state abbreviation (in case hospital name contains state-like abbreviations)
    # Split by spaces and work backwards
    parts = line_without_level.split()
    state_idx = -1
    state = None

    for i in range(len(parts) - 1, -1, -1):
        if parts[i] in valid_states:
            state_idx = i
            state = parts[i]
            break

    if state_idx == -1:
        return None

    # Everything before the state is the hospital name
    name = ' '.join(parts[:state_idx]).strip()
    # Everything after the state is the county
    county = ' '.join(parts[state_idx + 1:]).strip()

    if not name:
        return None

    return {
        'name': name,
        'state': get_state_full_name(state),
        'county': county if county else 'Unknown',
        'nicuLevel': parse_nicu_level(level),
        'url': url,
        'beds': None
    }

def load_existing_database(db_path):
    """Load existing NICU database"""
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'nicus': [], 'total': 0}

def main():
    # Paths
    base_dir = Path(__file__).parent.parent
    csv_path = base_dir / 'data' / 'FINALNicus.csv'
    db_path = base_dir / 'data' / 'nicu-database.json'

    print(f"Reading CSV from: {csv_path}")
    print(f"Database path: {db_path}")

    # Load existing database
    database = load_existing_database(db_path)
    existing_nicus = database.get('nicus', [])

    print(f"Existing database has {len(existing_nicus)} entries")

    # Create a set of existing entries for deduplication
    existing_keys = set()
    for nicu in existing_nicus:
        key = (nicu['name'].lower().strip(), nicu['state'].lower().strip())
        existing_keys.add(key)

    # Parse CSV and add new entries
    new_entries = []
    duplicates = 0
    errors = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            entry = parse_csv_line(line)
            if entry:
                key = (entry['name'].lower().strip(), entry['state'].lower().strip())

                if key not in existing_keys:
                    new_entries.append(entry)
                    existing_keys.add(key)
                else:
                    duplicates += 1
            else:
                print(f"Warning: Could not parse line {line_num}: {line[:80]}...")
                errors += 1

    print(f"\nParsed {len(new_entries)} new entries")
    print(f"Found {duplicates} duplicates (skipped)")
    print(f"Errors: {errors}")

    # Merge and sort
    all_nicus = existing_nicus + new_entries
    all_nicus.sort(key=lambda x: (x['state'], x['name']))

    # Update database
    database['nicus'] = all_nicus
    database['total'] = len(all_nicus)

    # Save updated database
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    print(f"\nDatabase updated successfully!")
    print(f"Total entries: {database['total']}")
    print(f"New entries added: {len(new_entries)}")

    # Show sample of new entries
    if new_entries:
        print("\nSample of new entries:")
        for entry in new_entries[:5]:
            print(f"  - {entry['name']} ({entry['state']}) - {entry['nicuLevel']}")

if __name__ == '__main__':
    main()
