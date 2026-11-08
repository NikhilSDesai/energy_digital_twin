# UK Energy Grid Digital Twin

**Live Application**: https://uk-energy-digital-twin.vercel.app

Interactive visualization of the UK's electricity infrastructure - transmission networks, distribution systems, power generation assets, and substations.

---

## 🎯 Overview

A comprehensive digital twin mapping the UK's energy infrastructure with:
- **1,212** transmission lines (400kV, 275kV, 220kV, DC)
- **2,587** power generation sites (64.4 GW capacity)
- **5,584** total infrastructure features
- **35%** UK coverage and growing

## 🚀 Quick Start

### View the Application
Visit: https://uk-energy-digital-twin.vercel.app

### Run Locally

```bash
# Start development server
cd frontend/public
python3 -m http.server 8000

# Open browser
open http://localhost:8000
```

## 📊 Current Data Coverage

| Layer | Coverage | Features | Source |
|-------|----------|----------|--------|
| **Transmission** | 100% UK | 1,212 lines | OpenStreetMap |
| **Distribution** | London, SE, East | 842+ lines | UKPN |
| **Power Plants** | 100% UK | 2,587 sites | UK Energy Generation Map |
| **Substations** | Multiple regions | 590+ sites | OSM, UKPN, NGED |
| **DNO Boundaries** | Partial | 197 areas | UKPN, NGED, SPEN |
| **Buildings** | 100% UK | 29.5M footprints | Overture Maps (processing) |

## 🗺️ Geographic Coverage

### Distribution Networks (132-33kV)
- ✅ **UKPN**: London, South East, East England (25% UK)
- ✅ **NGED**: South Wales primary substations
- ✅ **SPEN**: License area boundaries (Scotland, NW England)
- ⏳ **SSEN, NPG, ENWL**: Coming soon

### Transmission Network
- ✅ Complete UK coverage (400kV, 275kV, 220kV, DC interconnectors)

### Power Generation
- ✅ Complete UK coverage (all technologies, all regions)

## 🛠️ Technology Stack

**Frontend:**
- Mapbox GL JS (v3.0.1)
- Vanilla JavaScript
- Dark theme optimized UI

**Data Processing:**
- Python 3.x
- GeoPandas, Shapely
- Tippecanoe (vector tiles)
- GDAL/OGR

**Deployment:**
- Vercel (auto-deploy from main branch)
- GitHub repository

## 📁 Project Structure

```
energy_dt/
├── frontend/           # Web application
│   └── public/
│       ├── app.js     # Main application logic
│       ├── index.html # UI
│       └── data/      # GeoJSON datasets
├── scripts/           # Data processing scripts
├── data/             # Source data and processing
│   ├── processed/    # Processed GeoJSON
│   └── official_sources/ # DNO downloads
├── docs/             # Documentation
└── README.md         # This file
```

## 📚 Documentation

All detailed documentation is in the `docs/` folder:

- **[UI Design Plan](docs/UI_DESIGN_PLAN.md)** - Planned UI redesign with dual sidebars
- **[Layer Analysis](docs/LAYER_ANALYSIS.md)** - Complete infrastructure categorization
- **[Street Level Roadmap](docs/STREET_LEVEL_ROADMAP.md)** - Path to household-level detail
- **[DNO Integration Report](docs/DNO_INTEGRATION_REPORT.md)** - Distribution network data status
- **[Building Tiles Status](docs/BUILDING_TILES_STATUS.md)** - Building footprint optimization
- **[Session Integration Summary](docs/SESSION_INTEGRATION_SUMMARY.md)** - Recent updates
- **[Comprehensive Status Report](docs/COMPREHENSIVE_STATUS_REPORT.md)** - Full project status

## 🎨 Features

### Interactive Map
- Progressive zoom disclosure (different data at different zoom levels)
- Voltage-based color coding for transmission lines
- Technology-based color coding for power plants
- Clustered visualization for dense data
- Interactive popups with infrastructure details

### Data Layers
- Transmission lines (400-220kV)
- Distribution networks (132-33kV)
- Power generation (wind, solar, gas, nuclear, hydro, biomass, battery)
- Substations (transmission, primary, distribution)
- Network regions (GSP, DNO boundaries)
- Building footprints (in progress)

### Visualization
- Dark theme for energy infrastructure
- Mapbox satellite and street basemaps
- Real-time interaction with 5,584 features
- No performance degradation

## 🔄 Recent Updates

**2024-11-07:**
- ✅ Added 2,587 UK power plants (64.4 GW)
- ✅ Integrated South Wales primary substations (195 areas)
- ✅ Added SPEN license boundaries
- ✅ Removed sidebar for UI redesign
- ✅ Building tiles processing (29.5M footprints)

## 🎯 Roadmap

### Short Term
- [ ] Implement new dual sidebar UI
- [ ] Complete building footprint tiles
- [ ] Add NGED 11kV distribution network
- [ ] Add SSEN network data

### Medium Term
- [ ] Complete all 6 DNO coverage (100% UK)
- [ ] Add LV (low voltage) networks
- [ ] Add connection queue visualization (TEC Register)
- [ ] Implement spatial analysis tools

### Long Term
- [ ] Real-time generation data
- [ ] Demand estimation and forecasting
- [ ] Network constraint analysis
- [ ] Carbon intensity visualization

## 📊 Data Sources

- **OpenStreetMap**: Transmission network, substations
- **UKPN**: Distribution network (London, SE, East)
- **NGED**: South Wales primary substations
- **SPEN**: License area boundaries
- **Overture Maps**: Building footprints (29.5M)
- **UK Energy Generation Map**: Power plants
- **National Grid ESO**: Grid supply points, TEC register

## 🤝 Contributing

This is a personal project, but data contributions are welcome:
- Report data errors or missing infrastructure
- Suggest new data layers or visualizations
- Provide access to official DNO datasets

## 📄 License

MIT License - See LICENSE file for details

Data sources have their own licenses:
- OSM data: ODbL (Open Database License)
- Overture Maps: ODbL
- DNO data: Various open data licenses

## 🔗 Links

- **Live App**: https://uk-energy-digital-twin.vercel.app
- **Repository**: https://github.com/NikhilSDesai/energy_digital_twin
- **Vercel**: Auto-deploys from main branch

---

**Built with Claude Code** • Last updated: 2024-11-07
