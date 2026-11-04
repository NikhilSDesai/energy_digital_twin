#!/usr/bin/env python3
"""
Master script to download all UK energy data
Orchestrates downloads from NESO, BMRS, and DNOs
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_script(script_name):
    """Run a Python script and return success status"""
    print(f"\n{'=' * 80}")
    print(f"Running: {script_name}")
    print('=' * 80)

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"✓ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {script_name} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ Error running {script_name}: {e}")
        return False

def main():
    print("=" * 80)
    print("UK ENERGY DIGITAL TWIN - DATA ACQUISITION")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    scripts_dir = Path(__file__).parent
    results = {}

    # List of download scripts to run
    scripts = [
        "download_neso_data.py",
        "download_bmrs_data.py",
        "download_dno_data.py"
    ]

    # Run each script
    for script in scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            results[script] = run_script(script_path)
        else:
            print(f"✗ Script not found: {script}")
            results[script] = False

    # Summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)

    for script, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{script:30s} {status}")

    successful = sum(1 for s in results.values() if s)
    total = len(results)

    print(f"\nCompleted: {successful}/{total} scripts successful")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    # Data directory summary
    data_dir = Path("data/raw")
    if data_dir.exists():
        print("Downloaded files by category:")
        for subdir in ["infrastructure", "demand", "queue", "operational"]:
            subdir_path = data_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*"))
                print(f"  {subdir:20s}: {len(files)} files")

if __name__ == "__main__":
    main()
