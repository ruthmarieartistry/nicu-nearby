#!/usr/bin/env python3
"""
Add hospitals from major states to expand coverage
"""

import json

# New Jersey hospitals
nj_hospitals = [
    {"name": "Newark Beth Israel Medical Center", "state": "New Jersey", "nicuLevel": "Level IV", "beds": 46},
    {"name": "Atlanticare Regional Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 22},
    {"name": "Capital Health Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 12},
    {"name": "Cooper University Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 25},
    {"name": "Englewood Hospital and Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": None},
    {"name": "Hackensack University Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 40},
    {"name": "Inspira Medical Center Vineland", "state": "New Jersey", "nicuLevel": "Level III", "beds": 20},
    {"name": "Jefferson Washington Township Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 14},
    {"name": "Jersey City Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 41},
    {"name": "Jersey Shore University Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 34},
    {"name": "Monmouth Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 29},
    {"name": "Morristown Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 34},
    {"name": "Overlook Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 15},
    {"name": "Robert Wood Johnson University Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 37},
    {"name": "Rutgers University Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 48},
    {"name": "Saint Barnabas Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 56},
    {"name": "St. Joseph Regional Medical Center", "state": "New Jersey", "nicuLevel": "Level III", "beds": 50},
    {"name": "St. Peters University Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 54},
    {"name": "The Valley Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 15},
    {"name": "Virtua Voorhees Hospital", "state": "New Jersey", "nicuLevel": "Level III", "beds": 46},
    {"name": "CentraState Medical Center", "state": "New Jersey", "nicuLevel": "Level II", "beds": None},
    {"name": "Chilton Medical Center", "state": "New Jersey", "nicuLevel": "Level II", "beds": 4},
    {"name": "Clara Maass Medical Center", "state": "New Jersey", "nicuLevel": "Level II", "beds": None},
    {"name": "Community Medical Center", "state": "New Jersey", "nicuLevel": "Level II", "beds": None},
    {"name": "Inspira Medical Center Mullica Hill", "state": "New Jersey", "nicuLevel": "Level II", "beds": 6},
    {"name": "Inspira Medical Center Woodbury", "state": "New Jersey", "nicuLevel": "Level II", "beds": 6},
    {"name": "JFK Medical Center", "state": "New Jersey", "nicuLevel": "Level II", "beds": 6},
    {"name": "Lourdes Medical Center", "state": "New Jersey", "nicuLevel": "Level II", "beds": None},
]

# Load existing database
with open('data/nicu-database.json', 'r') as f:
    data = json.load(f)

# Add New Jersey hospitals
print(f"Current total: {len(data['nicus'])} hospitals")
data['nicus'].extend(nj_hospitals)
print(f"Added {len(nj_hospitals)} New Jersey hospitals")

# Remove duplicates
seen = set()
unique_nicus = []
for nicu in data['nicus']:
    key = f"{nicu['name']}|{nicu['state']}"
    if key not in seen:
        seen.add(key)
        unique_nicus.append(nicu)

data['nicus'] = unique_nicus
data['total'] = len(unique_nicus)

# Save
with open('data/nicu-database.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"New total: {len(unique_nicus)} hospitals")
print(f"\nStates now covered:")
states = {}
for nicu in unique_nicus:
    states[nicu['state']] = states.get(nicu['state'], 0) + 1
for state in sorted(states.keys()):
    print(f"  {state}: {states[state]} hospitals")
