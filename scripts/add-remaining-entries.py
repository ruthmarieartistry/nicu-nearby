#!/usr/bin/env python3
"""
Manually add the 17 problematic entries that couldn't be parsed automatically
"""

import json
from pathlib import Path

# Manually parsed entries from the problematic lines
manual_entries = [
    {
        "name": "Amita Health Alexian Brothers Medical Center Elk Grove Village",
        "state": "Illinois",
        "county": "Cook, DuPage",
        "nicuLevel": "Level II",
        "url": "https://nicudata.com/entry/amita-health-alexian-brothers-medical-center-elk-grove-village/",
        "beds": None
    },
    {
        "name": "Anderson Lucchetti Women's and Children's Center, Sutter medical center Sacramento",
        "state": "California",
        "county": "Sacramento",
        "nicuLevel": "Level IV",
        "url": "https://nicudata.com/entry/anderson-lucchetti-womens-and-childrens-center-sutter-medical-center-sacramento/",
        "beds": None
    },
    {
        "name": "Baylor Scott and White All Saints Medical Center - Fort Worth",
        "state": "Texas",
        "county": "Tarrant, Denton",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/baylor-scott-and-white-all-saints-medical-center-fort-worth/",
        "beds": None
    },
    {
        "name": "Baylor Scott and White - Centennial",
        "state": "Texas",
        "county": "Collin, Denton",
        "nicuLevel": "Level II",
        "url": "https://nicudata.com/entry/baylor-scott-and-white-centennial/",
        "beds": None
    },
    {
        "name": "Brigham and Women's Hospital",
        "state": "Massachusetts",  # Corrected from AL to MA
        "county": "Suffolk",
        "nicuLevel": None,  # No level in that line
        "url": "https://nicudata.com/entry/brigham-and-womens-hospital/",
        "beds": None
    },
    {
        "name": "Childrens Hospital, Greenville, Memorial Hospital (prisma)",
        "state": "South Carolina",
        "county": "Greenville",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/childrens-hospital-greenville-memorial-hospital-prisma/",
        "beds": None
    },
    {
        "name": "Cook Children's Medical Center",
        "state": "Texas",
        "county": "Tarrant, Denton, Parker, Wise, Johnson",
        "nicuLevel": "Level IV",
        "url": "https://nicudata.com/entry/cook-childrens-medical-center/",
        "beds": None
    },
    {
        "name": "El Camino Hospital, Los Gatos",
        "state": "California",
        "county": "Santa Clara",
        "nicuLevel": "Level II",
        "url": "https://nicudata.com/entry/el-camino-hospital-los-gatos/",
        "beds": None
    },
    {
        "name": "Hennepin Healthcare, Medical Center",
        "state": "Minnesota",
        "county": "Hennepin",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/hennepin-healthcare-medical-center/",
        "beds": None
    },
    {
        "name": "JPS Hospital (John Peter Smith)",
        "state": "Texas",
        "county": "Tarrant, Denton, Parker, Wise, Johnson",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/jps-hospital-john-peter-smith/",
        "beds": None
    },
    {
        "name": "Kent General Hospital - Bayhealth Hospital, Kent Campus",
        "state": "Delaware",
        "county": "Kent",
        "nicuLevel": "Level II",
        "url": "https://nicudata.com/entry/kent-general-hospital-bayhealth-hospital-kent-campus/",
        "beds": None
    },
    {
        "name": "Louisiana State University Health Sciences Center, Shreveport - LSU HSC-S (Ochsner LSU Health)",
        "state": "Louisiana",
        "county": "Caddo Parrish",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/louisiana-state-university-health-sciences-center-shreveport-lsu-hsc-s-ochsner-lsu-health/",
        "beds": None
    },
    {
        "name": "Medical City Alliance",
        "state": "Texas",
        "county": "Tarrant, Denton, Parker, Wise, Johnson",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/medical-city-alliance/",
        "beds": None
    },
    {
        "name": "Medical City Arlington",
        "state": "Texas",
        "county": "Tarrant, Denton, Parker, Wise, Johnson",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/medical-city-arlington/",
        "beds": None
    },
    {
        "name": "Medical City Frisco",
        "state": "Texas",
        "county": "Collin, Denton",
        "nicuLevel": "Level III",
        "url": "https://nicudata.com/entry/medical-city-frisco/",
        "beds": None
    },
    {
        "name": "Michigan Medicine, C.S. Mott Children's Hospital",
        "state": "Michigan",
        "county": "Washtenaw",
        "nicuLevel": "Level IV",
        "url": "https://nicudata.com/entry/michigan-medicine-c-s-mott-childrens-hospital/",
        "beds": None
    },
    {
        "name": "Monroe Carell, Jr. Children's Hospital at Vanderbilt",
        "state": "Tennessee",
        "county": "Davidson",
        "nicuLevel": "Level IV",
        "url": "https://nicudata.com/entry/monroe-carell-jr-childrens-hospital-at-vanderbilt/",
        "beds": None
    }
]

def main():
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / 'data' / 'nicu-database.json'

    # Load existing database
    with open(db_path, 'r', encoding='utf-8') as f:
        database = json.load(f)

    existing_nicus = database.get('nicus', [])

    # Create a set of existing entries for deduplication
    existing_keys = set()
    for nicu in existing_nicus:
        key = (nicu['name'].lower().strip(), nicu['state'].lower().strip())
        existing_keys.add(key)

    # Add new entries if they don't exist
    added = 0
    for entry in manual_entries:
        key = (entry['name'].lower().strip(), entry['state'].lower().strip())
        if key not in existing_keys:
            existing_nicus.append(entry)
            existing_keys.add(key)
            added += 1
            print(f"Added: {entry['name']} ({entry['state']})")
        else:
            print(f"Already exists: {entry['name']} ({entry['state']})")

    # Sort by state and name
    existing_nicus.sort(key=lambda x: (x['state'], x['name']))

    # Update database
    database['nicus'] = existing_nicus
    database['total'] = len(existing_nicus)

    # Save updated database
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    print(f"\nDatabase updated successfully!")
    print(f"Total entries: {database['total']}")
    print(f"New entries added: {added}")

if __name__ == '__main__':
    main()
