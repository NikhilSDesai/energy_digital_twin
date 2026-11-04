#!/usr/bin/env python3
"""
Download BMRS (Balancing Mechanism Reporting Service) data
Includes: Generation, Demand, Prices, Fuel Mix
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import time

# BMRS API Base
BMRS_API_BASE = "https://data.elexon.co.uk/bmrs/api/v1"
DATA_DIR = Path("data/raw/operational")

def download_actual_load(days_back=90):
    """Download actual total load data"""
    print(f"Downloading Actual Total Load (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    url = f"{BMRS_API_BASE}/datasets/ATL"
    params = {
        "publishDateTimeFrom": from_date,
        "publishDateTimeTo": to_date,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            df = pd.DataFrame(data["data"])

            output_file = DATA_DIR / f"actual_load_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Actual Load downloaded: {len(df)} records, {output_file}")
            return df
        else:
            print("✗ No data returned for Actual Load")
            return None
    except Exception as e:
        print(f"✗ Error downloading Actual Load: {e}")
        return None

def download_generation_by_fuel(days_back=90):
    """Download generation by fuel type"""
    print(f"Downloading Generation by Fuel Type (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    url = f"{BMRS_API_BASE}/datasets/FUELHH"
    params = {
        "publishDateTimeFrom": from_date,
        "publishDateTimeTo": to_date,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            df = pd.DataFrame(data["data"])

            output_file = DATA_DIR / f"generation_fuel_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Generation by Fuel downloaded: {len(df)} records, {output_file}")
            return df
        else:
            print("✗ No data returned for Generation by Fuel")
            return None
    except Exception as e:
        print(f"✗ Error downloading Generation by Fuel: {e}")
        return None

def download_system_prices(days_back=90):
    """Download system buy/sell prices"""
    print(f"Downloading System Prices (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    url = f"{BMRS_API_BASE}/datasets/DISEBSP"
    params = {
        "settlementDateFrom": from_date,
        "settlementDateTo": to_date,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            df = pd.DataFrame(data["data"])

            output_file = DATA_DIR / f"system_prices_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ System Prices downloaded: {len(df)} records, {output_file}")
            return df
        else:
            print("✗ No data returned for System Prices")
            return None
    except Exception as e:
        print(f"✗ Error downloading System Prices: {e}")
        return None

def download_wind_solar_forecast(days_back=30):
    """Download wind and solar forecast vs actual"""
    print(f"Downloading Wind/Solar Forecast (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    # Wind forecast
    url_wind = f"{BMRS_API_BASE}/datasets/WINDFOR"
    params = {
        "publishDateTimeFrom": from_date,
        "publishDateTimeTo": to_date,
        "format": "json"
    }

    try:
        response = requests.get(url_wind, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            df = pd.DataFrame(data["data"])
            output_file = DATA_DIR / f"wind_forecast_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Wind Forecast downloaded: {len(df)} records")

        time.sleep(1)

        # Solar forecast
        url_solar = f"{BMRS_API_BASE}/datasets/SOLARFOR"
        response = requests.get(url_solar, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            df = pd.DataFrame(data["data"])
            output_file = DATA_DIR / f"solar_forecast_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Solar Forecast downloaded: {len(df)} records")

        return True
    except Exception as e:
        print(f"✗ Error downloading Wind/Solar Forecast: {e}")
        return None

def get_available_datasets():
    """List available BMRS datasets"""
    print("Fetching available BMRS datasets...")

    url = f"{BMRS_API_BASE}/datasets"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        datasets = response.json()

        output_file = DATA_DIR.parent / "bmrs_datasets_list.txt"
        with open(output_file, 'w') as f:
            f.write(f"BMRS Available Datasets ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
            f.write("=" * 80 + "\n\n")

            if isinstance(datasets, list):
                for dataset in sorted(datasets, key=lambda x: x.get('name', '')):
                    name = dataset.get('name', 'Unknown')
                    desc = dataset.get('description', 'No description')
                    f.write(f"{name}: {desc}\n")

        print(f"✓ Dataset list saved to: {output_file}")
        return datasets
    except Exception as e:
        print(f"✗ Error fetching datasets: {e}")
        return None

def main():
    print("=" * 80)
    print("BMRS Operational Data Download Script")
    print("=" * 80 + "\n")

    # Create output directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Get available datasets
    get_available_datasets()
    print()

    # Download key operational datasets
    load_df = download_actual_load(days_back=90)
    print()

    fuel_df = download_generation_by_fuel(days_back=90)
    print()

    prices_df = download_system_prices(days_back=90)
    print()

    wind_solar = download_wind_solar_forecast(days_back=30)
    print()

    print("=" * 80)
    print("Download Summary")
    print("=" * 80)
    print(f"Actual Load: {'✓' if load_df is not None else '✗'}")
    print(f"Generation by Fuel: {'✓' if fuel_df is not None else '✗'}")
    print(f"System Prices: {'✓' if prices_df is not None else '✗'}")
    print(f"Wind/Solar: {'✓' if wind_solar else '✗'}")
    print()

if __name__ == "__main__":
    main()
