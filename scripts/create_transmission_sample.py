#!/usr/bin/env python3
"""
Create sample transmission lines connecting major UK cities/GSPs
"""

import json
from pathlib import Path

# Major UK transmission corridors (approximate)
transmission_lines = [
    # London - Birmingham - Manchester - Scotland corridor
    {
        "name": "England-Scotland Interconnector",
        "voltage": "400kV",
        "coordinates": [
            [-0.1276, 51.5074],  # London
            [-1.8904, 52.4862],  # Birmingham
            [-2.2426, 53.4808],  # Manchester
            [-2.9915, 54.4042],  # Lancaster
            [-3.1883, 55.9533],  # Glasgow
        ]
    },
    # East Coast corridor
    {
        "name": "East Coast Main",
        "voltage": "400kV",
        "coordinates": [
            [-0.1276, 51.5074],  # London
            [0.1278, 52.2053],   # Cambridge
            [0.7190, 52.6309],   # Norwich
            [-1.0813, 53.9581],  # York
            [-1.6178, 54.9783],  # Newcastle
        ]
    },
    # West Coast corridor
    {
        "name": "West Coast Main",
        "voltage": "400kV",
        "coordinates": [
            [-3.4360, 50.3755],  # Plymouth
            [-3.5339, 50.7236],  # Exeter
            [-2.5879, 51.4545],  # Bristol
            [-2.9915, 53.4084],  # Liverpool
            [-4.2576, 55.8642],  # Glasgow
        ]
    },
    # Midlands cross-link
    {
        "name": "Midlands Link",
        "voltage": "275kV",
        "coordinates": [
            [-1.8904, 52.4862],  # Birmingham
            [-1.4701, 52.9225],  # Derby
            [-1.5491, 53.8008],  # Leeds
        ]
    },
    # South Coast
    {
        "name": "South Coast Link",
        "voltage": "275kV",
        "coordinates": [
            [-0.1276, 51.5074],  # London
            [-0.5706, 50.8292],  # Brighton
            [-1.4043, 50.9097],  # Southampton
        ]
    },
    # Wales connections
    {
        "name": "Wales Link",
        "voltage": "400kV",
        "coordinates": [
            [-2.5879, 51.4545],  # Bristol
            [-3.1791, 51.4816],  # Cardiff
            [-4.0814, 53.1435],  # Aberystwyth
        ]
    },
]

# Convert to GeoJSON
features = []
for line in transmission_lines:
    features.append({
        'type': 'Feature',
        'properties': {
            'name': line['name'],
            'voltage': line['voltage']
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': line['coordinates']
        }
    })

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# Save
output_file = Path('frontend/public/data/transmission_lines.geojson')
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"✓ Created {len(features)} transmission line corridors")
print(f"  Saved to: {output_file}")
print(f"  File size: {output_file.stat().st_size / 1024:.1f} KB")
