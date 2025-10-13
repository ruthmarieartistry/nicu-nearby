#!/usr/bin/env python3
"""
Manually add New York NICU data to the database
"""

import json

# New York NICU data manually extracted
ny_nicus = [
    # Level IV
    {"name": "Albany Medical Center", "state": "New York", "nicuLevel": "Level IV", "beds": 60},
    {"name": "Cohen Children's Medical Center", "state": "New York", "nicuLevel": "Level IV", "beds": 57},
    {"name": "Crouse Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 57},
    {"name": "Golisano Children's Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 68},
    {"name": "Montefiore Medical Center", "state": "New York", "nicuLevel": "Level IV", "beds": 35},
    {"name": "Mount Sinai Kravis Children's Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 46},
    {"name": "NewYork-Presbyterian Morgan Stanley Children's Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 62},
    {"name": "NewYork-Presbyterian Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 50},
    {"name": "NYU Winthrop Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 35},
    {"name": "Oishei Children's Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 64},
    {"name": "Stony Brook University Medical Center", "state": "New York", "nicuLevel": "Level IV", "beds": 46},
    {"name": "Tisch Hospital", "state": "New York", "nicuLevel": "Level IV", "beds": 54},
    {"name": "Westchester Medical Center", "state": "New York", "nicuLevel": "Level IV", "beds": 49},
    # Level III
    {"name": "Arnot Ogden Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 16},
    {"name": "Bellevue Hospital Center", "state": "New York", "nicuLevel": "Level III", "beds": 15},
    {"name": "BronxCare Hospital Center", "state": "New York", "nicuLevel": "Level III", "beds": 30},
    {"name": "The Brooklyn Hospital Center", "state": "New York", "nicuLevel": "Level III", "beds": 26},
    {"name": "Cayuga Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 12},
    {"name": "Highland Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 20},
    {"name": "Jacobi Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 33},
    {"name": "Jamaica Hospital Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 40},
    {"name": "Lincoln Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 32},
    {"name": "Maimonides Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 60},
    {"name": "Mount Sinai Beth Israel", "state": "New York", "nicuLevel": "Level III", "beds": 18},
    {"name": "Mount Sinai Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 24},
    {"name": "Mount Sinai West", "state": "New York", "nicuLevel": "Level III", "beds": 26},
    {"name": "NewYork-Presbyterian Brooklyn Methodist Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 48},
    {"name": "NewYork-Presbyterian Queens", "state": "New York", "nicuLevel": "Level III", "beds": 16},
    {"name": "North Shore University Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 51},
    {"name": "Northwell Health Plainview Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 20},
    {"name": "NYU Langone Hospital - Brooklyn", "state": "New York", "nicuLevel": "Level III", "beds": 24},
    {"name": "NYU Langone Hospital - Long Island", "state": "New York", "nicuLevel": "Level III", "beds": 27},
    {"name": "Richmond University Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 26},
    {"name": "Rochester General Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 28},
    {"name": "St. Joseph's Hospital Health Center", "state": "New York", "nicuLevel": "Level III", "beds": 18},
    {"name": "St. Luke's Cornwall Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 14},
    {"name": "St. Peter's Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 27},
    {"name": "Staten Island University Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 40},
    {"name": "Strong Memorial Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 22},
    {"name": "Upstate University Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 24},
    {"name": "Vassar Brothers Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 20},
    {"name": "White Plains Hospital", "state": "New York", "nicuLevel": "Level III", "beds": 24},
    {"name": "Wyckoff Heights Medical Center", "state": "New York", "nicuLevel": "Level III", "beds": 24},
    # Level II
    {"name": "Coney Island Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 15},
    {"name": "Ellis Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 15},
    {"name": "Good Samaritan Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 17},
    {"name": "Gouverneur Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 6},
    {"name": "Kings County Hospital Center", "state": "New York", "nicuLevel": "Level II", "beds": 16},
    {"name": "Lenox Hill Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 16},
    {"name": "Long Island Jewish Medical Center", "state": "New York", "nicuLevel": "Level II", "beds": 20},
    {"name": "Lutheran Medical Center", "state": "New York", "nicuLevel": "Level II", "beds": 16},
    {"name": "Mercy Hospital of Buffalo", "state": "New York", "nicuLevel": "Level II", "beds": 16},
    {"name": "New York Downtown Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 10},
    {"name": "Newark Wayne Community Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 10},
    {"name": "Queens Hospital Center", "state": "New York", "nicuLevel": "Level II", "beds": 20},
    {"name": "Samaritan Medical Center", "state": "New York", "nicuLevel": "Level II", "beds": 10},
    {"name": "Sisters of Charity Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 10},
    {"name": "South Nassau Communities Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 20},
    {"name": "Southside Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 14},
    {"name": "St. Barnabas Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 18},
    {"name": "St. John's Episcopal Hospital", "state": "New York", "nicuLevel": "Level II", "beds": 12},
    {"name": "The Unity Hospital of Rochester", "state": "New York", "nicuLevel": "Level II", "beds": 14},
    {"name": "Woodhull Medical Center", "state": "New York", "nicuLevel": "Level II", "beds": 20},
]

# Load existing database
with open('data/nicu-database.json', 'r') as f:
    data = json.load(f)

# Add New York hospitals
data['nicus'].extend(ny_nicus)
data['total'] = len(data['nicus'])

# Save updated database
with open('data/nicu-database.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added {len(ny_nicus)} New York NICUs to the database")
print(f"Total NICUs now: {data['total']}")
