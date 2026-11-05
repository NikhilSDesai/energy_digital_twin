#!/usr/bin/env python3
"""
Download real UK transmission lines from OpenStreetMap using overpy
"""

import json
from pathlib import Path
import subprocess
import sys

# Install overpy if needed
try:
    import overpy
except ImportError:
    print("Installing overpy...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "overpy"])
    import overpy

print("📡 Downloading REAL UK transmission network from OpenStreetMap...")

api = overpy.Overpass()

# Query for UK transmission lines (132kV, 275kV, 400kV)
# These are the actual high-voltage transmission lines
query = """
[out:json][timeout:180];
area["ISO3166-1"="GB"][admin_level=2]->.uk;
(
  way(area.uk)["power"="line"]["voltage"~"^(132000|275000|400000)"];
);
out geom;
"""

try:
    print("⏳ Querying OpenStreetMap (this may take 2-3 minutes)...")
    result = api.query(query)

    print(f"✓ Retrieved {len(result.ways)} transmission line segments")

    # Convert to GeoJSON
    features = []

    for way in result.ways:
        if len(way.nodes) < 2:
            continue

        coords = [[float(node.lon), float(node.lat)] for node in way.nodes]

        voltage = way.tags.get('voltage', 'unknown')
        name = way.tags.get('name', '')
        operator = way.tags.get('operator', '')

        features.append({
            'type': 'Feature',
            'properties': {
                'voltage': voltage,
                'name': name,
                'operator': operator,
                'voltage_kv': int(voltage) / 1000 if voltage.isdigit() else 0
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        })

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    # Save
    output_file = Path('frontend/public/data/transmission_lines.geojson')
    with open(output_file, 'w') as f:
        json.dump(geojson, f)

    size_mb = output_file.stat().st_size / 1024 / 1024
    print(f"\n✅ Success!")
    print(f"   File: {output_file}")
    print(f"   Lines: {len(features)}")
    print(f"   Size: {size_mb:.2f} MB")

    # Count by voltage
    voltages = {}
    for f in features:
        v = f['properties']['voltage']
        voltages[v] = voltages.get(v, 0) + 1

    print("\n   By voltage:")
    for v, count in sorted(voltages.items()):
        print(f"     {v}: {count} segments")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nNote: OpenStreetMap Overpass API can be slow/rate-limited.")
    print("If this fails repeatedly, we may need to use a different data source.")
