#!/usr/bin/env python3
"""
Download NESO (National Energy System Operator) data
Includes: TEC Register, Historic Demand, GIS Boundaries
"""

import requests
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# Base URLs
NESO_API_BASE = "https://api.neso.energy/api/3/action"
DATA_DIR = Path("data/raw")

def download_tec_register():
    """Download Transmission Entry Capacity (TEC) Register - Connection Queue"""
    print("Downloading TEC Register (Connection Queue)...")

    url = f"{NESO_API_BASE}/datastore_search"
    params = {
        "resource_id": "tec_register",
        "limit": 10000  # Get all records
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            records = data["result"]["records"]
            df = pd.DataFrame(records)

            output_file = DATA_DIR / "queue" / f"tec_register_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ TEC Register downloaded: {len(df)} projects, {output_file}")
            return df
        else:
            print("✗ Failed to download TEC Register")
            return None
    except Exception as e:
        print(f"✗ Error downloading TEC Register: {e}")
        return None

def download_gsp_boundaries():
    """Download Grid Supply Point (GSP) boundaries GeoJSON"""
    print("Downloading GSP Boundaries...")

    # Find the GSP boundaries resource
    url = f"{NESO_API_BASE}/package_show"
    params = {"id": "gis-boundaries-for-gb-grid-supply-points"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            resources = data["result"]["resources"]

            # Look for GeoJSON resource
            for resource in resources:
                if "geojson" in resource.get("format", "").lower():
                    download_url = resource["url"]

                    geo_response = requests.get(download_url)
                    geo_response.raise_for_status()

                    output_file = DATA_DIR / "infrastructure" / f"gsp_boundaries_{datetime.now().strftime('%Y%m%d')}.geojson"
                    with open(output_file, 'w') as f:
                        json.dump(geo_response.json(), f, indent=2)

                    print(f"✓ GSP Boundaries downloaded: {output_file}")
                    return output_file

        print("✗ GSP Boundaries not found")
        return None
    except Exception as e:
        print(f"✗ Error downloading GSP Boundaries: {e}")
        return None

def download_historic_demand():
    """Download historic demand data"""
    print("Downloading Historic Demand Data...")

    # Search for historic demand datasets
    url = f"{NESO_API_BASE}/package_search"
    params = {
        "q": "historic demand",
        "rows": 100
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            datasets = data["result"]["results"]
            downloaded = []

            for dataset in datasets:
                if "historic" in dataset.get("title", "").lower() and "demand" in dataset.get("title", "").lower():
                    for resource in dataset.get("resources", []):
                        if resource.get("format", "").upper() in ["CSV", "XLSX"]:
                            download_url = resource["url"]
                            filename = resource.get("name", resource.get("id", "unknown"))

                            # Download file
                            file_response = requests.get(download_url, timeout=60)
                            file_response.raise_for_status()

                            ext = resource.get("format", "csv").lower()
                            output_file = DATA_DIR / "demand" / f"{filename.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{ext}"

                            with open(output_file, 'wb') as f:
                                f.write(file_response.content)

                            downloaded.append(output_file)
                            print(f"✓ Downloaded: {output_file.name}")
                            time.sleep(1)  # Be polite to the API

            print(f"✓ Historic Demand: {len(downloaded)} files downloaded")
            return downloaded

        print("✗ No historic demand data found")
        return None
    except Exception as e:
        print(f"✗ Error downloading historic demand: {e}")
        return None

def list_available_datasets():
    """List all available datasets from NESO"""
    print("Fetching available NESO datasets...")

    url = f"{NESO_API_BASE}/package_list"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            datasets = data["result"]
            print(f"\n✓ Found {len(datasets)} datasets")

            # Save list
            output_file = DATA_DIR / "neso_datasets_list.txt"
            with open(output_file, 'w') as f:
                f.write(f"NESO Available Datasets ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
                f.write("=" * 80 + "\n\n")
                for dataset in sorted(datasets):
                    f.write(f"{dataset}\n")

            print(f"✓ Dataset list saved to: {output_file}")
            return datasets

        return None
    except Exception as e:
        print(f"✗ Error listing datasets: {e}")
        return None

def main():
    print("=" * 80)
    print("NESO Data Download Script")
    print("=" * 80 + "\n")

    # Create output directories
    (DATA_DIR / "queue").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "infrastructure").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "demand").mkdir(parents=True, exist_ok=True)

    # List available datasets
    list_available_datasets()
    print()

    # Download key datasets
    tec_df = download_tec_register()
    print()

    gsp_file = download_gsp_boundaries()
    print()

    demand_files = download_historic_demand()
    print()

    print("=" * 80)
    print("Download Summary")
    print("=" * 80)
    print(f"TEC Register: {'✓' if tec_df is not None else '✗'}")
    print(f"GSP Boundaries: {'✓' if gsp_file else '✗'}")
    print(f"Historic Demand: {'✓' if demand_files else '✗'}")
    print()

if __name__ == "__main__":
    main()
