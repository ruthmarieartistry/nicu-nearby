#!/usr/bin/env python3
"""
Scrape NICU data from neonatologysolutions.com for all US states
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time

# List of all states with their URLs
STATES = {
    'Alabama': 'https://neonatologysolutions.com/alabama-nicus/',
    'Alaska': 'https://neonatologysolutions.com/alaska-nicus/',
    'Arizona': 'https://neonatologysolutions.com/arizona-nicus/',
    'Arkansas': 'https://neonatologysolutions.com/arkansas-nicus/',
    'California': 'https://neonatologysolutions.com/california-nicus/',
    'Colorado': 'https://neonatologysolutions.com/colorado-nicus/',
    'Connecticut': 'https://neonatologysolutions.com/connecticut-nicus/',
    'Delaware': 'https://neonatologysolutions.com/deleware-nicus/',
    'District of Columbia': 'https://neonatologysolutions.com/district-of-columbia-nicus/',
    'Florida': 'https://neonatologysolutions.com/florida-nicus/',
    'Georgia': 'https://neonatologysolutions.com/georgia-nicus/',
    'Hawaii': 'https://neonatologysolutions.com/hawaii-nicus/',
    'Idaho': 'https://neonatologysolutions.com/idaho-nicus/',
    'Illinois': 'https://neonatologysolutions.com/illinois-nicus/',
    'Indiana': 'https://neonatologysolutions.com/indiana-nicus/',
    'Iowa': 'https://neonatologysolutions.com/iowa-nicus/',
    'Kansas': 'https://neonatologysolutions.com/kansas-nicus/',
    'Kentucky': 'https://neonatologysolutions.com/kentucky-nicus/',
    'Louisiana': 'https://neonatologysolutions.com/louisiana-nicus/',
    'Maine': 'https://neonatologysolutions.com/maine-nicus/',
    'Maryland': 'https://neonatologysolutions.com/maryland-nicus/',
    'Massachusetts': 'https://neonatologysolutions.com/massachusetts-nicus/',
    'Michigan': 'https://neonatologysolutions.com/michigan-nicus/',
    'Minnesota': 'https://neonatologysolutions.com/minnesota-nicus/',
    'Mississippi': 'https://neonatologysolutions.com/mississippi-nicus/',
    'Missouri': 'https://neonatologysolutions.com/missouri-nicus/',
    'Montana': 'https://neonatologysolutions.com/montana-nicus/',
    'Nebraska': 'https://neonatologysolutions.com/nebraska/',
    'Nevada': 'https://neonatologysolutions.com/nevada-nicus/',
    'New Hampshire': 'https://neonatologysolutions.com/new-hampshire-nicus/',
    'New Jersey': 'https://neonatologysolutions.com/new-jersey-nicus/',
    'New Mexico': 'https://neonatologysolutions.com/new-mexico-nicus/',
    'New York': 'https://neonatologysolutions.com/new-york-nicus/',
    'North Carolina': 'https://neonatologysolutions.com/north-carolina-nicus/',
    'North Dakota': 'https://neonatologysolutions.com/north-dakota/',
    'Ohio': 'https://neonatologysolutions.com/ohio/',
    'Oklahoma': 'https://neonatologysolutions.com/oklahoma-nicus/',
    'Oregon': 'https://neonatologysolutions.com/oregon-nicus/',
    'Pennsylvania': 'https://neonatologysolutions.com/pennsylvania-nicus/',
    'Rhode Island': 'https://neonatologysolutions.com/rhode-island-nicus/',
    'South Carolina': 'https://neonatologysolutions.com/south-carolina-nicus/',
    'South Dakota': 'https://neonatologysolutions.com/south-dakota-nicus/',
    'Tennessee': 'https://neonatologysolutions.com/tennessee-nicus/',
    'Texas': 'https://neonatologysolutions.com/texas-nicus/',
    'Utah': 'https://neonatologysolutions.com/utah-nicus/',
    'Vermont': 'https://neonatologysolutions.com/vermont-nicus/',
    'Virginia': 'https://neonatologysolutions.com/virginia-nicus/',
    'Washington': 'https://neonatologysolutions.com/washington-nicus/',
    'West Virginia': 'https://neonatologysolutions.com/west-virginia-nicus/',
    'Wisconsin': 'https://neonatologysolutions.com/wisconsin-nicus/',
    'Wyoming': 'https://neonatologysolutions.com/wyoming-nicus/',
}

def scrape_state_nicus(state_name, url):
    """Scrape NICU data for a single state"""
    print(f"Scraping {state_name}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        nicus = []

        # Find all hospital entries - they typically are in a specific format
        # Look for hospital names (usually in <strong> or <h3> tags followed by Level and Beds info)
        content = soup.find('div', class_='entry-content') or soup.find('article')

        if not content:
            print(f"  Warning: Could not find content for {state_name}")
            return nicus

        # Get all text and parse it
        text = content.get_text()

        # Pattern to match: Hospital Name followed by Level and Beds
        # Example: "Children's Hospital of Michigan\nLevel IV | 40 Beds"
        lines = text.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for lines that might be hospital names (not empty, not metadata)
            if line and not line.startswith('NICU Level') and not line.startswith('Practice Type'):
                # Check if next line contains Level and Beds info
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    level_match = re.search(r'Level\s+(II|III|IV|I)\s*\|?\s*(\d+)\s*Beds?', next_line, re.IGNORECASE)

                    if level_match:
                        hospital_name = line
                        level = level_match.group(1).upper()
                        beds = int(level_match.group(2))

                        nicus.append({
                            'name': hospital_name,
                            'state': state_name,
                            'nicuLevel': f'Level {level}',
                            'beds': beds
                        })

                        i += 2  # Skip the next line since we've processed it
                        continue

            i += 1

        print(f"  Found {len(nicus)} NICUs in {state_name}")
        return nicus

    except requests.RequestException as e:
        print(f"  Error scraping {state_name}: {e}")
        return []
    except Exception as e:
        print(f"  Unexpected error for {state_name}: {e}")
        return []

def main():
    """Main scraping function"""
    all_nicus = []

    for state_name, url in STATES.items():
        nicus = scrape_state_nicus(state_name, url)
        all_nicus.extend(nicus)

        # Be polite - wait between requests
        time.sleep(1)

    # Save to JSON file
    output_file = 'data/nicu-database.json'

    with open(output_file, 'w') as f:
        json.dump({
            'nicus': all_nicus,
            'total': len(all_nicus),
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2)

    print(f"\n{'='*50}")
    print(f"Scraping complete!")
    print(f"Total NICUs found: {len(all_nicus)}")
    print(f"Data saved to: {output_file}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
