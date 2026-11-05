#!/usr/bin/env python3
"""
Process and optimize Overture Maps building data for web display
"""

import json
from pathlib import Path
import geopandas as gpd
from shapely.geometry import shape
import numpy as np

print("🔄 Processing Overture Maps building data...")

input_file = Path("data/processed/uk_buildings_overture.geojson")
output_file = Path("frontend/public/data/uk_buildings.geojson")

if not input_file.exists():
    print(f"❌ Input file not found: {input_file}")
    exit(1)

# Read the GeoJSON
print(f"📖 Reading {input_file}...")
with open(input_file, 'r') as f:
    data = json.load(f)

print(f"   Buildings: {len(data['features']):,}")

# Simplify geometries and reduce precision
print("⚙️  Simplifying geometries...")

simplified_features = []
for i, feature in enumerate(data['features']):
    if i % 10000 == 0 and i > 0:
        print(f"   Processed {i:,}/{len(data['features']):,} buildings...")

    try:
        geom = shape(feature['geometry'])

        # Simplify geometry (tolerance in degrees, ~100m)
        simplified = geom.simplify(0.0001, preserve_topology=True)

        # Round coordinates to 5 decimal places (~1m precision)
        coords = list(simplified.exterior.coords)
        rounded_coords = [[round(x, 5), round(y, 5)] for x, y in coords]

        simplified_features.append({
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Polygon',
                'coordinates': [rounded_coords]
            }
        })
    except Exception as e:
        # Skip invalid geometries
        continue

print(f"✓ Simplified to {len(simplified_features):,} valid buildings")

# Create optimized GeoJSON
optimized_geojson = {
    'type': 'FeatureCollection',
    'features': simplified_features
}

# Save
output_file.parent.mkdir(parents=True, exist_ok=True)
print(f"💾 Saving to {output_file}...")

with open(output_file, 'w') as f:
    json.dump(optimized_geojson, f, separators=(',', ':'))

file_size_mb = output_file.stat().st_size / 1024 / 1024
print(f"\n✓ Complete!")
print(f"  Output: {output_file}")
print(f"  Size: {file_size_mb:.1f} MB")
print(f"  Buildings: {len(simplified_features):,}")

# Calculate reduction
input_size_mb = input_file.stat().st_size / 1024 / 1024
reduction = ((input_size_mb - file_size_mb) / input_size_mb) * 100
print(f"  Size reduction: {reduction:.1f}%")
