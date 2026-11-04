#!/usr/bin/env python3
"""
Convert TEC Register CSV to GeoJSON with geocoded points
"""

import pandas as pd
import json
from pathlib import Path
import re

DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("frontend/public/data")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_coordinates_from_name(site_name):
    """
    Extract rough coordinates based on connection site name
    Using UK major cities/regions as reference points
    This is a placeholder - in production, use proper geocoding API
    """

    # Rough coordinate mapping for UK regions/cities
    location_map = {
        # Scotland
        'aberdeen': (-2.094, 57.149),
        'dundee': (-2.970, 56.462),
        'glasgow': (-4.251, 55.860),
        'edinburgh': (-3.188, 55.953),
        'inverness': (-4.224, 57.477),

        # North England
        'newcastle': (-1.617, 54.978),
        'sunderland': (-1.382, 54.906),
        'middlesbrough': (-1.232, 54.574),
        'carlisle': (-2.933, 54.892),

        # Yorkshire
        'leeds': (-1.549, 53.801),
        'sheffield': (-1.470, 53.381),
        'hull': (-0.336, 53.745),
        'york': (-1.080, 53.958),

        # Northwest
        'manchester': (-2.244, 53.483),
        'liverpool': (-2.991, 53.408),
        'preston': (-2.707, 53.763),
        'blackpool': (-3.049, 53.817),

        # Midlands
        'birmingham': (-1.890, 52.486),
        'nottingham': (-1.150, 52.954),
        'leicester': (-1.131, 52.637),
        'coventry': (-1.508, 52.406),
        'derby': (-1.476, 52.922),

        # East
        'norwich': (1.297, 52.630),
        'ipswich': (1.156, 52.059),
        'cambridge': (0.121, 52.205),
        'peterborough': (-0.244, 52.573),

        # Wales
        'cardiff': (-3.179, 51.481),
        'swansea': (-3.943, 51.621),
        'newport': (-2.998, 51.588),
        'wrexham': (-2.993, 53.046),

        # Southwest
        'bristol': (-2.588, 51.454),
        'exeter': (-3.533, 50.725),
        'plymouth': (-4.142, 50.376),
        'swindon': (-1.781, 51.556),

        # Southeast
        'london': (-0.127, 51.507),
        'brighton': (-0.137, 50.822),
        'southampton': (-1.404, 50.909),
        'portsmouth': (-1.091, 50.805),
        'reading': (-0.973, 51.454),
        'oxford': (-1.258, 51.752),

        # Default UK center
        'default': (-2.5, 54.5)
    }

    site_lower = site_name.lower()

    # Try to find matching location
    for key, coords in location_map.items():
        if key in site_lower:
            return coords

    # Return UK center as fallback
    return location_map['default']

def convert_tec_to_geojson():
    """Convert TEC Register to GeoJSON"""
    print("Converting TEC Register to GeoJSON...")

    # Load TEC Register
    tec_file = list(DATA_DIR.glob("queue/tec_register*.csv"))[0]
    df = pd.read_csv(tec_file)

    print(f"Loaded {len(df)} projects")

    # Create GeoJSON features
    features = []

    for idx, row in df.iterrows():
        # Extract coordinates from connection site name
        coords = extract_coordinates_from_name(str(row.get('Connection Site', '')))

        # Determine plant type category
        plant_type = str(row.get('Plant Type', 'Other'))

        if 'Energy Storage' in plant_type:
            category = 'Storage'
            color = '#667eea'
        elif 'Wind Offshore' in plant_type:
            category = 'Wind Offshore'
            color = '#4d9de0'
        elif 'Wind Onshore' in plant_type or 'Wind' in plant_type:
            category = 'Wind Onshore'
            color = '#6bcf7f'
        elif 'Solar' in plant_type or 'PV' in plant_type:
            category = 'Solar'
            color = '#ffd93d'
        elif 'CCGT' in plant_type:
            category = 'Gas'
            color = '#e15554'
        else:
            category = 'Other'
            color = '#999999'

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [coords[0], coords[1]]
            },
            'properties': {
                'project_name': str(row.get('Project Name', 'Unknown')),
                'customer': str(row.get('Customer Name', 'Unknown')),
                'connection_site': str(row.get('Connection Site', 'Unknown')),
                'plant_type': plant_type,
                'category': category,
                'color': color,
                'capacity_mw': float(row.get('MW Connected', 0)),
                'status': str(row.get('Project Status', 'Unknown')),
                'stage': str(row.get('Stage', 'N/A')),
                'agreement_type': str(row.get('Agreement Type', 'Unknown'))
            }
        }

        features.append(feature)

    # Create GeoJSON
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    # Save
    output_file = OUTPUT_DIR / 'tec_register_points.geojson'
    with open(output_file, 'w') as f:
        json.dump(geojson, f)

    print(f"✓ Saved {len(features)} projects to {output_file}")

    # Statistics
    print(f"\nBreakdown by category:")
    categories = {}
    for feature in features:
        cat = feature['properties']['category']
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")

    return output_file

if __name__ == "__main__":
    convert_tec_to_geojson()
