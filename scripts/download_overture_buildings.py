#!/usr/bin/env python3
"""
Download and process Overture Maps building data for the UK
"""

import duckdb
import json
from pathlib import Path

# UK bounding box: [min_lon, min_lat, max_lon, max_lat]
UK_BBOX = [-8.0, 49.5, 2.0, 61.0]

print("🌍 Downloading Overture Maps building data for UK...")
print(f"   Bounding box: {UK_BBOX}")

# Create output directory
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to DuckDB and query Overture Maps data
con = duckdb.connect()

# Install and load spatial extension
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute("INSTALL spatial; LOAD spatial;")

print("\n📥 Querying Overture Maps S3 bucket...")

# Query Overture Maps building data for UK
# Using the latest release (2024-11)
query = f"""
SELECT
    ST_AsText(geometry) as geometry,
    ST_GeometryType(geometry) as geom_type
FROM read_parquet('s3://overturemaps-us-west-2/release/2024-11-13.0/theme=buildings/type=building/*',
    filename=true,
    hive_partitioning=1)
WHERE bbox.xmin >= {UK_BBOX[0]}
  AND bbox.ymin >= {UK_BBOX[1]}
  AND bbox.xmax <= {UK_BBOX[2]}
  AND bbox.ymax <= {UK_BBOX[3]}
LIMIT 100000;
"""

print("⏳ Executing query (this may take several minutes)...")

try:
    result = con.execute(query).fetchall()

    print(f"\n✓ Retrieved {len(result):,} buildings")

    # Convert to GeoJSON
    print("\n🔄 Converting to GeoJSON...")

    features = []
    for row in result:
        wkt_geom = row[0]

        # Parse WKT to GeoJSON-style coordinates
        # This is a simplified parser - for production, use a proper library
        if wkt_geom.startswith('POLYGON'):
            # Extract coordinates from WKT
            coords_str = wkt_geom.replace('POLYGON ((', '').replace('))', '')
            coords = []
            for point in coords_str.split(', '):
                lon, lat = map(float, point.split())
                coords.append([round(lon, 5), round(lat, 5)])

            features.append({
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [coords]
                }
            })

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    # Save to file
    output_file = output_dir / 'uk_buildings_overture.geojson'
    with open(output_file, 'w') as f:
        json.dump(geojson, f, separators=(',', ':'))

    file_size_mb = output_file.stat().st_size / 1024 / 1024
    print(f"\n✓ Saved to {output_file}")
    print(f"  File size: {file_size_mb:.1f} MB")
    print(f"  Buildings: {len(features):,}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTrying alternative approach with overturemaps-py...")

    # Alternative: Use overturemaps Python package
    import subprocess
    result = subprocess.run([
        'overturemaps', 'download',
        '--bbox=' + ','.join(map(str, UK_BBOX)),
        '-f', 'geojson',
        '--type=building',
        '-o', str(output_dir / 'uk_buildings_overture.geojson')
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Download successful using overturemaps CLI")
    else:
        print(f"Error: {result.stderr}")

con.close()
