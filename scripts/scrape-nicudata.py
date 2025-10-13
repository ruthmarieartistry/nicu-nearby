#!/usr/bin/env python3
"""
Scrape NICU data from nicudata.com
This site has 1432+ NICU entries with levels and bed counts
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time

def scrape_nicudata():
    """Scrape NICU data from nicudata.com"""
    print("Scraping nicudata.com...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    url = 'https://nicudata.com/entry/'

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        nicus = []

        # Look for table rows or data entries
        # Try to find the data table
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")

        for table in tables:
            rows = table.find_all('tr')
            print(f"  Found {len(rows)} rows in table")

            for row in rows[1:]:  # Skip header row
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:
                    hospital_name = cells[0].get_text().strip()
                    state = cells[1].get_text().strip()
                    county = cells[2].get_text().strip() if len(cells) > 2 else ''
                    nicu_level = cells[3].get_text().strip() if len(cells) > 3 else ''

                    # Convert numeric level to "Level X" format
                    if nicu_level.isdigit():
                        level_map = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV'}
                        nicu_level = f"Level {level_map.get(nicu_level, nicu_level)}"

                    if hospital_name and state:
                        nicus.append({
                            'name': hospital_name,
                            'state': state,
                            'county': county,
                            'nicuLevel': nicu_level,
                            'beds': None  # May need to fetch individual pages for bed count
                        })

        # Alternative: Look for divs/lists with hospital data
        if not nicus:
            print("  No table found, trying alternative parsing...")
            # Try to find data in divs or other structures
            entries = soup.find_all(['div', 'li'], class_=re.compile(r'(hospital|entry|row|item)', re.I))
            print(f"  Found {len(entries)} potential entries")

        print(f"\nTotal NICUs scraped: {len(nicus)}")
        return nicus

    except Exception as e:
        print(f"Error scraping nicudata.com: {e}")
        return []

def main():
    """Main function"""
    nicus = scrape_nicudata()

    if nicus:
        # Save to temporary file
        output_file = 'data/nicudata-raw.json'

        with open(output_file, 'w') as f:
            json.dump({
                'nicus': nicus,
                'total': len(nicus),
                'source': 'nicudata.com',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)

        print(f"\nData saved to: {output_file}")

        # Show sample
        if nicus:
            print("\nSample entries:")
            for nicu in nicus[:10]:
                print(f"  - {nicu['name']} ({nicu['state']}): {nicu['nicuLevel']}")
    else:
        print("\nNo data scraped. The website may use JavaScript to load data dynamically.")
        print("Consider using Selenium or checking the page's API endpoints.")

if __name__ == '__main__':
    main()
