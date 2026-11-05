#!/usr/bin/env python3
"""
Transform GSP boundaries from British National Grid (EPSG:27700) to WGS84 (EPSG:4326)
"""

import json
from pyproj import Transformer

# Create transformer from British National Grid to WGS84
transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)

def transform_coordinates(coords, depth=0):
    """Recursively transform coordinates at any nesting level"""
    if depth == 0:  # We're at coordinate pair level
        # coords is [easting, northing]
        lon, lat = transformer.transform(coords[0], coords[1])
        return [lon, lat]
    else:
        # coords is a list of coordinate arrays
        return [transform_coordinates(c, depth - 1) for c in coords]

def transform_geometry(geometry):
    """Transform a GeoJSON geometry"""
    geom_type = geometry['type']
    coords = geometry['coordinates']

    if geom_type == 'Point':
        geometry['coordinates'] = transform_coordinates(coords, 0)
    elif geom_type == 'LineString':
        geometry['coordinates'] = transform_coordinates(coords, 1)
    elif geom_type == 'Polygon':
        geometry['coordinates'] = transform_coordinates(coords, 2)
    elif geom_type == 'MultiPolygon':
        geometry['coordinates'] = transform_coordinates(coords, 3)

    return geometry

# Read input file
input_file = 'frontend/public/data/gsp_boundaries.geojson'
output_file = 'frontend/public/data/gsp_boundaries_wgs84.geojson'

print(f"Reading {input_file}...")
with open(input_file, 'r') as f:
    data = json.load(f)

print(f"Transforming {len(data['features'])} features from EPSG:27700 to EPSG:4326...")

# Transform all features
for i, feature in enumerate(data['features']):
    if (i + 1) % 50 == 0:
        print(f"  Processed {i + 1} features...")
    feature['geometry'] = transform_geometry(feature['geometry'])

# Update CRS to WGS84
data['crs'] = {
    "type": "name",
    "properties": {
        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
    }
}

# Write output
print(f"Writing {output_file}...")
with open(output_file, 'w') as f:
    json.dump(data, f, separators=(',', ':'))

print("✅ Transformation complete!")
print(f"Sample coordinate check:")
first_coord = data['features'][0]['geometry']['coordinates'][0][0][0]
print(f"  First coordinate: {first_coord}")
print(f"  Expected: lon in [-8, 2], lat in [49, 61]")
