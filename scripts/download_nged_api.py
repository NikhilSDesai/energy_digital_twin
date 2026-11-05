#!/usr/bin/env python3
"""
Download NGED spatial datasets via API

Automatically fetches and downloads:
- 132kV Overhead Lines
- 66kV Overhead Lines
- 33kV Overhead Lines
- Primary Substations

From NGED Connected Data Portal API
"""

import requests
import json
import os
from pathlib import Path
from urllib.parse import urljoin

# Color output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")

# NGED API endpoints
NGED_API_BASE = "https://connecteddata.nationalgrid.co.uk"
DATAPACKAGE_URL = f"{NGED_API_BASE}/dataset/spatial-datasets/datapackage.json"

# What we're looking for
TARGET_DATASETS = {
    '132kV_OHL': {
        'keywords': ['132', 'overhead', 'line'],
        'exclude': ['underground', 'cable', 'tower', 'pole', 'substation'],
        'output': '132kv_ohl_nged.gpkg'
    },
    '66kV_OHL': {
        'keywords': ['66', 'overhead', 'line'],
        'exclude': ['underground', 'cable', 'tower', 'pole', 'substation'],
        'output': '66kv_ohl_nged.gpkg'
    },
    '33kV_OHL': {
        'keywords': ['33', 'overhead', 'line'],
        'exclude': ['underground', 'cable', 'tower', 'pole', 'substation'],
        'output': '33kv_ohl_nged.gpkg'
    },
    'substations': {
        'keywords': ['primary', 'substation'],
        'exclude': ['secondary', 'pole'],
        'output': 'primary_substations_nged.gpkg'
    }
}

def get_session():
    """Create a session with authentication if needed"""
    session = requests.Session()

    # Check for API key in environment variable
    api_key = os.environ.get('NGED_API_KEY')
    if api_key:
        print_info("Using API key from NGED_API_KEY environment variable")
        session.headers.update({'Authorization': f'Bearer {api_key}'})

    return session

def fetch_datapackage():
    """Fetch and parse the datapackage.json from NGED API"""
    print_info("Fetching NGED spatial datasets catalog...")

    session = get_session()

    try:
        response = session.get(DATAPACKAGE_URL, timeout=30)

        # If forbidden, provide helpful message
        if response.status_code == 403:
            print_warning("API returned 403 Forbidden")
            print_info("The NGED portal may require browser-based download")
            print_info("Trying alternative approach...")

            # Try without auth - some endpoints may be public
            response = requests.get(DATAPACKAGE_URL, timeout=30, allow_redirects=True)

        response.raise_for_status()

        data = response.json()
        print_success(f"Found {len(data.get('resources', []))} spatial datasets")

        return data

    except requests.exceptions.RequestException as e:
        print_error(f"Failed to fetch datapackage: {e}")
        print()
        print_info("Alternative: Try direct dataset URLs")
        print_info("Visit: https://connecteddata.nationalgrid.co.uk/group/system-and-network")
        print_info("Then use browser to download files manually")
        return None
    except json.JSONDecodeError as e:
        print_error(f"Failed to parse JSON: {e}")
        return None

def match_dataset(resource, target_config):
    """Check if a resource matches our target criteria"""
    name = resource.get('name', '').lower()
    title = resource.get('title', '').lower()
    description = resource.get('description', '').lower()

    combined = f"{name} {title} {description}"

    # Check if all keywords are present
    has_keywords = all(kw.lower() in combined for kw in target_config['keywords'])

    # Check if any exclusions are present
    has_exclusions = any(ex.lower() in combined for ex in target_config['exclude'])

    return has_keywords and not has_exclusions

def find_datasets(datapackage):
    """Find the specific datasets we need"""
    print_header("Searching for Target Datasets")

    resources = datapackage.get('resources', [])
    found = {}

    for target_name, target_config in TARGET_DATASETS.items():
        print_info(f"Looking for {target_name}...")

        matches = []
        for resource in resources:
            if match_dataset(resource, target_config):
                matches.append(resource)

        if matches:
            # Prefer the first match (usually most comprehensive)
            found[target_name] = matches[0]
            resource_name = found[target_name].get('name', 'Unknown')
            print_success(f"Found: {resource_name}")
        else:
            print_warning(f"Not found: {target_name}")
            # Print available resources with similar keywords for debugging
            similar = []
            for resource in resources:
                name = resource.get('name', '').lower()
                if any(kw.lower() in name for kw in target_config['keywords'][:1]):
                    similar.append(resource.get('name', 'Unknown'))

            if similar:
                print_info(f"Similar datasets available: {', '.join(similar[:3])}")

    return found

def download_file(url, output_path, description):
    """Download a file with progress indication"""
    print_info(f"Downloading {description}...")
    print(f"  URL: {url}")
    print(f"  Output: {output_path}")

    try:
        # Stream download to handle large files
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()

        # Get file size if available
        total_size = int(response.headers.get('content-length', 0))

        # Download with progress
        downloaded = 0
        chunk_size = 8192

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Show progress
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        mb_downloaded = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        print(f"\r  Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='', flush=True)

        print()  # New line after progress

        # Verify file was created
        file_size = os.path.getsize(output_path)
        print_success(f"Downloaded: {output_path.name} ({file_size / (1024*1024):.2f} MB)")

        return True

    except requests.exceptions.RequestException as e:
        print_error(f"Download failed: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def main():
    print_header("NGED Spatial Datasets Downloader")

    # Create output directory
    output_dir = Path('data/dno/nged/raw')
    output_dir.mkdir(parents=True, exist_ok=True)
    print_success(f"Output directory: {output_dir}")

    # Fetch datapackage
    datapackage = fetch_datapackage()
    if not datapackage:
        print_error("Failed to fetch datapackage. Exiting.")
        return 1

    # Find our target datasets
    found_datasets = find_datasets(datapackage)

    if not found_datasets:
        print_error("No datasets found. Check API or search criteria.")
        return 1

    # Download each dataset
    print_header(f"Downloading {len(found_datasets)} Datasets")

    success_count = 0
    failed = []

    for target_name, resource in found_datasets.items():
        target_config = TARGET_DATASETS[target_name]
        output_file = output_dir / target_config['output']

        # Get download URL
        path = resource.get('path')
        if not path:
            print_warning(f"No path found for {target_name}")
            failed.append(target_name)
            continue

        # Construct full URL
        if path.startswith('http'):
            download_url = path
        else:
            download_url = urljoin(NGED_API_BASE, path)

        # Download
        if download_file(download_url, output_file, resource.get('name', target_name)):
            success_count += 1
        else:
            failed.append(target_name)

    # Summary
    print_header("Download Summary")
    print(f"Successful: {success_count}/{len(found_datasets)}")

    if failed:
        print_warning(f"Failed: {', '.join(failed)}")

    if success_count > 0:
        print()
        print_success("NGED data download complete!")
        print()
        print_info("Next steps:")
        print("  1. Run: python3 scripts/convert_dno_shapefiles.py")
        print("  2. Run: python3 scripts/standardize_dno_properties.py")
        print("  3. Run: python3 scripts/combine_dno_data.py")
        print()
        print("Or use the master script:")
        print("  ./scripts/process_all_dno_data.sh")

    return 0 if success_count == len(found_datasets) else 1

if __name__ == '__main__':
    exit(main())
