#!/usr/bin/env python3
"""
Fix BMRS API calls and download operational data
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import time

BMRS_API_BASE = "https://data.elexon.co.uk/bmrs/api/v1"
DATA_DIR = Path("data/raw/operational")

def download_generation_outturn(days_back=30):
    """Download generation outturn (actual generation by fuel type)"""
    print(f"Downloading Generation Outturn (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    # Try B1620 - Actual Generation Output per Generation Unit
    url = f"{BMRS_API_BASE}/generation/outturn"
    params = {
        "from": from_date,
        "to": to_date
    }

    try:
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            output_file = DATA_DIR / f"generation_outturn_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Generation Outturn: {len(df)} records downloaded")
            return df
        else:
            print("✗ No data returned")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def download_demand_outturn(days_back=30):
    """Download demand outturn (actual demand)"""
    print(f"Downloading Demand Outturn (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    url = f"{BMRS_API_BASE}/demand/outturn"
    params = {
        "from": from_date,
        "to": to_date
    }

    try:
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            output_file = DATA_DIR / f"demand_outturn_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Demand Outturn: {len(df)} records downloaded")
            return df
        else:
            print("✗ No data returned")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def download_balancing_services(days_back=30):
    """Download balancing services volumes and prices"""
    print(f"Downloading Balancing Services (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    url = f"{BMRS_API_BASE}/balancing/settlement/system-prices"
    params = {
        "from": from_date,
        "to": to_date
    }

    try:
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            output_file = DATA_DIR / f"system_prices_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ System Prices: {len(df)} records downloaded")
            return df
        else:
            print("✗ No data returned")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def download_generation_forecast(days_back=7):
    """Download wind and solar generation forecast"""
    print(f"Downloading Wind/Solar Forecasts (last {days_back} days)...")

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    # Wind forecast
    url_wind = f"{BMRS_API_BASE}/forecast/generation/wind/peak"
    params = {
        "from": from_date,
        "to": to_date
    }

    results = []

    try:
        response = requests.get(url_wind, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            output_file = DATA_DIR / f"wind_forecast_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Wind Forecast: {len(df)} records downloaded")
            results.append(True)
        else:
            print("✗ No wind forecast data")
            results.append(False)

    except Exception as e:
        print(f"✗ Wind forecast error: {e}")
        results.append(False)

    time.sleep(1)

    # Try day-ahead wind/solar
    try:
        url_day_ahead = f"{BMRS_API_BASE}/forecast/generation/wind-and-solar/day-ahead"
        response = requests.get(url_day_ahead, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            output_file = DATA_DIR / f"wind_solar_day_ahead_{from_date}_to_{to_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Wind/Solar Day-Ahead: {len(df)} records downloaded")
            results.append(True)
        else:
            print("✗ No day-ahead data")
            results.append(False)

    except Exception as e:
        print(f"✗ Day-ahead error: {e}")
        results.append(False)

    return any(results)

def explore_bmrs_endpoints():
    """Try to discover working BMRS endpoints"""
    print("Exploring BMRS API endpoints...")

    endpoints = [
        "/generation/outturn/summary",
        "/demand/outturn/summary",
        "/datasets",
        "/generation/actual/per-type",
        "/balancing/settlement/system-prices",
    ]

    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    for endpoint in endpoints:
        url = f"{BMRS_API_BASE}{endpoint}"
        print(f"\nTrying: {endpoint}")

        try:
            # Try with date parameters
            response = requests.get(url, params={"from": from_date}, timeout=30)

            if response.status_code == 200:
                print(f"  ✓ Success (200)")
                data = response.json()
                print(f"  Response type: {type(data)}")
                if isinstance(data, list):
                    print(f"  Records: {len(data)}")
                    if len(data) > 0:
                        print(f"  Sample keys: {list(data[0].keys())[:5]}")
            else:
                print(f"  Status: {response.status_code}")

        except Exception as e:
            print(f"  ✗ Error: {e}")

def main():
    print("=" * 80)
    print("BMRS Data Download Fix")
    print("=" * 80 + "\n")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Explore endpoints first
    explore_bmrs_endpoints()
    print("\n" + "=" * 80 + "\n")

    # Try downloading data
    gen_df = download_generation_outturn(days_back=30)
    print()

    demand_df = download_demand_outturn(days_back=30)
    print()

    prices_df = download_balancing_services(days_back=30)
    print()

    forecast = download_generation_forecast(days_back=7)
    print()

    print("=" * 80)
    print("Download Summary")
    print("=" * 80)
    print(f"Generation: {'✓' if gen_df is not None else '✗'}")
    print(f"Demand: {'✓' if demand_df is not None else '✗'}")
    print(f"Prices: {'✓' if prices_df is not None else '✗'}")
    print(f"Forecasts: {'✓' if forecast else '✗'}")

if __name__ == "__main__":
    main()
