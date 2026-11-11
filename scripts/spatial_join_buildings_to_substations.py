#!/usr/bin/env python3
"""
Spatial Join: Buildings to LV Substations

Assigns each building to its nearest LV (11kV/400V) substation using spatial join.
This enables analysis of which buildings are served by which substations.

Data Requirements:
1. LV Substations: NGED 11kV transformers (download from connecteddata.nationalgrid.co.uk)
2. Buildings: UK building footprints (29.5M from Overture Maps)

Output:
- building_substation_mapping.geojson: Buildings with nearest substation ID
- substation_building_counts.csv: Count of buildings per substation
- analysis_report.json: Statistics and analysis results
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from scipy.spatial import cKDTree
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import sys

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROCESSED_DIR / "spatial_analysis"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_substations(filepath):
    """
    Load LV substation data from various formats.

    Args:
        filepath: Path to substation data (shapefile, geojson, gpkg)

    Returns:
        GeoDataFrame with substations in EPSG:4326
    """
    print(f"Loading substations from {filepath}...")

    try:
        substations = gpd.read_file(filepath)

        # Convert to WGS84 if needed
        if substations.crs != "EPSG:4326":
            print(f"  Converting from {substations.crs} to EPSG:4326...")
            substations = substations.to_crs("EPSG:4326")

        # Ensure we have point geometries
        if not all(substations.geometry.type == 'Point'):
            print("  Warning: Some substations are not points. Using centroids.")
            substations.geometry = substations.geometry.centroid

        print(f"  Loaded {len(substations):,} substations")
        return substations

    except Exception as e:
        print(f"ERROR loading substations: {e}")
        return None


def load_buildings_sample(filepath, sample_size=10000):
    """
    Load a sample of buildings for testing.
    For full run, use load_buildings_full().

    Args:
        filepath: Path to building data
        sample_size: Number of buildings to sample

    Returns:
        GeoDataFrame with building sample
    """
    print(f"Loading sample of {sample_size:,} buildings from {filepath}...")

    try:
        # Read first N features
        buildings = gpd.read_file(filepath, rows=sample_size)

        # Convert to WGS84 if needed
        if buildings.crs != "EPSG:4326":
            print(f"  Converting from {buildings.crs} to EPSG:4326...")
            buildings = buildings.to_crs("EPSG:4326")

        # Use centroids for point-based spatial join
        print("  Computing building centroids...")
        buildings['geometry'] = buildings.geometry.centroid

        print(f"  Loaded {len(buildings):,} building centroids")
        return buildings

    except Exception as e:
        print(f"ERROR loading buildings: {e}")
        return None


def nearest_neighbor_join(buildings, substations, max_distance_km=5.0):
    """
    Assign each building to its nearest substation using KDTree.

    Args:
        buildings: GeoDataFrame of buildings (points)
        substations: GeoDataFrame of substations (points)
        max_distance_km: Maximum distance to consider (km)

    Returns:
        buildings GeoDataFrame with substation_id and distance columns
    """
    print("\nPerforming spatial join (nearest neighbor)...")
    print(f"  Buildings: {len(buildings):,}")
    print(f"  Substations: {len(substations):,}")
    print(f"  Max distance: {max_distance_km} km")

    # Extract coordinates
    building_coords = np.array(list(zip(buildings.geometry.x, buildings.geometry.y)))
    substation_coords = np.array(list(zip(substations.geometry.x, substations.geometry.y)))

    # Build KDTree for fast nearest neighbor search
    print("  Building spatial index (KDTree)...")
    tree = cKDTree(substation_coords)

    # Query nearest neighbor for each building
    print("  Finding nearest substation for each building...")
    distances, indices = tree.query(building_coords, k=1)

    # Convert distances from degrees to approximate km
    # At UK latitude (~54°), 1 degree ≈ 111 km longitude, 69 km latitude
    # Use average for rough estimate
    distances_km = distances * 90  # Rough approximation

    # Add substation info to buildings
    buildings['nearest_substation_idx'] = indices
    buildings['distance_km'] = distances_km

    # Filter by max distance
    within_range = distances_km <= max_distance_km
    buildings['within_range'] = within_range

    print(f"\nResults:")
    print(f"  Buildings within {max_distance_km}km of substation: {within_range.sum():,} ({100*within_range.mean():.1f}%)")
    print(f"  Buildings beyond range: {(~within_range).sum():,}")
    print(f"  Mean distance: {distances_km[within_range].mean():.2f} km")
    print(f"  Median distance: {np.median(distances_km[within_range]):.2f} km")
    print(f"  Max distance (within range): {distances_km[within_range].max():.2f} km")

    # Add substation ID/name if available
    if 'id' in substations.columns:
        buildings['substation_id'] = substations.iloc[indices]['id'].values
    elif 'name' in substations.columns:
        buildings['substation_id'] = substations.iloc[indices]['name'].values
    elif 'OBJECTID' in substations.columns:
        buildings['substation_id'] = substations.iloc[indices]['OBJECTID'].values
    else:
        buildings['substation_id'] = indices  # Use index as ID

    return buildings


def analyze_results(buildings, substations):
    """
    Generate analysis statistics from spatial join.

    Args:
        buildings: GeoDataFrame with joined data
        substations: GeoDataFrame of substations

    Returns:
        dict with analysis results
    """
    print("\nAnalyzing results...")

    # Buildings per substation
    buildings_per_sub = buildings[buildings['within_range']].groupby('substation_id').size()

    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_buildings': len(buildings),
        'total_substations': len(substations),
        'buildings_matched': int(buildings['within_range'].sum()),
        'buildings_unmatched': int((~buildings['within_range']).sum()),
        'match_rate': float(buildings['within_range'].mean()),
        'distance_stats': {
            'mean_km': float(buildings[buildings['within_range']]['distance_km'].mean()),
            'median_km': float(buildings[buildings['within_range']]['distance_km'].median()),
            'min_km': float(buildings[buildings['within_range']]['distance_km'].min()),
            'max_km': float(buildings[buildings['within_range']]['distance_km'].max()),
            'std_km': float(buildings[buildings['within_range']]['distance_km'].std())
        },
        'buildings_per_substation': {
            'mean': float(buildings_per_sub.mean()),
            'median': float(buildings_per_sub.median()),
            'min': int(buildings_per_sub.min()),
            'max': int(buildings_per_sub.max()),
            'std': float(buildings_per_sub.std())
        }
    }

    print(f"  Total buildings: {analysis['total_buildings']:,}")
    print(f"  Buildings matched: {analysis['buildings_matched']:,} ({100*analysis['match_rate']:.1f}%)")
    print(f"  Mean distance: {analysis['distance_stats']['mean_km']:.2f} km")
    print(f"  Buildings per substation: {analysis['buildings_per_substation']['mean']:.0f} ± {analysis['buildings_per_substation']['std']:.0f}")
    print(f"  Range: {analysis['buildings_per_substation']['min']} - {analysis['buildings_per_substation']['max']}")

    return analysis


def save_results(buildings, substations, analysis, output_dir):
    """
    Save spatial join results to disk.

    Args:
        buildings: Joined buildings GeoDataFrame
        substations: Substations GeoDataFrame
        analysis: Analysis results dict
        output_dir: Output directory
    """
    print("\nSaving results...")

    # 1. Buildings with substation assignments (matched only)
    matched = buildings[buildings['within_range']].copy()
    output_file = output_dir / "buildings_with_substations.geojson"
    print(f"  Saving {len(matched):,} matched buildings to {output_file}...")
    matched.to_file(output_file, driver='GeoJSON')

    # 2. Substation building counts
    counts = matched.groupby('substation_id').agg({
        'distance_km': ['count', 'mean', 'median', 'max']
    }).reset_index()
    counts.columns = ['substation_id', 'building_count', 'mean_distance_km', 'median_distance_km', 'max_distance_km']
    counts_file = output_dir / "substation_building_counts.csv"
    print(f"  Saving substation counts to {counts_file}...")
    counts.to_csv(counts_file, index=False)

    # 3. Analysis report
    report_file = output_dir / "analysis_report.json"
    print(f"  Saving analysis report to {report_file}...")
    with open(report_file, 'w') as f:
        json.dump(analysis, f, indent=2)

    # 4. Summary statistics
    summary_file = output_dir / "summary.txt"
    print(f"  Saving summary to {summary_file}...")
    with open(summary_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("SPATIAL JOIN: Buildings to LV Substations\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Timestamp: {analysis['timestamp']}\n\n")
        f.write("INPUT DATA:\n")
        f.write(f"  Total buildings: {analysis['total_buildings']:,}\n")
        f.write(f"  Total substations: {analysis['total_substations']:,}\n\n")
        f.write("MATCHING RESULTS:\n")
        f.write(f"  Buildings matched: {analysis['buildings_matched']:,} ({100*analysis['match_rate']:.1f}%)\n")
        f.write(f"  Buildings unmatched: {analysis['buildings_unmatched']:,}\n\n")
        f.write("DISTANCE STATISTICS:\n")
        f.write(f"  Mean: {analysis['distance_stats']['mean_km']:.2f} km\n")
        f.write(f"  Median: {analysis['distance_stats']['median_km']:.2f} km\n")
        f.write(f"  Range: {analysis['distance_stats']['min_km']:.2f} - {analysis['distance_stats']['max_km']:.2f} km\n")
        f.write(f"  Std Dev: {analysis['distance_stats']['std_km']:.2f} km\n\n")
        f.write("BUILDINGS PER SUBSTATION:\n")
        f.write(f"  Mean: {analysis['buildings_per_substation']['mean']:.0f}\n")
        f.write(f"  Median: {analysis['buildings_per_substation']['median']:.0f}\n")
        f.write(f"  Range: {analysis['buildings_per_substation']['min']} - {analysis['buildings_per_substation']['max']}\n")
        f.write(f"  Std Dev: {analysis['buildings_per_substation']['std']:.0f}\n\n")
        f.write("OUTPUT FILES:\n")
        f.write(f"  - buildings_with_substations.geojson (matched buildings)\n")
        f.write(f"  - substation_building_counts.csv (aggregated counts)\n")
        f.write(f"  - analysis_report.json (full statistics)\n")
        f.write(f"  - summary.txt (this file)\n")

    print(f"\nAll results saved to: {output_dir}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("SPATIAL JOIN: Buildings to LV Substations")
    print("=" * 60)
    print()

    # Check for substation data
    substation_files = [
        RAW_DIR / "nged_11kv_transformers.shp",
        RAW_DIR / "nged_11kv_transformers.geojson",
        PROCESSED_DIR / "lv_substations.geojson",
        RAW_DIR / "lv_substations.geojson"
    ]

    substation_file = None
    for f in substation_files:
        if f.exists():
            substation_file = f
            break

    if not substation_file:
        print("ERROR: No LV substation data found!")
        print("\nPlease download NGED 11kV transformers from:")
        print("  https://connecteddata.nationalgrid.co.uk/dataset/11kv-transformers")
        print("\nSave as one of:")
        for f in substation_files:
            print(f"  {f}")
        sys.exit(1)

    # Check for building data
    building_files = [
        RAW_DIR / "uk_buildings_sample.geojson",
        PROCESSED_DIR / "uk_buildings_sample.geojson",
        RAW_DIR / "overture_buildings.geojson"
    ]

    building_file = None
    for f in building_files:
        if f.exists():
            building_file = f
            break

    if not building_file:
        print("ERROR: No building data found!")
        print("\nPlease ensure you have building footprint data.")
        sys.exit(1)

    # Load data
    substations = load_substations(substation_file)
    if substations is None:
        sys.exit(1)

    buildings = load_buildings_sample(building_file, sample_size=10000)
    if buildings is None:
        sys.exit(1)

    # Perform spatial join
    buildings_joined = nearest_neighbor_join(buildings, substations, max_distance_km=5.0)

    # Analyze results
    analysis = analyze_results(buildings_joined, substations)

    # Save results
    save_results(buildings_joined, substations, analysis, OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
