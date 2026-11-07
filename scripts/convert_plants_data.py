#!/usr/bin/env python3
"""
Convert UK Energy Generation Map plants data to GeoJSON
Source: https://github.com/dan-osull/UK-Energy-Generation-Map
"""

import json
from pathlib import Path

INPUT_FILE = Path(__file__).parent.parent / "data" / "github_sources" / "UK-Energy-Generation-Map" / "data" / "plants.json"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "processed" / "uk-power-plants.geojson"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print("Converting UK power plants data to GeoJSON...")
print(f"Input: {INPUT_FILE}")

# Load the plants data
with open(INPUT_FILE, 'r') as f:
    plants_data = json.load(f)

print(f"Found {len(plants_data)} power plants")

# Convert to GeoJSON
# Format: [name, type, lat, lon, capacity_mw, ?, operator, ?, osm_id]
features = []

plant_types = {
    'nw': 'wind',
    'ow': 'offshore_wind',
    'h': 'hydro',
    'ng': 'natural_gas',
    'c': 'coal',
    'n': 'nuclear',
    's': 'solar',
    'b': 'biomass',
    'o': 'oil',
    'ps': 'pumped_storage'
}

for plant in plants_data:
    if len(plant) >= 5:
        name = plant[0]
        plant_type_code = plant[1] if len(plant) > 1 else 'unknown'
        lat = plant[2] if len(plant) > 2 else None
        lon = plant[3] if len(plant) > 3 else None
        capacity_mw = plant[4] if len(plant) > 4 else 0
        operator = plant[6] if len(plant) > 6 else ''
        osm_id = plant[8] if len(plant) > 8 else ''

        if lat is None or lon is None:
            continue

        plant_type = plant_types.get(plant_type_code, plant_type_code)

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            'properties': {
                'name': name,
                'plant_type': plant_type,
                'plant_type_code': plant_type_code,
                'capacity_mw': capacity_mw,
                'operator': operator,
                'osm_id': osm_id,
                'source': 'UK Energy Generation Map'
            }
        }
        features.append(feature)

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# Save to file
with open(OUTPUT_FILE, 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"\n✅ Converted {len(features)} power plants")
print(f"📁 Output: {OUTPUT_FILE}")

# Print type breakdown
from collections import Counter
type_counts = Counter(f['properties']['plant_type'] for f in features)
print(f"\nPower plant types:")
for plant_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    total_capacity = sum(f['properties']['capacity_mw'] or 0 for f in features if f['properties']['plant_type'] == plant_type)
    print(f"  {plant_type}: {count} plants, {total_capacity:.1f} MW")

print(f"\n✅ Ready to integrate into frontend")
