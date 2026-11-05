#!/usr/bin/env python3
"""
Standardize property schemas across all DNO GeoJSON files

Different DNOs use different property names for the same data.
This script creates consistent property names while preserving original data.
"""

import json
from pathlib import Path
import sys

# Color output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

# Property mapping for standardization
PROPERTY_MAPPINGS = {
    'voltage': [
        'voltage', 'Voltage', 'VOLTAGE',
        'kv', 'KV', 'kV',
        'operating_voltage', 'OperatingVoltage',
        'sitevoltage', 'SiteVoltage'
    ],
    'dno': [
        'dno', 'DNO',
        'licensee', 'Licensee',
        'operator', 'Operator',
        'owner', 'Owner'
    ],
    'local_authority': [
        'local_authority', 'LocalAuthority', 'Local_Auth',
        'LA_NAME', 'la_name',
        'authority', 'Authority',
        'council', 'Council'
    ],
    'site_name': [
        'sitename', 'SiteName', 'site_name',
        'name', 'Name', 'NAME',
        'substation_name', 'SubstationName'
    ],
    'site_type': [
        'sitetype', 'SiteType', 'site_type',
        'type', 'Type', 'TYPE',
        'asset_type', 'AssetType'
    ],
    'status': [
        'status', 'Status', 'STATUS',
        'operational_status', 'OperationalStatus',
        'circuit_status', 'CircuitStatus'
    ]
}

def find_property_value(properties, standard_key):
    """Find property value from various possible field names"""
    possible_keys = PROPERTY_MAPPINGS.get(standard_key, [standard_key])

    for key in possible_keys:
        if key in properties:
            return properties[key]

    return None

def standardize_voltage(voltage_value):
    """Standardize voltage format to 'XXXkV'"""
    if voltage_value is None:
        return None

    # Convert to string
    v = str(voltage_value).strip()

    # Already in correct format
    if v.endswith('kV'):
        return v

    # Extract number and add kV
    v = v.replace('KV', '').replace('kv', '').strip()

    try:
        num = float(v)
        return f"{int(num)}kV"
    except:
        return voltage_value

def standardize_dno_name(dno_value):
    """Standardize DNO names"""
    if dno_value is None:
        return None

    dno_map = {
        'LPN': 'UKPN-LPN',
        'SPN': 'UKPN-SPN',
        'EPN': 'UKPN-EPN',
        'UK Power Networks': 'UKPN',
        'Western Power Distribution': 'NGED',
        'WPD': 'NGED',
        'NGED': 'NGED',
        'Northern Powergrid': 'NPG',
        'SSEN': 'SSEN',
        'SSE': 'SSEN',
        'SP Distribution': 'SPEN-SPD',
        'SP Manweb': 'SPEN-SPM',
        'SPEN': 'SPEN',
        'Electricity North West': 'ENWL',
        'ENWL': 'ENWL'
    }

    dno_str = str(dno_value).strip()

    # Check exact matches
    if dno_str in dno_map:
        return dno_map[dno_str]

    # Check partial matches
    for key, value in dno_map.items():
        if key.lower() in dno_str.lower():
            return value

    return dno_str

def standardize_feature_properties(feature, dno_hint=None):
    """Standardize properties for a single feature"""
    props = feature.get('properties', {})

    # Create standardized properties
    std_props = {}

    # Voltage
    voltage = find_property_value(props, 'voltage')
    if voltage:
        std_props['voltage'] = standardize_voltage(voltage)

    # DNO
    dno = find_property_value(props, 'dno')
    if dno:
        std_props['dno'] = standardize_dno_name(dno)
    elif dno_hint:
        std_props['dno'] = dno_hint

    # Local Authority
    local_auth = find_property_value(props, 'local_authority')
    if local_auth:
        std_props['local_authority'] = local_auth

    # Site Name (for substations)
    site_name = find_property_value(props, 'site_name')
    if site_name:
        std_props['site_name'] = site_name

    # Site Type (for substations)
    site_type = find_property_value(props, 'site_type')
    if site_type:
        std_props['site_type'] = site_type

    # Status
    status = find_property_value(props, 'status')
    if status:
        std_props['status'] = status

    # Merge standardized properties back
    feature['properties'] = {**props, **std_props}

    return feature

def process_geojson_file(file_path, dno_code=None):
    """Process a GeoJSON file and standardize properties"""
    print_info(f"Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if data.get('type') != 'FeatureCollection':
        print_warning(f"Not a FeatureCollection: {file_path.name}")
        return False

    features = data.get('features', [])

    if not features:
        print_warning(f"No features found: {file_path.name}")
        return False

    # Standardize each feature
    for i, feature in enumerate(features):
        features[i] = standardize_feature_properties(feature, dno_code)

    data['features'] = features

    # Save back
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    print_success(f"Standardized {len(features):,} features in {file_path.name}")

    return True

def main():
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}DNO Property Standardization{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    data_dir = Path('frontend/public/data')

    if not data_dir.exists():
        print_warning("Data directory not found. Run conversion script first.")
        sys.exit(1)

    # Find all DNO GeoJSON files
    dno_files = {}

    for dno_code in ['ukpn', 'nged', 'npg', 'ssen', 'spen', 'enwl']:
        pattern = f"{dno_code}-*.geojson"
        files = list(data_dir.glob(pattern))
        if files:
            dno_files[dno_code.upper()] = files

    if not dno_files:
        print_warning("No DNO GeoJSON files found in frontend/public/data/")
        print_info("Run: python scripts/convert_dno_shapefiles.py")
        sys.exit(1)

    # Process each DNO's files
    total_processed = 0

    for dno_code, files in dno_files.items():
        print(f"\n{Colors.BOLD}{dno_code}:{Colors.ENDC}")

        for file_path in files:
            if process_geojson_file(file_path, dno_code):
                total_processed += 1

    # Summary
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}SUMMARY{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    print(f"Total files processed: {total_processed}")
    print("")

    print_info("Next step: python scripts/combine_dno_data.py")

if __name__ == '__main__':
    main()
