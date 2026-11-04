#!/usr/bin/env python3
"""
Find and download the TEC Register from NESO
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

NESO_API_BASE = "https://api.neso.energy/api/3/action"
DATA_DIR = Path("data/raw/queue")

def find_tec_register():
    """Search for TEC Register in NESO catalog"""
    print("Searching for TEC Register...")

    # Search for packages
    url = f"{NESO_API_BASE}/package_search"
    params = {
        "q": "tec register",
        "rows": 10
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            results = data["result"]["results"]
            print(f"Found {len(results)} packages matching 'tec register'")

            for pkg in results:
                print(f"\nPackage: {pkg.get('title', 'Unknown')}")
                print(f"  ID: {pkg.get('id', 'N/A')}")
                print(f"  Name: {pkg.get('name', 'N/A')}")
                print(f"  Resources: {len(pkg.get('resources', []))}")

                # Try to download each resource
                for resource in pkg.get("resources", []):
                    res_format = resource.get("format", "").upper()
                    res_name = resource.get("name", "unknown")
                    res_id = resource.get("id", "")

                    print(f"    - {res_name} ({res_format})")

                    if res_format in ["CSV", "XLSX", "XLS"]:
                        download_url = resource.get("url", "")

                        if download_url:
                            try:
                                print(f"      Downloading from: {download_url}")
                                file_response = requests.get(download_url, timeout=120)
                                file_response.raise_for_status()

                                ext = res_format.lower()
                                filename = f"tec_register_{datetime.now().strftime('%Y%m%d')}.{ext}"
                                output_file = DATA_DIR / filename

                                with open(output_file, 'wb') as f:
                                    f.write(file_response.content)

                                print(f"      ✓ Downloaded: {output_file}")

                                # Try to read and show info
                                if ext == 'csv':
                                    df = pd.read_csv(output_file)
                                    print(f"      Records: {len(df)}")
                                    print(f"      Columns: {', '.join(df.columns[:5])}...")
                                    return output_file

                            except Exception as e:
                                print(f"      ✗ Error downloading: {e}")

        return None
    except Exception as e:
        print(f"✗ Error searching for TEC Register: {e}")
        return None

def try_direct_package():
    """Try to access TEC register package directly"""
    print("\nTrying direct package access...")

    package_names = [
        "transmission-entry-capacity-tec-register",
        "tec-register",
        "tec_register",
        "transmission-entry-capacity"
    ]

    for pkg_name in package_names:
        print(f"\nTrying package: {pkg_name}")
        url = f"{NESO_API_BASE}/package_show"
        params = {"id": pkg_name}

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                pkg = data["result"]
                print(f"✓ Found package: {pkg.get('title', 'Unknown')}")

                for resource in pkg.get("resources", []):
                    res_format = resource.get("format", "").upper()
                    res_name = resource.get("name", "unknown")

                    print(f"  Resource: {res_name} ({res_format})")

                    if res_format in ["CSV", "XLSX"]:
                        download_url = resource.get("url", "")

                        try:
                            print(f"    Downloading...")
                            file_response = requests.get(download_url, timeout=120)
                            file_response.raise_for_status()

                            ext = res_format.lower()
                            filename = f"tec_register_{datetime.now().strftime('%Y%m%d')}.{ext}"
                            output_file = DATA_DIR / filename

                            with open(output_file, 'wb') as f:
                                f.write(file_response.content)

                            print(f"    ✓ Downloaded: {output_file}")

                            if ext == 'csv':
                                df = pd.read_csv(output_file)
                                print(f"    Records: {len(df)}")
                                print(f"    Columns: {list(df.columns[:10])}")
                                return output_file

                        except Exception as e:
                            print(f"    ✗ Error: {e}")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"  Not found")
            else:
                print(f"  Error: {e}")
        except Exception as e:
            print(f"  Error: {e}")

    return None

def main():
    print("=" * 80)
    print("TEC Register Download Fix")
    print("=" * 80 + "\n")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Try searching first
    result = find_tec_register()

    if not result:
        # Try direct package access
        result = try_direct_package()

    if result:
        print(f"\n✓ SUCCESS: TEC Register downloaded to {result}")
    else:
        print("\n✗ FAILED: Could not find/download TEC Register")
        print("The data may be available through a web portal download only.")

if __name__ == "__main__":
    main()
