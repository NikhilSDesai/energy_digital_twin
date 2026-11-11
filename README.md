# UK Energy Grid Digital Twin

**Live Application**: https://uk-energy-digital-twin.vercel.app

Interactive visualization of the UK's electricity infrastructure - transmission networks, distribution systems, power generation assets, substations, and network constraints.

---

## 🎯 Overview

A comprehensive digital twin mapping the UK's energy infrastructure with:
- **1,212** transmission lines (400kV, 275kV, 220kV, DC interconnectors)
- **34** transmission constraint boundaries (B6, B7, B8, etc.)
- **2,587** power generation sites (64.4 GW capacity)
- **29.5M** building footprints (vector tiles)
- **590+** substations across multiple DNOs
- Modern purple/blue-purple (BuPu) color scheme

## 🚀 Quick Start

### View the Application
Visit: https://uk-energy-digital-twin.vercel.app

### Run Locally

```bash
# Clone repository
git clone https://github.com/NikhilSDesai/energy_digital_twin.git
cd energy_digital_twin

# Start development server
cd frontend/public
python3 -m http.server 8001

# Open browser
open http://localhost:8001
```

## 🎨 Visual Design

### Color Scheme
- **Electric Blue (#00D9FF)**: Transmission & distribution lines (core grid infrastructure)
- **Purple (#9D4EDD)**: Substations, GSP boundaries
- **BuPu Gradient**: Power plants and connection queue (light blue → dark purple)
- **White Dashed Lines**: Transmission constraint boundaries
- **Black Background**: High-contrast dark theme

### UI Features
- **Left Sidebar**: Hierarchical layer controls with 7 categories
- **Collapsible Categories**: Transmission, Distribution, Generation, Queue, Substations, Regions, Buildings
- **Interactive Popups**: Blue gradient speech bubbles with dotted borders
- **Progressive Disclosure**: Different layers visible at different zoom levels

## 📊 Current Data Coverage

| Layer | Coverage | Features | Source |
|-------|----------|----------|--------|
| **Transmission Lines** | 100% UK | 1,212 lines | OpenStreetMap |
| **Transmission Boundaries** | 100% UK | 34 boundaries | NESO ETYS 2024 |
| **Distribution (132-33kV)** | London, SE, East | 842+ lines | UKPN |
| **Power Plants** | 100% UK | 2,587 sites | UK Energy Generation Map |
| **Substations** | Multiple regions | 590+ sites | OSM, UKPN, NGED |
| **DNO Boundaries** | Partial | 197 areas | UKPN, NGED, SPEN |
| **Buildings** | 100% UK | 29.5M footprints | Overture Maps |
| **Connection Queue** | 100% UK | 2,219 projects | NESO TEC Register |
| **GSP Regions** | 100% UK | 329 regions | NESO |

## 🗺️ Geographic Coverage

### Transmission Network (275-400kV)
- ✅ **Complete UK coverage**: All 400kV, 275kV, 220kV, and DC interconnector lines
- ✅ **34 constraint boundaries**: Official NESO ETYS boundaries (B6, B7, B8, SC1, NW1, EC5, etc.)

### Distribution Networks (132-33kV)
- ✅ **UKPN**: London, South East, East England (25% UK) - 132kV, 66kV, 33kV
- ✅ **NGED**: South Wales primary substations (195 areas)
- ✅ **SPEN**: License area boundaries (Scotland, NW England)
- ⏳ **SSEN, NPG, ENWL**: Coming soon

### Power Generation
- ✅ **Complete UK coverage**: All technologies (wind, solar, gas, nuclear, hydro, biomass, battery, tidal)
- ✅ **2,587 generation sites**: 64.4 GW total capacity
- ✅ **Purple/blue-purple palette**: Technology-based color coding

### Building Footprints
- ✅ **29.5 million buildings**: Complete UK coverage
- ✅ **Vector tiles**: Optimized with Tippecanoe (zoom 17-20)
- ✅ **35GB dataset**: Served via tileserver-gl-light

## 🛠️ Technology Stack

### Frontend
- **MapLibre GL JS** (v3.6.2) - Open-source mapping library
- **MapTiler Backdrop Dark** - Clean terrain basemap (no labels/borders)
- **Vanilla JavaScript** - No frameworks, pure performance
- **Purple/BuPu color scheme** - ColorBrewer-inspired palette

### Data Processing
- **Python 3.12** - Data processing and conversion
- **GeoPandas, Shapely** - Spatial data manipulation
- **Tippecanoe** - Vector tile generation (29.5M buildings → 35GB .mbtiles)
- **GDAL/OGR** - Format conversion (Shapefile → GeoJSON)
- **tileserver-gl-light** - Vector tile serving (localhost:8080)

### Deployment
- **Vercel** - Auto-deploy from main branch
- **GitHub** - Version control and collaboration
- **Continuous Integration** - Automatic deployment on push

## 📁 Project Structure

```
energy_dt/
├── frontend/              # Web application
│   └── public/
│       ├── app.js        # Main application logic (MapLibre + layers)
│       ├── index.html    # UI with sidebar, popups, styling
│       ├── config.js     # MapTiler API key (gitignored)
│       └── data/         # GeoJSON datasets (publicly served)
├── scripts/              # Data processing pipeline
│   ├── download_*.py     # Data acquisition scripts
│   ├── convert_*.py      # Format conversion
│   ├── process_*.py      # Data cleaning & optimization
│   └── optimize_buildings.py  # Tippecanoe vector tiles
├── data/                 # Source data and processing
│   ├── raw/             # Downloaded source files
│   ├── processed/       # Processed GeoJSON (gitignored)
│   └── official_sources/ # DNO data downloads
├── docs/                # Documentation
└── venv/               # Python virtual environment
```

## 📚 Documentation

Comprehensive documentation in `docs/` folder:

- **[UI Design Plan](docs/UI_DESIGN_PLAN.md)** - Dual sidebar design specifications
- **[Layer Analysis](docs/LAYER_ANALYSIS.md)** - Complete infrastructure categorization
- **[Street Level Roadmap](docs/STREET_LEVEL_ROADMAP.md)** - Path to household-level detail
- **[DNO Integration Report](docs/DNO_INTEGRATION_REPORT.md)** - Distribution network data status
- **[Building Tiles Status](docs/BUILDING_TILES_STATUS.md)** - 29.5M building optimization
- **[Session Integration Summary](docs/SESSION_INTEGRATION_SUMMARY.md)** - Recent updates
- **[Comprehensive Status Report](docs/COMPREHENSIVE_STATUS_REPORT.md)** - Full project status

## 🎮 Features

### Interactive Map
- **Hierarchical Sidebar**: 7 categories with expand/collapse functionality
- **Layer Toggle**: Independent control of all infrastructure layers
- **Zoom-Based Disclosure**: Progressive detail revelation (transmission → distribution → buildings)
- **Smart Filtering**: Voltage-specific transmission line filtering
- **Hover Interactions**: Cursor changes, visual feedback
- **Keyboard Shortcuts**: R to reset view

### Data Layers

**Transmission (Always Electric Blue)**
- 400kV, 275kV, 220kV Lines
- DC Interconnectors
- Transmission Substations (395 sites)
- Constraint Boundaries (34 NESO boundaries)

**Distribution (Electric Blue)**
- 132kV, 66kV, 33kV Lines
- Primary Substations

**Generation (Purple/BuPu Gradient)**
- Power Plants (2,587 sites)
- Clustered by density
- Sized by capacity

**Connection Queue (Purple Tones)**
- TEC Register Projects (2,219)
- Status-based filtering
- Technology categorization

**Network Regions (Purple)**
- GSP Boundaries (329 regions)
- DNO License Areas
- South Wales Primary Areas (195)

**Buildings (Grey)**
- 29.5M UK Building Footprints
- Vector tiles (zoom 17-20)

### Visual Design
- **Purple & BuPu Gradient**: Modern ColorBrewer-inspired palette
- **Electric Blue Grid**: Core transmission/distribution infrastructure
- **Gradient Popups**: Blue-purple speech bubbles with dotted borders
- **Glowing Lines**: Subtle blur effect on all infrastructure
- **Dark Theme**: MapTiler Backdrop Dark (no labels, pure terrain)

## 🔄 Recent Updates

**2026-11-11:**
- ✅ Added NESO transmission boundaries (34 official constraint zones)
- ✅ Introduced purple & BuPu gradient color scheme
- ✅ Migrated from Mapbox GL JS to MapLibre GL JS
- ✅ Integrated MapTiler Backdrop Dark basemap
- ✅ Redesigned popups with gradient blue speech bubbles
- ✅ Added glowing effect to all lines (zoom-responsive blur)
- ✅ Implemented hierarchical sidebar with 7 categories
- ✅ Removed all labels/borders from basemap

**2026-11-08:**
- ✅ Optimized 29.5M buildings to vector tiles (35GB, zoom 17-20)
- ✅ Set up tileserver-gl-light on localhost:8080
- ✅ Fixed sidebar layer toggle filtering
- ✅ Aesthetic overhaul: black/white/electric blue scheme

**2026-11-07:**
- ✅ Added 2,587 UK power plants (64.4 GW capacity)
- ✅ Integrated South Wales primary substations (195 areas)
- ✅ Added SPEN license boundaries
- ✅ TEC Register connection queue visualization

## 🎯 Roadmap

### Immediate (Next 2 Weeks)
- [ ] Add capacity constraint data to transmission boundaries
- [ ] Implement building footprint layer toggle
- [ ] Add network flow visualization
- [ ] Create data export functionality

### Short Term (1-3 Months)
- [ ] Complete all 6 DNO coverage (SSEN, NPG, ENWL)
- [ ] Add NGED 11kV distribution network
- [ ] Implement search functionality
- [ ] Add detailed popup information for all layers
- [ ] Create mini-map overview

### Medium Term (3-6 Months)
- [ ] Real-time generation data integration
- [ ] Demand estimation visualization
- [ ] Network constraint analysis tools
- [ ] Historical data playback
- [ ] 3D terrain visualization

### Long Term (6-12 Months)
- [ ] Low voltage (LV) network data
- [ ] Household-level granularity
- [ ] Carbon intensity visualization
- [ ] Demand forecasting
- [ ] Integration with smart meter data
- [ ] Mobile app development

## 📊 Data Sources

### Official Sources
- **NESO (National Energy System Operator)**
  - ETYS 2024 GB Transmission System Boundaries (34 boundaries)
  - TEC Register (Connection queue)
  - GSP Boundaries (329 regions)
- **UK Power Networks (UKPN)**
  - 132kV, 66kV, 33kV distribution lines
  - Primary substations
- **NGED (National Grid Electricity Distribution)**
  - South Wales primary substations (195 areas)
- **SP Energy Networks (SPEN)**
  - License area boundaries

### Community Sources
- **OpenStreetMap**: Transmission network (1,212 lines), substations (395 sites)
- **Overture Maps**: Building footprints (29.5M)
- **UK Energy Generation Map**: Power plants (2,587 sites)

## 🤝 Contributing

This is a personal project, but contributions are welcome:

### Data Contributions
- Report missing or incorrect infrastructure
- Provide access to official DNO datasets
- Share network constraint information

### Code Contributions
- Bug fixes and improvements
- New visualization features
- Performance optimizations
- Documentation improvements

### Reporting Issues
Please open an issue on GitHub with:
- Clear description of the problem
- Screenshots if applicable
- Browser/environment information

## 📄 License

**MIT License** - See LICENSE file for details

### Data Licenses
- **OSM data**: ODbL (Open Database License)
- **Overture Maps**: CDLA-Permissive-2.0
- **NESO data**: Open Government License
- **DNO data**: Various open data licenses (check individual sources)

## 🔗 Links

- **Live Application**: https://uk-energy-digital-twin.vercel.app
- **GitHub Repository**: https://github.com/NikhilSDesai/energy_digital_twin
- **MapTiler**: https://www.maptiler.com/
- **NESO Data Portal**: https://www.neso.energy/data-portal/

## 🏆 Acknowledgments

- **NESO** - Official transmission boundary data
- **OpenStreetMap** - Community-maintained transmission network
- **Overture Maps** - 29.5M building footprints
- **UK Energy Generation Map** - Comprehensive power plant database
- **MapTiler** - Clean, label-free basemap
- **MapLibre GL JS** - Open-source mapping library

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

**Built with Claude Code** • **Last updated**: November 11, 2026
