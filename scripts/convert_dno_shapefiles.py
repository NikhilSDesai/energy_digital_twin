#!/usr/bin/env python3
"""
Convert DNO shapefiles to GeoJSON format

This script:
1. Finds all downloaded shapefile ZIP archives
2. Extracts and converts to GeoJSON
3. Reprojects to WGS84 (EPSG:4326)
4. Adds DNO identifier to properties
5. Saves to frontend/public/data/
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import json

try:
    import geopandas as gpd
    from shapely.geometry import shape
except ImportError:
    print("❌ Required packages missing. Install with:")
    print("   pip install geopandas shapely")
    sys.exit(1)

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

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

def extract_shapefile_from_zip(zip_path, temp_dir):
    """Extract shapefile from ZIP archive"""
    print_info(f"Extracting: {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Find .shp file
    shp_files = list(Path(temp_dir).rglob('*.shp'))

    if not shp_files:
        raise FileNotFoundError(f"No .shp file found in {zip_path}")

    if len(shp_files) > 1:
        print_warning(f"Multiple .shp files found, using: {shp_files[0].name}")

    return str(shp_files[0])

def convert_shapefile_to_geojson(shp_path, output_path, dno_code, voltage=None):
    """Convert shapefile to GeoJSON with DNO tagging"""

    print_info(f"Reading shapefile: {Path(shp_path).name}")

    # Read shapefile
    gdf = gpd.read_file(shp_path)

    # Check CRS and reproject if needed
    if gdf.crs is None:
        print_warning("No CRS found, assuming EPSG:27700 (British National Grid)")
        gdf.set_crs('EPSG:27700', inplace=True)

    if gdf.crs != 'EPSG:4326':
        print_info(f"Reprojecting from {gdf.crs} to EPSG:4326")
        gdf = gdf.to_crs('EPSG:4326')

    # Add DNO identifier
    gdf['dno'] = dno_code

    # Add voltage if specified
    if voltage and 'voltage' not in gdf.columns:
        gdf['voltage'] = voltage

    # Remove null geometries
    gdf = gdf[gdf.geometry.notnull()]

    # Save as GeoJSON
    gdf.to_file(output_path, driver='GeoJSON')

    # Get statistics
    feature_count = len(gdf)
    file_size = os.path.getsize(output_path) / (1024 * 1024)

    return {
        'features': feature_count,
        'size_mb': file_size,
        'crs': str(gdf.crs),
        'bounds': gdf.total_bounds.tolist()
    }

def process_ukpn_data():
    """Process UKPN shapefiles"""
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}Processing UKPN Data{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    raw_dir = Path('data/dno/ukpn/raw')
    output_dir = Path('frontend/public/data')
    temp_dir = Path('data/dno/ukpn/temp')

    datasets = {
        'ukpn-132kv-overhead-lines.zip': ('132kV', 'ukpn-132kv-overhead-lines.geojson'),
        'ukpn-66kv-overhead-lines.zip': ('66kV', 'ukpn-66kv-overhead-lines.geojson'),
        'ukpn-33kv-overhead-lines.zip': ('33kV', 'ukpn-33kv-overhead-lines.geojson'),
        'ukpn-substations.zip': (None, 'ukpn-substations.geojson')
    }

    results = []

    for zip_file, (voltage, output_file) in datasets.items():
        zip_path = raw_dir / zip_file

        if not zip_path.exists():
            print_warning(f"Not found: {zip_path}")
            continue

        try:
            # Extract
            temp_dir.mkdir(parents=True, exist_ok=True)
            shp_path = extract_shapefile_from_zip(zip_path, temp_dir)

            # Convert
            output_path = output_dir / output_file
            stats = convert_shapefile_to_geojson(shp_path, output_path, 'UKPN', voltage)

            print_success(f"{output_file}: {stats['features']} features, {stats['size_mb']:.2f} MB")

            results.append({
                'dno': 'UKPN',
                'dataset': output_file,
                **stats
            })

            # Cleanup temp
            shutil.rmtree(temp_dir)

        except Exception as e:
            print_error(f"Failed to process {zip_file}: {e}")

    return results

def process_nged_data():
    """Process NGED shapefiles"""
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}Processing NGED Data{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    raw_dir = Path('data/dno/nged/raw')
    output_dir = Path('frontend/public/data')
    temp_dir = Path('data/dno/nged/temp')

    datasets = {
        '132kv_ohl_nged.zip': ('132kV', 'nged-132kv-overhead-lines.geojson'),
        '66kv_ohl_nged.zip': ('66kV', 'nged-66kv-overhead-lines.geojson'),
        '33kv_ohl_nged.zip': ('33kV', 'nged-33kv-overhead-lines.geojson'),
        'primary_substations_nged.zip': (None, 'nged-substations.geojson')
    }

    results = []

    for zip_file, (voltage, output_file) in datasets.items():
        zip_path = raw_dir / zip_file

        if not zip_path.exists():
            print_warning(f"Not found: {zip_path} (download manually from NGED portal)")
            continue

        try:
            temp_dir.mkdir(parents=True, exist_ok=True)
            shp_path = extract_shapefile_from_zip(zip_path, temp_dir)

            output_path = output_dir / output_file
            stats = convert_shapefile_to_geojson(shp_path, output_path, 'NGED', voltage)

            print_success(f"{output_file}: {stats['features']} features, {stats['size_mb']:.2f} MB")

            results.append({
                'dno': 'NGED',
                'dataset': output_file,
                **stats
            })

            shutil.rmtree(temp_dir)

        except Exception as e:
            print_error(f"Failed to process {zip_file}: {e}")

    return results

def process_other_dnos():
    """Process other DNO data (NPG, SSEN, SPEN, ENWL)"""
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}Processing Other DNOs{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    dnos = {
        'NPG': 'Northern Powergrid',
        'SSEN': 'SSE Energy Networks',
        'SPEN': 'Scottish Power Energy Networks',
        'ENWL': 'Electricity North West'
    }

    results = []

    for dno_code, dno_name in dnos.items():
        print_info(f"Checking {dno_name} ({dno_code})...")

        raw_dir = Path(f'data/dno/{dno_code.lower()}/raw')

        if not raw_dir.exists() or not any(raw_dir.iterdir()):
            print_warning(f"No data found for {dno_code}. Download manually from their portal.")
            continue

        # Look for ZIP or shapefile directly
        shp_files = list(raw_dir.rglob('*.shp'))
        zip_files = list(raw_dir.rglob('*.zip'))

        temp_dir = Path(f'data/dno/{dno_code.lower()}/temp')
        output_dir = Path('frontend/public/data')

        processed = 0

        # Process ZIP files
        for zip_file in zip_files:
            try:
                temp_dir.mkdir(parents=True, exist_ok=True)
                shp_path = extract_shapefile_from_zip(zip_file, temp_dir)

                # Try to infer voltage from filename
                filename = zip_file.stem.lower()
                if '132kv' in filename or '132' in filename:
                    voltage = '132kV'
                elif '66kv' in filename or '66' in filename:
                    voltage = '66kV'
                elif '33kv' in filename or '33' in filename:
                    voltage = '33kV'
                else:
                    voltage = None

                output_name = f"{dno_code.lower()}-{zip_file.stem}.geojson"
                output_path = output_dir / output_name

                stats = convert_shapefile_to_geojson(shp_path, output_path, dno_code, voltage)

                print_success(f"{output_name}: {stats['features']} features, {stats['size_mb']:.2f} MB")

                results.append({
                    'dno': dno_code,
                    'dataset': output_name,
                    **stats
                })

                processed += 1
                shutil.rmtree(temp_dir)

            except Exception as e:
                print_error(f"Failed to process {zip_file.name}: {e}")

        # Process direct shapefile
        for shp_file in shp_files:
            try:
                filename = shp_file.stem.lower()
                if '132kv' in filename or '132' in filename:
                    voltage = '132kV'
                elif '66kv' in filename or '66' in filename:
                    voltage = '66kV'
                elif '33kv' in filename or '33' in filename:
                    voltage = '33kV'
                else:
                    voltage = None

                output_name = f"{dno_code.lower()}-{shp_file.stem}.geojson"
                output_path = output_dir / output_name

                stats = convert_shapefile_to_geojson(str(shp_file), output_path, dno_code, voltage)

                print_success(f"{output_name}: {stats['features']} features, {stats['size_mb']:.2f} MB")

                results.append({
                    'dno': dno_code,
                    'dataset': output_name,
                    **stats
                })

                processed += 1

            except Exception as e:
                print_error(f"Failed to process {shp_file.name}: {e}")

        if processed == 0:
            print_warning(f"No processable files found for {dno_code}")

    return results

def save_conversion_report(all_results):
    """Save conversion statistics report"""
    report_path = 'data/dno/conversion_report.json'

    total_features = sum(r['features'] for r in all_results)
    total_size = sum(r['size_mb'] for r in all_results)

    report = {
        'timestamp': str(Path(__file__).stat().st_mtime),
        'total_datasets': len(all_results),
        'total_features': total_features,
        'total_size_mb': round(total_size, 2),
        'by_dno': {},
        'datasets': all_results
    }

    for result in all_results:
        dno = result['dno']
        if dno not in report['by_dno']:
            report['by_dno'][dno] = {'datasets': 0, 'features': 0, 'size_mb': 0}

        report['by_dno'][dno]['datasets'] += 1
        report['by_dno'][dno]['features'] += result['features']
        report['by_dno'][dno]['size_mb'] += result['size_mb']

    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print_success(f"Conversion report saved: {report_path}")

    return report

def main():
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}DNO Shapefile to GeoJSON Converter{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    all_results = []

    # Process each DNO
    all_results.extend(process_ukpn_data())
    all_results.extend(process_nged_data())
    all_results.extend(process_other_dnos())

    # Generate report
    if all_results:
        report = save_conversion_report(all_results)

        print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}CONVERSION SUMMARY{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

        print(f"Total datasets:  {report['total_datasets']}")
        print(f"Total features:  {report['total_features']:,}")
        print(f"Total size:      {report['total_size_mb']:.2f} MB")
        print("")

        print("By DNO:")
        for dno, stats in report['by_dno'].items():
            print(f"  {dno:6} - {stats['datasets']} datasets, {stats['features']:6,} features, {stats['size_mb']:6.2f} MB")

        print("")
        print_info("Next step: python scripts/standardize_dno_properties.py")

    else:
        print_warning("No data processed. Download DNO data first.")
        print_info("Run: python scripts/download_all_dno_network_data.py")

if __name__ == '__main__':
    main()
