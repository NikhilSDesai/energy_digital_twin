#!/usr/bin/env python3
"""
Download DNO (Distribution Network Operator) data
Includes: UKPN, SSEN, NGED, Northern Powergrid
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

DATA_DIR = Path("data/raw")

def download_ukpn_data():
    """Download UK Power Networks data"""
    print("Downloading UK Power Networks data...")

    # UKPN uses OpenDataSoft platform
    base_url = "https://ukpowernetworks.opendatasoft.com/api/records/1.0/search/"

    datasets = [
        {
            "dataset": "ukpn-smart-meter-demand-data-aggregated-gsp",
            "filename": "ukpn_smart_meter_gsp",
            "description": "Smart meter demand at GSP level"
        },
        {
            "dataset": "ukpn-substations-open-data",
            "filename": "ukpn_substations",
            "description": "Substation locations and specs"
        },
        {
            "dataset": "ukpn-overhead-line-data",
            "filename": "ukpn_overhead_lines",
            "description": "Overhead transmission lines"
        }
    ]

    downloaded = []
    for ds in datasets:
        try:
            print(f"  Downloading {ds['description']}...")

            params = {
                "dataset": ds["dataset"],
                "rows": 10000,
                "format": "json"
            }

            response = requests.get(base_url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()

            if "records" in data:
                records = [r["fields"] for r in data["records"]]
                df = pd.DataFrame(records)

                output_file = DATA_DIR / "infrastructure" / f"{ds['filename']}_{datetime.now().strftime('%Y%m%d')}.csv"
                df.to_csv(output_file, index=False)
                print(f"  ✓ {ds['description']}: {len(df)} records")
                downloaded.append(output_file)
            else:
                print(f"  ✗ No records found for {ds['description']}")

        except Exception as e:
            print(f"  ✗ Error downloading {ds['description']}: {e}")

    return downloaded

def download_ssen_data():
    """Download Scottish and Southern Energy Networks data"""
    print("Downloading SSEN data...")

    # SSEN data portal base
    base_url = "https://data.ssen.co.uk/api/3/action"

    try:
        # List available packages
        list_url = f"{base_url}/package_list"
        response = requests.get(list_url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            packages = data["result"]
            print(f"  Found {len(packages)} SSEN datasets")

            # Save package list
            output_file = DATA_DIR / "ssen_datasets_list.txt"
            with open(output_file, 'w') as f:
                f.write(f"SSEN Available Datasets ({datetime.now().strftime('%Y-%m-%d')})\n")
                f.write("=" * 80 + "\n\n")
                for pkg in sorted(packages):
                    f.write(f"{pkg}\n")

            print(f"  ✓ Dataset list saved to: {output_file}")

            # Download key datasets (substations, demand data)
            key_datasets = []
            for pkg in packages:
                if any(term in pkg.lower() for term in ["substation", "demand", "smart", "capacity"]):
                    key_datasets.append(pkg)

            print(f"  Found {len(key_datasets)} relevant datasets")
            for dataset in key_datasets[:5]:  # Limit to first 5 for now
                print(f"    - {dataset}")

            return key_datasets

    except Exception as e:
        print(f"  ✗ Error downloading SSEN data: {e}")
        return None

def download_nged_data():
    """Download National Grid Electricity Distribution data"""
    print("Downloading NGED data...")

    # NGED uses National Grid Connected Data portal
    base_url = "https://connecteddata.nationalgrid.co.uk/api/3/action"

    try:
        # Search for connection queue data
        search_url = f"{base_url}/package_search"
        params = {
            "q": "connection queue",
            "rows": 50
        }

        response = requests.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            datasets = data["result"]["results"]
            print(f"  Found {len(datasets)} connection-related datasets")

            downloaded = []
            for dataset in datasets[:3]:  # Download first 3
                title = dataset.get("title", "Unknown")
                print(f"  Processing: {title}")

                for resource in dataset.get("resources", []):
                    if resource.get("format", "").upper() in ["CSV", "XLSX"]:
                        download_url = resource["url"]

                        try:
                            file_response = requests.get(download_url, timeout=60)
                            file_response.raise_for_status()

                            ext = resource.get("format", "csv").lower()
                            filename = f"nged_{resource.get('name', 'data').replace(' ', '_')}"
                            output_file = DATA_DIR / "queue" / f"{filename}_{datetime.now().strftime('%Y%m%d')}.{ext}"

                            with open(output_file, 'wb') as f:
                                f.write(file_response.content)

                            print(f"  ✓ Downloaded: {output_file.name}")
                            downloaded.append(output_file)
                            break  # One resource per dataset
                        except Exception as e:
                            print(f"  ✗ Error downloading resource: {e}")

            return downloaded

    except Exception as e:
        print(f"  ✗ Error downloading NGED data: {e}")
        return None

def download_northern_powergrid_data():
    """Download Northern Powergrid data"""
    print("Downloading Northern Powergrid data...")

    # Northern Powergrid uses OpenDataSoft
    base_url = "https://northernpowergrid.opendatasoft.com/api/records/1.0/search/"

    try:
        # Get available datasets
        catalog_url = "https://northernpowergrid.opendatasoft.com/api/datasets/1.0/search/"
        response = requests.get(catalog_url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "datasets" in data:
            datasets = data["datasets"]
            print(f"  Found {len(datasets)} datasets")

            # Save dataset list
            output_file = DATA_DIR / "northern_powergrid_datasets_list.txt"
            with open(output_file, 'w') as f:
                f.write(f"Northern Powergrid Available Datasets ({datetime.now().strftime('%Y-%m-%d')})\n")
                f.write("=" * 80 + "\n\n")
                for ds in datasets:
                    dataset_id = ds.get("datasetid", "Unknown")
                    title = ds.get("metas", {}).get("default", {}).get("title", "No title")
                    f.write(f"{dataset_id}: {title}\n")

            print(f"  ✓ Dataset list saved to: {output_file}")
            return datasets

    except Exception as e:
        print(f"  ✗ Error downloading Northern Powergrid data: {e}")
        return None

def main():
    print("=" * 80)
    print("DNO Data Download Script")
    print("=" * 80 + "\n")

    # Create output directories
    (DATA_DIR / "infrastructure").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "queue").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "demand").mkdir(parents=True, exist_ok=True)

    # Download from each DNO
    ukpn_files = download_ukpn_data()
    print()

    ssen_datasets = download_ssen_data()
    print()

    nged_files = download_nged_data()
    print()

    npg_datasets = download_northern_powergrid_data()
    print()

    print("=" * 80)
    print("Download Summary")
    print("=" * 80)
    print(f"UKPN: {len(ukpn_files) if ukpn_files else 0} files")
    print(f"SSEN: {len(ssen_datasets) if ssen_datasets else 0} datasets identified")
    print(f"NGED: {len(nged_files) if nged_files else 0} files")
    print(f"Northern Powergrid: {len(npg_datasets) if npg_datasets else 0} datasets identified")
    print()

if __name__ == "__main__":
    main()
