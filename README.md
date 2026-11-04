# UK Energy Grid Digital Twin

A spatial digital twin platform for the UK energy grid, focused on:
1. Running simulations on energy infrastructure
2. Forecasting future energy demand (sustainable tech, data centers)
3. Understanding pain points in interconnection queues

## Project Status

**Phase:** Data Acquisition ✅
**Region:** United Kingdom (Great Britain)
**Data Coverage:** 54 MB, 33 files

## Quick Start

```bash
# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download all available data
python scripts/download_all.py

# View data summary
python scripts/data_summary.py
```

## Data Inventory

See [DATA_INVENTORY.md](DATA_INVENTORY.md) for complete data documentation.

**Key Datasets:**
- **Connection Queue:** 2,219 projects, 81.7 GW (TEC Register)
- **Historic Demand:** 26 years (2001-2026)
- **Geographic Data:** 329 GSP boundaries
- **Operational:** Real-time generation and demand

## Why UK?

After comprehensive research comparing US ISOs (CAISO, ERCOT, PJM) with UK:

**UK Advantages:**
- ✅ Superior distribution network data (585k+ substations)
- ✅ Publicly available smart meter data (feeder-level)
- ✅ Twice-weekly queue updates
- ✅ No authentication required for APIs
- ✅ Exceptional planning framework (FES, DFES)

**UK Limitations:**
- ⚠️ No locational marginal pricing (single price zone)
- ⚠️ Limited historical operational data (2 years vs 17+ for CAISO)

## Use Cases

### 1. Infrastructure Simulation
Model energy network behavior:
- Power flow analysis
- Capacity constraint identification
- Renewable integration scenarios
- Network reinforcement planning

**Data Available:**
- Connection points (1,259 sites)
- Generation capacity by technology
- GSP-level network topology
- Real-time generation mix

### 2. Demand Forecasting
Predict future energy demand:
- Historical trends (26 years)
- Embedded generation impact
- Data center growth (50 GW requested)
- Electrification scenarios (EV, heat pumps)

**Data Available:**
- Half-hourly demand (2001-2026)
- Interconnector flows
- Connection queue (future projects)
- Embedded wind/solar generation

### 3. Queue Analysis
Understand interconnection bottlenecks:
- 741 GW in transmission queue
- 1M+ distribution applications
- Gate-based reform process
- Timeline and constraint analysis

**Data Available:**
- TEC Register (transmission)
- NGED queue (distribution)
- Queue stages and status
- Connection site mapping

## Project Structure

```
energy_dt/
├── data/
│   ├── raw/              # Downloaded data
│   │   ├── infrastructure/
│   │   ├── demand/
│   │   ├── queue/
│   │   └── operational/
│   └── processed/        # Cleaned data
├── scripts/
│   ├── download_all.py   # Master download script
│   ├── download_neso_data.py
│   ├── download_bmrs_data.py
│   ├── download_dno_data.py
│   └── data_summary.py
├── docs/                 # Research and documentation
├── requirements.txt
├── DATA_INVENTORY.md
└── README.md
```

## Data Sources

### Primary APIs

1. **NESO (National Energy System Operator)**
   - URL: https://www.neso.energy/data-portal
   - API: https://api.neso.energy/api/3/action
   - Data: TEC Register, GSP boundaries, historic demand
   - Auth: None required

2. **BMRS (Balancing Mechanism Reporting Service)**
   - URL: https://data.elexon.co.uk/bmrs/api/v1
   - Data: Generation, demand, system prices
   - Auth: None required

3. **National Grid Electricity Distribution**
   - URL: https://connecteddata.nationalgrid.co.uk
   - Data: Connection queues, network data
   - Auth: None required

### Additional Sources
- UK Power Networks: Distribution data
- SSEN: Smart meter data
- Northern Powergrid: Capacity heat maps
- Ofgem: Regulatory data

## Next Steps

### Immediate (Week 1-2)
- [ ] Download 2-year BMRS operational history
- [ ] Add UKPN distribution network data
- [ ] Get transmission line shapefiles
- [ ] Download FES 2025 scenarios

### Short-term (Weeks 3-4)
- [ ] Set up PostGIS database
- [ ] ETL pipeline for regular updates
- [ ] Data quality checks and validation
- [ ] Initial exploratory analysis

### Medium-term (Weeks 5-8)
- [ ] Build network topology model
- [ ] Create baseline demand forecast
- [ ] Queue bottleneck analysis
- [ ] Web-based visualization prototype

## Research Documentation

Comprehensive research on data availability across US and UK energy markets documented in conversation history. Key findings:

- **Best US ISO:** CAISO (for locational pricing, deep history)
- **Best UK Region:** London/SE (UKPN coverage)
- **Overall Best:** UK for physical network modeling
- **Data Quality:** UK = 65% complete, CAISO = 75% complete

## Key Metrics

**Connection Queue:**
- 741 GW total capacity in queue
- 2,219 transmission projects
- 1M+ distribution applications
- 1,259 unique connection sites

**Data Center Impact:**
- 50 GW requested connections
- 140 proposed projects
- 5 TWh → 26 TWh by 2030

**Historical Coverage:**
- Demand: 2001-2026 (26 years)
- Operational: 2024-2026 (limited)
- Geographic: Current snapshot

## Technology Stack

**Current:**
- Python 3.x
- pandas, geopandas
- requests (API client)

**Planned:**
- PostgreSQL + PostGIS (spatial database)
- Pandapower (power systems simulation)
- FastAPI (web services)
- Mapbox/Deck.gl (visualization)

## Contributing

This is a personal research project. For questions or collaboration:
- Review DATA_INVENTORY.md for data documentation
- Check scripts/ for data acquisition code
- See conversation history for research methodology

## License

Data sources have various licenses:
- NESO: Open Data License (with attribution)
- BMRS: BSC Open Data License
- NGED: Check portal for specific terms

## Acknowledgments

Data provided by:
- National Energy System Operator (NESO)
- Elexon (BMRS)
- National Grid Electricity Distribution
- UK Power Networks
- SSEN Distribution

Research methodology based on comprehensive market analysis of US ISOs and UK energy data landscape.

---

**Last Updated:** November 3, 2026
**Version:** 0.1.0 (Data Acquisition Phase)
