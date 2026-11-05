#!/usr/bin/env python3
"""
Download UK transmission lines from OpenStreetMap
"""

import requests
import json
from pathlib import Path

print("📡 Downloading UK transmission lines from OpenStreetMap...")

# Overpass API query for power lines in UK
# Voltage >= 220kV (transmission level)
query = """
[out:json][timeout:180];
area["ISO3166-1"="GB"][admin_level=2];
(
  way(area)["power"="line"]["voltage"~"^(220000|275000|400000|132000)"];
);
out geom;
"""

url = "https://overpass-api.de/api/interpreter"

try:
    print("⏳ Querying Overpass API (this may take 1-2 minutes)...")
    response = requests.post(url, data={'data': query}, timeout=300)
    response.raise_for_status()

    data = response.json()
    print(f"✓ Retrieved {len(data.get('elements', []))} transmission line segments")

    # Convert to GeoJSON
    features = []
    for element in data.get('elements', []):
        if element['type'] == 'way' and 'geometry' in element:
            coords = [[node['lon'], node['lat']] for node in element['geometry']]

            features.append({
                'type': 'Feature',
                'properties': {
                    'voltage': element.get('tags', {}).get('voltage', 'unknown'),
                    'name': element.get('tags', {}).get('name', ''),
                    'operator': element.get('tags', {}).get('operator', '')
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
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(geojson, f)

    size_mb = output_file.stat().st_size / 1024 / 1024
    print(f"\n✓ Saved to {output_file}")
    print(f"  Features: {len(features)}")
    print(f"  File size: {size_mb:.2f} MB")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTrying smaller query...")

    # Fallback: smaller area (England only)
    query_small = """
    [out:json][timeout:120];
    area["name"="England"][admin_level=4];
    (
      way(area)["power"="line"]["voltage"~"^(400000|275000)"];
    );
    out geom;
    """

    try:
        response = requests.post(url, data={'data': query_small}, timeout=180)
        response.raise_for_status()
        data = response.json()

        # Process same as above
        features = []
        for element in data.get('elements', []):
            if element['type'] == 'way' and 'geometry' in element:
                coords = [[node['lon'], node['lat']] for node in element['geometry']]
                features.append({
                    'type': 'Feature',
                    'properties': {
                        'voltage': element.get('tags', {}).get('voltage', 'unknown')
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

        output_file = Path('frontend/public/data/transmission_lines.geojson')
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(geojson, f)

        print(f"✓ Saved {len(features)} transmission lines")

    except Exception as e2:
        print(f"❌ Fallback also failed: {e2}")
