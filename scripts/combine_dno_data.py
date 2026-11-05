#!/usr/bin/env python3
"""
Combine all DNO GeoJSON files into unified datasets

Creates combined files for:
- all-dnos-132kv-overhead-lines.geojson
- all-dnos-66kv-overhead-lines.geojson
- all-dnos-33kv-overhead-lines.geojson
- all-dnos-substations.geojson
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

def load_geojson(file_path):
    """Load GeoJSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_geojson(data, file_path):
    """Save GeoJSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def combine_geojson_files(file_list, output_path):
    """Combine multiple GeoJSON files into one"""
    combined_features = []
    source_info = []

    for file_path in file_list:
        if not file_path.exists():
            continue

        try:
            data = load_geojson(file_path)

            if data.get('type') == 'FeatureCollection':
                features = data.get('features', [])
                combined_features.extend(features)

                source_info.append({
                    'file': file_path.name,
                    'features': len(features)
                })

                print_info(f"  Added {len(features):,} features from {file_path.name}")

        except Exception as e:
            print_warning(f"  Failed to load {file_path.name}: {e}")

    if not combined_features:
        return None

    # Create combined FeatureCollection
    combined = {
        'type': 'FeatureCollection',
        'features': combined_features,
        'metadata': {
            'combined_from': source_info,
            'total_features': len(combined_features)
        }
    }

    # Save
    save_geojson(combined, output_path)

    file_size = output_path.stat().st_size / (1024 * 1024)

    print_success(f"Combined file: {output_path.name} ({len(combined_features):,} features, {file_size:.2f} MB)")

    return {
        'output': output_path.name,
        'features': len(combined_features),
        'size_mb': file_size,
        'sources': source_info
    }

def main():
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}Combine DNO Data{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    data_dir = Path('frontend/public/data')

    if not data_dir.exists():
        print_warning("Data directory not found")
        sys.exit(1)

    results = []

    # Combine 132kV overhead lines
    print(f"\n{Colors.BOLD}132kV Overhead Lines:{Colors.ENDC}")
    files_132 = [
        data_dir / f"{dno}-132kv-overhead-lines.geojson"
        for dno in ['ukpn', 'nged', 'npg', 'ssen', 'spen', 'enwl']
    ]
    result_132 = combine_geojson_files(
        [f for f in files_132 if f.exists()],
        data_dir / 'all-dnos-132kv-overhead-lines.geojson'
    )
    if result_132:
        results.append(result_132)

    # Combine 66kV overhead lines
    print(f"\n{Colors.BOLD}66kV Overhead Lines:{Colors.ENDC}")
    files_66 = [
        data_dir / f"{dno}-66kv-overhead-lines.geojson"
        for dno in ['ukpn', 'nged', 'npg', 'ssen', 'spen', 'enwl']
    ]
    result_66 = combine_geojson_files(
        [f for f in files_66 if f.exists()],
        data_dir / 'all-dnos-66kv-overhead-lines.geojson'
    )
    if result_66:
        results.append(result_66)

    # Combine 33kV overhead lines
    print(f"\n{Colors.BOLD}33kV Overhead Lines:{Colors.ENDC}")
    files_33 = [
        data_dir / f"{dno}-33kv-overhead-lines.geojson"
        for dno in ['ukpn', 'nged', 'npg', 'ssen', 'spen', 'enwl']
    ]
    result_33 = combine_geojson_files(
        [f for f in files_33 if f.exists()],
        data_dir / 'all-dnos-33kv-overhead-lines.geojson'
    )
    if result_33:
        results.append(result_33)

    # Combine substations
    print(f"\n{Colors.BOLD}Substations:{Colors.ENDC}")
    files_subs = [
        data_dir / f"{dno}-substations.geojson"
        for dno in ['ukpn', 'nged', 'npg', 'ssen', 'spen', 'enwl']
    ]
    result_subs = combine_geojson_files(
        [f for f in files_subs if f.exists()],
        data_dir / 'all-dnos-substations.geojson'
    )
    if result_subs:
        results.append(result_subs)

    # Summary
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}SUMMARY{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

    if results:
        total_features = sum(r['features'] for r in results)
        total_size = sum(r['size_mb'] for r in results)

        print(f"Combined files:   {len(results)}")
        print(f"Total features:   {total_features:,}")
        print(f"Total size:       {total_size:.2f} MB")
        print("")

        for result in results:
            print(f"  {result['output']:45} {result['features']:7,} features, {result['size_mb']:6.2f} MB")

        print("")
        print_success("Data combination complete!")
        print("")
        print_info("Next steps:")
        print("  1. Update frontend/public/app.js to use combined files")
        print("  2. See: scripts/app_js_update_instructions.txt")

        # Save combination report
        report_path = data_dir / 'combination_report.json'
        with open(report_path, 'w') as f:
            json.dump({
                'combined_files': results,
                'total_features': total_features,
                'total_size_mb': round(total_size, 2)
            }, f, indent=2)

        print_info(f"Report saved: {report_path}")

    else:
        print_warning("No files combined. Process DNO data first:")
        print("  1. python scripts/download_all_dno_network_data.py")
        print("  2. python scripts/convert_dno_shapefiles.py")
        print("  3. python scripts/standardize_dno_properties.py")

if __name__ == '__main__':
    main()
