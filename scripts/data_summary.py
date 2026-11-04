#!/usr/bin/env python3
"""
Generate summary of all downloaded data
"""

import pandas as pd
from pathlib import Path
import json

DATA_DIR = Path("data/raw")

def summarize_tec_register():
    """Summarize the connection queue (TEC Register)"""
    print("=" * 80)
    print("TEC REGISTER (CONNECTION QUEUE)")
    print("=" * 80)

    tec_file = list(DATA_DIR.glob("queue/tec_register*.csv"))
    if not tec_file:
        print("✗ Not found")
        return

    df = pd.read_csv(tec_file[0])

    print(f"\nTotal Projects: {len(df):,}")
    print(f"Columns: {list(df.columns)}\n")

    # Key statistics
    if 'MW Connected' in df.columns:
        total_mw = df['MW Connected'].sum()
        print(f"Total Capacity: {total_mw:,.0f} MW")

    if 'Stage' in df.columns:
        print("\nProjects by Stage:")
        print(df['Stage'].value_counts().head(10))

    if 'Connection Site' in df.columns:
        print(f"\nUnique Connection Sites: {df['Connection Site'].nunique():,}")

    # Sample records
    print("\nSample Projects:")
    print(df.head(3).to_string())

def summarize_historic_demand():
    """Summarize historic demand data"""
    print("\n" + "=" * 80)
    print("HISTORIC DEMAND DATA")
    print("=" * 80)

    demand_files = list(DATA_DIR.glob("demand/Historic_Demand_Data*.csv"))
    print(f"\nYears Available: {len(demand_files)}")

    if demand_files:
        # Load one file to show structure
        sample_file = sorted(demand_files)[0]
        df = pd.read_csv(sample_file, nrows=1000)

        print(f"\nSample File: {sample_file.name}")
        print(f"Columns: {list(df.columns)}")
        print(f"Records (sample): {len(df):,}")

        # Show date range
        if 'SETTLEMENT_DATE' in df.columns:
            print(f"Date Range: {df['SETTLEMENT_DATE'].min()} to {df['SETTLEMENT_DATE'].max()}")

def summarize_gsp_boundaries():
    """Summarize GSP boundaries"""
    print("\n" + "=" * 80)
    print("GSP BOUNDARIES (GEOGRAPHIC DATA)")
    print("=" * 80)

    gsp_file = list(DATA_DIR.glob("infrastructure/gsp_boundaries*.geojson"))
    if not gsp_file:
        print("✗ Not found")
        return

    with open(gsp_file[0], 'r') as f:
        geojson = json.load(f)

    features = geojson.get('features', [])
    print(f"\nTotal GSP Regions: {len(features)}")

    if features:
        print("\nSample GSP:")
        sample = features[0]
        props = sample.get('properties', {})
        print(f"  Name: {props.get('GSP_NAME', 'N/A')}")
        print(f"  ID: {props.get('GSP_ID', 'N/A')}")
        print(f"  Properties: {list(props.keys())}")

def summarize_nged_queue():
    """Summarize NGED connection queue"""
    print("\n" + "=" * 80)
    print("NGED CONNECTION QUEUE")
    print("=" * 80)

    nged_file = list(DATA_DIR.glob("queue/nged_NGED_Connections_Reform*.csv"))
    if not nged_file:
        print("✗ Not found")
        return

    df = pd.read_csv(nged_file[0])

    print(f"\nTotal Applications: {len(df):,}")
    print(f"Columns: {list(df.columns)[:10]}...")

    if 'Capacity (MVA)' in df.columns:
        total_capacity = df['Capacity (MVA)'].sum()
        print(f"\nTotal Capacity: {total_capacity:,.0f} MVA")

    if 'Technology Type' in df.columns:
        print("\nApplications by Technology:")
        print(df['Technology Type'].value_counts().head(10))

def summarize_operational_data():
    """Summarize BMRS operational data"""
    print("\n" + "=" * 80)
    print("OPERATIONAL DATA (BMRS)")
    print("=" * 80)

    # Generation data
    gen_file = list(DATA_DIR.glob("operational/generation_summary*.csv"))
    if gen_file:
        df = pd.read_csv(gen_file[0])
        print(f"\nGeneration Data: {len(df):,} records")

        if 'fuelType' in df.columns:
            print(f"Fuel Types: {df['fuelType'].nunique()}")
            print("\nGeneration by Fuel Type:")
            print(df.groupby('fuelType')['generation'].sum().sort_values(ascending=False).head(10))

    # Demand data
    demand_file = list(DATA_DIR.glob("operational/demand_summary*.csv"))
    if demand_file:
        df = pd.read_csv(demand_file[0])
        print(f"\nDemand Data: {len(df):,} records")
        print(f"Columns: {list(df.columns)}")

def main():
    print("=" * 80)
    print("UK ENERGY DIGITAL TWIN - DATA SUMMARY")
    print("=" * 80 + "\n")

    # File count by category
    print("Downloaded Files by Category:")
    for category in ['infrastructure', 'demand', 'queue', 'operational']:
        cat_dir = DATA_DIR / category
        if cat_dir.exists():
            files = list(cat_dir.glob("*"))
            print(f"  {category:20s}: {len(files):3d} files")

    print()

    # Detailed summaries
    summarize_tec_register()
    summarize_historic_demand()
    summarize_gsp_boundaries()
    summarize_nged_queue()
    summarize_operational_data()

    print("\n" + "=" * 80)
    print("DATA ACQUISITION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
