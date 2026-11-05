#!/usr/bin/env python3
"""
Download distribution network infrastructure data (overhead lines & substations) from all UK DNOs

This script downloads 132kV, 66kV, 33kV overhead lines and substation data from:
- UKPN (automated)
- NGED, NPG, SSEN, SPEN, ENWL (manual instructions provided)
"""

import os
import sys
from pathlib import Path
import json

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_step(step_num, text):
    print(f"{Colors.CYAN}{Colors.BOLD}Step {step_num}:{Colors.ENDC} {text}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")

# DNO configuration
DNO_CONFIG = {
    'UKPN': {
        'name': 'UK Power Networks',
        'coverage': 'London, SE England, East England',
        'customers': '8.4M',
        'portal': 'https://ukpowernetworks.opendatasoft.com/',
        'registration_required': False,
        'datasets': {
            '132kV_OHL': {
                'name': '132kV Overhead Lines',
                'url': 'https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets/ukpn-132kv-overhead-lines/exports/shp',
                'output': 'ukpn-132kv-overhead-lines.zip'
            },
            '66kV_OHL': {
                'name': '66kV Overhead Lines',
                'url': 'https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets/ukpn-66kv-overhead-lines-shapefile/exports/shp',
                'output': 'ukpn-66kv-overhead-lines.zip'
            },
            '33kV_OHL': {
                'name': '33kV Overhead Lines',
                'url': 'https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets/ukpn-33kv-overhead-lines/exports/shp',
                'output': 'ukpn-33kv-overhead-lines.zip'
            },
            'substations': {
                'name': 'Grid and Primary Sites',
                'url': 'https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets/grid-and-primary-sites/exports/shp',
                'output': 'ukpn-substations.zip'
            }
        }
    },
    'NGED': {
        'name': 'National Grid Electricity Distribution',
        'coverage': 'Midlands, South West, South Wales',
        'customers': '7.9M',
        'portal': 'https://connecteddata.nationalgrid.co.uk/',
        'registration_required': True,
        'manual_instructions': """
1. Visit https://connecteddata.nationalgrid.co.uk/
2. Register for a free account
3. Navigate to "System and Network" section
4. Download the following datasets as ESRI Shapefiles (.zip):
   - 132kV Overhead Lines (Full NGED Area - 4 DNOs)
   - 66kV Overhead Lines (Full NGED Area - 4 DNOs)
   - 33kV Overhead Lines (Full NGED Area - 4 DNOs)
   - Primary Substations (Full NGED Area - 4 DNOs)
5. Save downloaded ZIP files to: data/dno/nged/raw/
        """,
        'datasets': {
            '132kV_OHL': 'data/dno/nged/raw/132kv_ohl_nged.zip',
            '66kV_OHL': 'data/dno/nged/raw/66kv_ohl_nged.zip',
            '33kV_OHL': 'data/dno/nged/raw/33kv_ohl_nged.zip',
            'substations': 'data/dno/nged/raw/primary_substations_nged.zip'
        }
    },
    'NPG': {
        'name': 'Northern Powergrid',
        'coverage': 'NE England, Yorkshire',
        'customers': '3.9M',
        'portal': 'https://northernpowergrid.opendatasoft.com/',
        'registration_required': True,
        'manual_instructions': """
1. Visit https://northernpowergrid.opendatasoft.com/
2. Register for a free account
3. Search for "LTDS" (Long Term Development Statement) datasets
4. Download network schematic data containing 132kV, 66kV, 33kV information
5. Save downloaded files to: data/dno/npg/raw/

Note: NPG provides schematic diagrams. You may need to extract line data
from LTDS appendices or contact NPG for GIS exports.
        """,
        'datasets': {
            'network_data': 'data/dno/npg/raw/ltds_network_data.zip'
        }
    },
    'SSEN': {
        'name': 'SSE Energy Networks',
        'coverage': 'N Scotland, S England',
        'customers': '3.9M',
        'portal': 'https://data.ssen.co.uk/',
        'registration_required': False,
        'manual_instructions': """
1. Visit https://data.ssen.co.uk/
2. Search for "SSEN Substation Data"
3. Download substation datasets (XLSX/CSV format)
4. Save to: data/dno/ssen/raw/

Note: SSEN primarily provides substation point data. Overhead line data
may be limited or require special request from SSEN.

Alternative: Check https://www.ssen.co.uk/ for network development reports
which may contain GIS data or contact SSEN for line infrastructure data.
        """,
        'datasets': {
            'substations': 'data/dno/ssen/raw/ssen_substations.csv'
        }
    },
    'SPEN': {
        'name': 'Scottish Power Energy Networks',
        'coverage': 'Scotland, NW England, N Wales',
        'customers': '3.5M',
        'portal': 'https://spenergynetworks.opendatasoft.com/',
        'registration_required': True,
        'manual_instructions': """
1. Visit https://spenergynetworks.opendatasoft.com/
2. Register and request access to "GIS Shapefiles" section
3. Navigate to "SPD & SPT GIS Shapefiles - Line Assets"
4. Download shapefiles for:
   - SPD (SP Distribution) - 132kV, 66kV, 33kV overhead lines
   - SPM (SP Manweb) - 132kV, 66kV, 33kV overhead lines
5. Save to: data/dno/spen/raw/

The dataset includes voltage, status, and operating voltage for all line assets.
        """,
        'datasets': {
            'line_assets_spd': 'data/dno/spen/raw/spd_line_assets.zip',
            'line_assets_spm': 'data/dno/spen/raw/spm_line_assets.zip',
            'substations': 'data/dno/spen/raw/spen_substations.zip'
        }
    },
    'ENWL': {
        'name': 'Electricity North West',
        'coverage': 'NW England (Manchester, Lancashire)',
        'customers': '2.4M',
        'portal': 'https://electricitynorthwest.opendatasoft.com/',
        'registration_required': False,
        'manual_instructions': """
1. Visit https://electricitynorthwest.opendatasoft.com/
2. Search for network infrastructure datasets
3. Download:
   - SP ENW GIS Substations
   - Any available overhead line datasets
4. Save to: data/dno/enwl/raw/

Note: ENWL provides mainly substation data via their portal.
For overhead line data, you may need to:
- Check "Network Information" section on main ENWL website
- Request GIS data from ENWL customer services
- Check quarterly network capacity reports
        """,
        'datasets': {
            'substations': 'data/dno/enwl/raw/enwl_substations.zip'
        }
    }
}

def create_directory_structure():
    """Create directory structure for DNO data"""
    print_step(1, "Creating directory structure...")

    dirs = ['data/dno/downloads', 'frontend/public/data']

    for dno in DNO_CONFIG.keys():
        dirs.extend([
            f'data/dno/{dno.lower()}/raw',
            f'data/dno/{dno.lower()}/processed'
        ])

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print_success("Directory structure created")

def download_ukpn_data():
    """Download UKPN data via API (no registration required)"""
    print_header("DOWNLOADING UKPN DATA (Automated)")

    try:
        import requests
        from tqdm import tqdm
    except ImportError:
        print_error("Required packages missing. Install with:")
        print("  pip install requests tqdm")
        return False

    ukpn = DNO_CONFIG['UKPN']
    success_count = 0

    for dataset_key, dataset_info in ukpn['datasets'].items():
        print_step(dataset_key, f"Downloading {dataset_info['name']}...")

        output_path = f"data/dno/ukpn/raw/{dataset_info['output']}"

        if os.path.exists(output_path):
            print_warning(f"File already exists: {output_path}")
            success_count += 1
            continue

        try:
            response = requests.get(dataset_info['url'], stream=True, timeout=300)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(output_path, 'wb') as f, tqdm(
                desc=dataset_info['name'],
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    size = f.write(chunk)
                    pbar.update(size)

            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print_success(f"Downloaded: {output_path} ({file_size:.1f} MB)")
            success_count += 1

        except requests.exceptions.Timeout:
            print_error(f"Timeout downloading {dataset_info['name']}. Try again later.")
        except Exception as e:
            print_error(f"Failed to download {dataset_info['name']}: {e}")

    return success_count == len(ukpn['datasets'])

def print_manual_instructions():
    """Print manual download instructions for DNOs requiring registration"""
    print_header("MANUAL DOWNLOAD INSTRUCTIONS")

    print_info("The following DNOs require manual download after registration:\n")

    for dno_code, dno_info in DNO_CONFIG.items():
        if dno_code == 'UKPN':
            continue

        print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{dno_info['name']} ({dno_code}){Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.ENDC}")
        print(f"Coverage: {dno_info['coverage']}")
        print(f"Customers: {dno_info['customers']}")
        print(f"Portal: {dno_info['portal']}")
        print(f"Registration: {'Required' if dno_info['registration_required'] else 'Not Required'}")

        if 'manual_instructions' in dno_info:
            print(f"\n{Colors.CYAN}Instructions:{Colors.ENDC}")
            print(dno_info['manual_instructions'])

        print(f"\n{Colors.WARNING}Expected file paths:{Colors.ENDC}")
        for dataset_key, dataset_path in dno_info['datasets'].items():
            if isinstance(dataset_path, str):
                print(f"  • {dataset_path}")

def save_download_checklist():
    """Save a markdown checklist"""
    checklist_path = 'data/dno/DOWNLOAD_CHECKLIST.md'

    content = """# UK DNO Distribution Network Data Download Checklist

This checklist tracks download progress for distribution network infrastructure data from all UK DNOs.

**Goal**: Complete UK coverage with 132kV, 66kV, 33kV overhead lines and substations.

Mark completed items by changing `[ ]` to `[x]`.

---

"""

    total_datasets = 0
    completed_datasets = 1  # UKPN automated

    for dno_code, dno_info in DNO_CONFIG.items():
        content += f"## {dno_info['name']} ({dno_code})\n\n"
        content += f"- **Coverage**: {dno_info['coverage']}\n"
        content += f"- **Customers**: {dno_info['customers']}\n"
        content += f"- **Portal**: {dno_info['portal']}\n"
        content += f"- **Registration**: {'✅ Required' if dno_info['registration_required'] else '❌ Not Required'}\n\n"

        content += "### Datasets:\n\n"

        for dataset_key, dataset_value in dno_info['datasets'].items():
            total_datasets += 1
            status = "[x]" if dno_code == "UKPN" else "[ ]"

            if isinstance(dataset_value, dict):
                dataset_name = dataset_value.get('name', dataset_key)
                if 'manual_path' in dataset_value:
                    path = dataset_value['manual_path']
                elif 'output' in dataset_value:
                    path = f"data/dno/ukpn/raw/{dataset_value['output']}"
                else:
                    path = "See instructions above"
            else:
                dataset_name = dataset_key
                path = dataset_value

            content += f"{status} **{dataset_name}**\n"
            content += f"   - Path: `{path}`\n\n"

        content += "---\n\n"

    content = f"""# UK DNO Distribution Network Data Download Checklist

**Progress**: {completed_datasets}/{total_datasets} datasets downloaded ({completed_datasets/total_datasets*100:.0f}%)

**Goal**: Complete UK coverage with 132kV, 66kV, 33kV overhead lines and substations.

Mark completed items by changing `[ ]` to `[x]`.

---

""" + content

    with open(checklist_path, 'w') as f:
        f.write(content)

    print_success(f"Download checklist saved: {checklist_path}")
    return checklist_path

def main():
    print_header("UK DNO DISTRIBUTION NETWORK DATA DOWNLOADER")

    print_info("This script will:")
    print("  • Create directory structure")
    print("  • Download UKPN data automatically")
    print("  • Provide manual instructions for other DNOs")
    print("")

    # Create directories
    create_directory_structure()

    # Download UKPN
    ukpn_success = download_ukpn_data()

    # Manual instructions
    print_manual_instructions()

    # Save checklist
    checklist_file = save_download_checklist()

    # Summary
    print_header("SUMMARY")

    if ukpn_success:
        print_success("UKPN data downloaded successfully (25% UK coverage)")
    else:
        print_warning("UKPN download incomplete")

    print_info("\nNext steps:")
    print(f"  1. Follow manual download instructions above")
    print(f"  2. Track progress in: {checklist_file}")
    print(f"  3. Run: python scripts/convert_dno_shapefiles.py")
    print("")

if __name__ == '__main__':
    main()
