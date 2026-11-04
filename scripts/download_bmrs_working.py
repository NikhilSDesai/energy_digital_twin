#!/usr/bin/env python3
"""
Download BMRS data using working endpoints
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

BMRS_API_BASE = "https://data.elexon.co.uk/bmrs/api/v1"
DATA_DIR = Path("data/raw/operational")

def download_generation_summary():
    """Download generation outturn summary (working endpoint)"""
    print("Downloading Generation Outturn Summary...")

    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    url = f"{BMRS_API_BASE}/generation/outturn/summary"
    params = {"from": from_date}

    try:
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            # Flatten nested data structure
            records = []
            for entry in data:
                start_time = entry.get('startTime')
                settlement_period = entry.get('settlementPeriod')

                for fuel_data in entry.get('data', []):
                    record = {
                        'startTime': start_time,
                        'settlementPeriod': settlement_period,
                        **fuel_data
                    }
                    records.append(record)

            df = pd.DataFrame(records)
            output_file = DATA_DIR / f"generation_summary_{from_date}_to_now.csv"
            df.to_csv(output_file, index=False)

            print(f"✓ Generation Summary: {len(df)} records")
            print(f"  Time range: {df['startTime'].min()} to {df['startTime'].max()}")
            print(f"  Fuel types: {df['fuelType'].nunique() if 'fuelType' in df.columns else 'N/A'}")
            return df
        else:
            print("✗ No data returned")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def download_demand_summary():
    """Try to get demand data with correct parameters"""
    print("Downloading Demand Summary...")

    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Try different demand endpoints
    endpoints = [
        "/demand/outturn/summary",
        "/demand/summary",
        "/demand/actual",
    ]

    for endpoint in endpoints:
        url = f"{BMRS_API_BASE}{endpoint}"
        print(f"  Trying: {endpoint}")

        try:
            # Try without date first
            response = requests.get(url, timeout=60)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    output_file = DATA_DIR / f"demand_summary_recent.csv"
                    df.to_csv(output_file, index=False)
                    print(f"  ✓ Demand data: {len(df)} records")
                    return df

            # Try with from parameter
            response = requests.get(url, params={"from": from_date}, timeout=60)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    output_file = DATA_DIR / f"demand_summary_{from_date}_to_now.csv"
                    df.to_csv(output_file, index=False)
                    print(f"  ✓ Demand data: {len(df)} records")
                    return df

        except Exception as e:
            print(f"  ✗ {e}")
            continue

    print("✗ Could not fetch demand data")
    return None

def main():
    print("=" * 80)
    print("BMRS Data Download (Working Endpoints)")
    print("=" * 80 + "\n")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    gen_df = download_generation_summary()
    print()

    demand_df = download_demand_summary()
    print()

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Generation: {'✓' if gen_df is not None else '✗'}")
    print(f"Demand: {'✓' if demand_df is not None else '✗'}")

if __name__ == "__main__":
    main()
