#!/usr/bin/env python3
"""
Simplify GeoJSON files for web deployment
"""

import json
from pathlib import Path

def simplify_gsp_boundaries():
    """Simplify GSP boundaries by reducing coordinate precision"""

    input_file = Path("frontend/public/data/gsp_boundaries.geojson")

    with open(input_file, 'r') as f:
        data = json.load(f)

    # Reduce coordinate precision to 4 decimal places (~11m accuracy)
    def round_coords(coords):
        if isinstance(coords[0], list):
            return [round_coords(c) for c in coords]
        else:
            return [round(c, 4) for c in coords]

    for feature in data['features']:
        if feature['geometry']['type'] == 'Polygon':
            feature['geometry']['coordinates'] = round_coords(feature['geometry']['coordinates'])
        elif feature['geometry']['type'] == 'MultiPolygon':
            feature['geometry']['coordinates'] = round_coords(feature['geometry']['coordinates'])

    # Save simplified version
    with open(input_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))

    print(f"✓ Simplified {input_file}")
    print(f"  New size: {input_file.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    simplify_gsp_boundaries()
