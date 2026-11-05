# UK Energy Grid Digital Twin

**🌐 LIVE:** https://uk-energy-digital-twin.vercel.app

A minimal dark-themed interactive visualization of the UK's energy transmission infrastructure.

---

## 📊 Current Status

**✅ DEPLOYED & WORKING:**
- Interactive web map with UK transmission and distribution grid
- Dark Mapbox background (labels removed for clean aesthetic)
- Transmission network: 400kV and 275kV corridors
- Distribution network: 132kV, 66kV, 33kV overhead lines (UKPN - SE England)
- Substations: 1,504 sites with clustering
- GSP boundaries: 329 regions
- Connection queue: 2,219 projects (81.7 GW)
- Zoom-based progressive disclosure
- Real-time deployment via Vercel

**📍 What You See:**
- UK transmission network (400kV and 275kV lines)
- UK Power Networks distribution (London, SE England, East England)
  - 132kV lines (685 features)
  - 66kV lines (4 features)
  - 33kV lines (6,081 features)
  - Substations (1,504 sites with metadata)
- GSP boundary regions
- Renewable energy connection queue projects
- Monochrome gold color palette for visual hierarchy
- Clean, minimal dark interface

---

## 🚀 Quick Links

- **Live Site:** https://uk-energy-digital-twin.vercel.app
- **GitHub:** https://github.com/NikhilSDesai/energy_digital_twin
- **Test Pages:**
  - Simple: https://uk-energy-digital-twin.vercel.app/test-simple.html
  - Transmission: https://uk-energy-digital-twin.vercel.app/test-transmission.html

---

## 🗺️ What's Visualized

### Current (Live)

1. **UK Transmission Grid** - Primary gold (#d4af37)
   - 14 major corridors covering entire UK
   - 400kV and 275kV routes
   - Based on National Grid ESO topology
   - Zoom-responsive line widths (2-6px)
   - Includes:
     - Scotland-England interconnectors (East & West)
     - Eastern 400kV spine (London → Edinburgh)
     - Western 400kV spine (London → Manchester → Scotland)
     - Midlands ring
     - Wales network (North & South)
     - Southwest peninsula
     - East Anglia & Humber regions

2. **UK Power Networks Distribution** - Gold monochrome palette
   - **Coverage:** London (LPN), South East (SPN), East England (EPN)
   - **Population:** 8.4M customers (~25% of UK)
   - **132kV Lines:** 685 features, 596 KB - Appears at zoom 8+
   - **66kV Lines:** 4 features, 4 KB - Appears at zoom 11+
   - **33kV Lines:** 6,081 features, 3.1 MB - Appears at zoom 11.5+
   - **Substations:** 1,504 sites, 1.2 MB - Clusters until zoom 14+
   - Progressive disclosure: Higher zoom reveals more detail
   - Rich metadata: Site type, voltage, demand, classification

3. **GSP Boundaries** - Blue overlay (329 regions, 2.5 MB)
   - Grid Supply Point administrative regions
   - Interactive popups with region info

4. **Connection Queue** - Color-coded by technology
   - 2,219 renewable energy projects
   - 81.7 GW total capacity
   - Clustering by density
   - Categories: Storage, Solar, Wind, Other

### Available for Expansion

**Distribution Networks (Other DNOs):**
- **NGED** - Midlands, South West, Wales (7.9M customers)
- **Northern Powergrid** - NE England, Yorkshire (3.9M customers)
- **SSEN** - North Scotland, South England (3.9M customers)
- **SPEN** - Scotland, NW England, N Wales (3.5M customers)
- **ENWL** - NW England (2.4M customers)
- **Scripts ready:** See `scripts/README_DNO_DATA.md`

**Other Data:**
- **Building Footprints:** 29.5M buildings from Overture Maps (2.2 GB)
- **Real-time Data:** BMRS API integration ready

---

## 🏗️ Tech Stack

**Frontend:**
- Vanilla JavaScript (no framework - for speed)
- Mapbox GL JS v3.0.1
- HTML/CSS

**Data:**
- Transmission: Manual GeoJSON based on National Grid topology
- Geographic: NESO official datasets
- Buildings: Overture Maps (downloaded but not deployed)

**Hosting & Deployment:**
- **Vercel** - Free tier, auto-deploy from GitHub
- **GitHub** - Version control
- No build process - pure static files

---

## 📁 Project Structure

```
energy_dt/
├── frontend/public/              # 🚀 DEPLOYED TO VERCEL
│   ├── index.html               # Main page
│   ├── app.js                   # Map logic (635 lines - expanded)
│   ├── data/
│   │   ├── transmission_lines.geojson          # 9.5 KB - UK grid
│   │   ├── gsp_boundaries.geojson              # 2.5 MB - GSP regions
│   │   ├── tec_register_points.geojson         # 906 KB - Connection queue
│   │   ├── ukpn-132kv-overhead-lines.geojson   # 596 KB - UKPN 132kV
│   │   ├── ukpn-66kv-overhead-lines.geojson    # 4 KB - UKPN 66kV
│   │   ├── ukpn-33kv-overhead-lines.geojson    # 3.1 MB - UKPN 33kV
│   │   ├── grid-and-primary-sites.geojson      # 1.2 MB - UKPN substations
│   │   └── [Future: all-dnos-*.geojson]        # Combined DNO files
│   ├── config.example.js        # Mapbox token template
│   └── test-*.html              # Debug/diagnostic pages
│
├── scripts/                      # Data processing
│   ├── # Transmission & System Data
│   ├── create_real_transmission_network.py   # ⭐ Generates transmission data
│   ├── download_neso_data.py                 # NESO API downloads
│   ├── simplify_geojson.py                   # Reduce GeoJSON file sizes
│   │
│   ├── # Distribution Network Data (NEW)
│   ├── download_all_dno_network_data.py      # ⭐ Download all DNO data
│   ├── convert_dno_shapefiles.py             # ⭐ Shapefile → GeoJSON
│   ├── standardize_dno_properties.py         # ⭐ Standardize schemas
│   ├── combine_dno_data.py                   # ⭐ Combine all DNOs
│   ├── process_all_dno_data.sh               # ⭐ Master script
│   ├── app_js_updated_code.js                # Frontend integration code
│   ├── README_DNO_DATA.md                    # ⭐ Complete DNO guide
│   │
│   └── # Other
│       └── download_overture_buildings.py    # Overture Maps downloader
│
├── data/
│   ├── raw/                     # Downloaded datasets
│   │   ├── infrastructure/      # GSP boundaries, substations
│   │   ├── queue/              # TEC Register, NGED queues
│   │   ├── demand/             # Historic demand (26 years)
│   │   └── operational/        # Real-time generation/demand
│   │
│   ├── dno/                     # DNO distribution network data (NEW)
│   │   ├── ukpn/raw/           # ✅ UKPN shapefiles (downloaded)
│   │   ├── nged/raw/           # 🟡 NGED shapefiles (manual download)
│   │   ├── npg/raw/            # 🟡 Northern Powergrid
│   │   ├── ssen/raw/           # 🟡 SSE Energy Networks
│   │   ├── spen/raw/           # 🟡 Scottish Power
│   │   ├── enwl/raw/           # 🟡 Electricity North West
│   │   ├── DOWNLOAD_CHECKLIST.md  # Progress tracker
│   │   └── conversion_report.json # Conversion statistics
│   │
│   └── processed/              # Processed data
│       └── uk_buildings_overture.geojson  # 18 GB - not deployed
│
├── vercel.json                  # Deployment configuration
├── README.md                    # This file (comprehensive)
└── CONTEXT.md                   # Context restoration guide
```

---

## 🎯 How It Works

### Map Rendering
```javascript
// 1. Load Mapbox dark-v11 style
// 2. Remove all text labels for clean look
// 3. Load transmission lines GeoJSON
// 4. Render as muted yellow lines (4px, 90% opacity)
```

### Data Flow
```
1. User visits site
2. Vercel serves frontend/public/
3. Browser loads app.js
4. Fetches transmission_lines.geojson
5. Mapbox renders on dark background
6. Interactive map ready (~2 seconds)
```

---

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone https://github.com/NikhilSDesai/energy_digital_twin.git
cd energy_dt

# Serve locally
cd frontend/public
python -m http.server 8000
# Visit http://localhost:8000
```

### Deploy Changes
```bash
git add .
git commit -m "Your changes"
git push
# Vercel auto-deploys in 1-2 minutes
```

### Create Mapbox Token
1. Get token from https://account.mapbox.com
2. For local dev: Create `frontend/public/config.js`:
```javascript
const CONFIG = { mapboxToken: 'pk.your-token-here' };
```
3. For production: Token embedded in app.js (already configured)

---

## 📊 Data Inventory

### Deployed (Live on Site)

| Dataset | Size | Features | Source | Coverage |
|---------|------|----------|--------|----------|
| **Transmission Lines** | 9.5 KB | 14 routes | National Grid ESO | 100% UK |
| **GSP Boundaries** | 2.5 MB | 329 regions | NESO | 100% UK |
| **TEC Register** | 906 KB | 2,219 projects | NESO | 100% UK |
| **UKPN 132kV Lines** | 596 KB | 685 lines | UK Power Networks | SE England (25%) |
| **UKPN 66kV Lines** | 4 KB | 4 lines | UK Power Networks | SE England (25%) |
| **UKPN 33kV Lines** | 3.1 MB | 6,081 lines | UK Power Networks | SE England (25%) |
| **UKPN Substations** | 1.2 MB | 1,504 sites | UK Power Networks | SE England (25%) |
| **Total Deployed** | **8.3 MB** | **~10,500** | Multiple | 25-100% UK |

### Available for Integration

**Other UK DNO Distribution Networks:**

| DNO | Coverage | Customers | Data Portal | Data Available |
|-----|----------|-----------|-------------|----------------|
| **NGED** | Midlands, SW, Wales | 7.9M | [Portal](https://connecteddata.nationalgrid.co.uk/) | 132kV, 66kV, 33kV OHL + Substations |
| **Northern Powergrid** | NE England, Yorkshire | 3.9M | [Portal](https://northernpowergrid.opendatasoft.com/) | Network schematics, LTDS data |
| **SSEN** | N Scotland, S England | 3.9M | [Portal](https://data.ssen.co.uk/) | Substation data, EHV systems |
| **SPEN** | Scotland, NW, N Wales | 3.5M | [Portal](https://spenergynetworks.opendatasoft.com/) | Line assets (all voltages) |
| **ENWL** | NW England | 2.4M | [Portal](https://electricitynorthwest.opendatasoft.com/) | Substations, network data |

**Estimated Combined Distribution Network:**
- Total features: ~40,000-50,000 (132kV, 66kV, 33kV lines + substations)
- Total size: ~25 MB raw, ~8-10 MB gzipped
- Coverage: 100% Great Britain, 30M customers
- Implementation guide: `scripts/README_DNO_DATA.md`

**Other Datasets:**

| Dataset | Size | Features | Source | Status |
|---------|------|----------|--------|--------|
| Historic Demand | 54 MB | 26 years | NESO | Downloaded |
| Overture Buildings | 18 GB | 29.5M buildings | Overture Maps | Downloaded |
| BMRS Real-time | API | Live | Elexon | Not integrated |

---

## 📚 Comprehensive Data Sources

### 🔌 Transmission Network

**National Grid ESO (Electricity System Operator)**
- **Portal:** https://data.nationalgrideso.com/
- **What We Use:**
  - Transmission network topology
  - Future Energy Scenarios (FES)
  - Electricity Ten Year Statement (ETYS)
- **License:** Open Government License v3.0
- **Coverage:** 100% GB transmission (400kV, 275kV, 132kV transmission)

### 🏭 Distribution Networks

#### UK Power Networks (UKPN) - ✅ Integrated
- **Portal:** https://ukpowernetworks.opendatasoft.com/
- **Coverage:** London (LPN), South East (SPN), East England (EPN)
- **Customers:** 8.4M (largest DNO in UK)
- **What We Use:**
  - 132kV Overhead Lines (685 lines)
  - 66kV Overhead Lines (4 lines)
  - 33kV Overhead Lines (6,081 lines)
  - Grid and Primary Sites (1,504 substations)
- **License:** Creative Commons Attribution 4.0 / OGL UK 3.0
- **Data Quality:** Verified by UKPN Open Data team
- **API:** OpenDataSoft platform with REST API
- **Download:** Direct API export (no registration required)

#### National Grid Electricity Distribution (NGED) - 🟡 Ready to Integrate
- **Portal:** https://connecteddata.nationalgrid.co.uk/
- **Former Name:** Western Power Distribution (WPD)
- **Coverage:** West Midlands, East Midlands, South West, South Wales
- **Customers:** 7.9M (second largest DNO)
- **Available Data:**
  - 132kV Overhead Lines (full NGED area)
  - 66kV Overhead Lines (full NGED area)
  - 33kV Overhead Lines (full NGED area)
  - 11kV Overhead Lines
  - Primary Substations with capacity data
  - 132kV Towers and poles
- **Formats:** ESRI Shapefile, AutoCAD DWG, Bentley MicroStation DGN, PDF
- **License:** NGED Shared Data Licence
- **Registration:** Free account required
- **Priority:** High (7.9M customers, 26% of UK)

#### Northern Powergrid (NPG) - 🟡 Ready to Integrate
- **Portal:** https://northernpowergrid.opendatasoft.com/
- **Coverage:** Northeast England, Yorkshire, North Lincolnshire
- **Customers:** 3.9M
- **Available Data:**
  - LTDS (Long Term Development Statement) network schematics
  - 132kV, 66kV, 33kV schematic diagrams
  - Primary substation data
  - Network capacity information
- **Formats:** Various (check portal for latest)
- **License:** Open data license
- **Registration:** Free registration required
- **Notes:** Provides schematic diagrams; may need to extract line data

#### SSE Energy Networks (SSEN) - 🟡 Ready to Integrate
- **Portal:** https://data.ssen.co.uk/
- **Coverage:** North Scotland (SHEPD), Central Southern England (SEPD)
- **Customers:** 3.9M
- **Available Data:**
  - Substation locations and metadata
  - EHV systems (132kV, 66kV, 33kV, 22kV)
  - Primary substation HV busbar data
  - Grid supply point data
  - Network capacity heatmaps
- **Formats:** XLSX, CSV, GeoJSON (some datasets)
- **License:** Open data
- **Registration:** Not required for most datasets
- **Notes:** Strong on substation data; overhead line data may be limited

#### Scottish Power Energy Networks (SPEN) - 🟡 Ready to Integrate
- **Portal:** https://spenergynetworks.opendatasoft.com/
- **Coverage:** Scotland (SPD), North Wales/Merseyside/Cheshire (SPM)
- **Customers:** 3.5M
- **Available Data:**
  - SPD & SPT GIS Shapefiles - Line Assets (all voltages)
  - Distribution and Transmission network assets
  - Voltage, status, operating voltage for each asset
  - Boundary information (license areas)
  - Grid supply points with generation capacity
- **Formats:** GIS Shapefiles
- **License:** Shared Data Licence
- **Registration:** Required for GIS section
- **Notes:** Comprehensive GIS data covering both distribution and transmission

#### Electricity North West (ENWL) - 🟡 Ready to Integrate
- **Portal:** https://electricitynorthwest.opendatasoft.com/
- **Coverage:** Northwest England (Greater Manchester, Lancashire)
- **Customers:** 2.4M
- **Available Data:**
  - SP ENW GIS Substations (with voltage data)
  - Network infrastructure datasets
  - Distribution Future Energy Scenarios (DFES)
  - Network capacity information
- **Formats:** Multiple formats including API access
- **License:** Open data
- **Registration:** Not required
- **Notes:** 28 datasets available; focus on substations and capacity

### 🔋 Connection Queue & Generation

**NESO TEC (Transmission Entry Capacity) Register**
- **Portal:** https://data.nationalgrideso.com/connection-registers/tec-register
- **What We Use:** 2,219 renewable projects, 81.7 GW capacity
- **Updates:** Monthly
- **License:** OGL v3.0
- **Coverage:** GB transmission-connected projects

**Elexon BMRS (Balancing Mechanism Reporting Service)**
- **Portal:** https://data.elexon.co.uk/bmrs/api/v1
- **Available:** Real-time generation, demand, carbon intensity
- **API:** REST API with live data
- **License:** BSC Open Data License
- **Status:** Not yet integrated (API ready)

### 🏘️ Geographic & Demographic

**Overture Maps - Building Footprints**
- **Portal:** https://overturemaps.org/
- **What We Downloaded:** 29.5M UK buildings (18 GB)
- **License:** Community Data License (CDLA Permissive 2.0)
- **Status:** Downloaded, not deployed (too large for Vercel)
- **Use Case:** Urban density analysis, connection planning

**Ordnance Survey Open Data**
- **Portal:** https://www.ordnancesurvey.co.uk/business-government/products/open-data
- **Available:** Boundaries, roads, buildings, terrain
- **License:** Open Government License
- **Status:** Not yet downloaded

### 📊 Energy Data Aggregators

**Open Net Zero**
- **Portal:** https://opennetzero.org/
- **Purpose:** Centralized catalog of UK energy datasets
- **Coverage:** All DNOs, NESO, Ofgem, and more
- **Use:** Dataset discovery and documentation

**UK Government Energy Portal**
- **Portal:** https://www.gov.uk/government/collections/energy-statistics
- **Data:** DUKES (Digest of UK Energy Statistics), capacity, consumption
- **License:** OGL v3.0

---

## 🎯 Data Coverage Summary

| Category | Current Coverage | Potential Coverage | Priority |
|----------|-----------------|-------------------|----------|
| **Transmission** | ✅ 100% UK | 100% | Complete |
| **Distribution** | ✅ 25% UK (UKPN) | 100% UK (all 6 DNOs) | High |
| **Substations** | ✅ 25% UK (1,504 sites) | 100% UK (~10,000 sites) | High |
| **Connection Queue** | ✅ 100% UK | 100% | Complete |
| **GSP Boundaries** | ✅ 100% UK | 100% | Complete |
| **Real-time Data** | ❌ None | Live generation/demand | Medium |
| **Buildings** | ✅ Downloaded | 100% UK | Low |

**Next Priority:** Integrate NGED distribution data (7.9M customers, Midlands/SW/Wales)

---

## 🔧 Data Processing Scripts

All data processing scripts are in `scripts/` directory:

**Distribution Network Data (NEW):**
- `download_all_dno_network_data.py` - Download from all DNO portals
- `convert_dno_shapefiles.py` - Convert shapefiles to GeoJSON
- `standardize_dno_properties.py` - Standardize property schemas
- `combine_dno_data.py` - Combine all DNOs into unified datasets
- `process_all_dno_data.sh` - Master script (runs all steps)
- `README_DNO_DATA.md` - Complete implementation guide

**Other Data:**
- `create_real_transmission_network.py` - Generate transmission GeoJSON
- `download_neso_data.py` - Download NESO datasets
- `download_overture_buildings.py` - Download Overture Maps buildings
- `simplify_geojson.py` - Reduce GeoJSON file sizes

---

## 🎨 Map Features

**Controls:**
- **Scroll:** Zoom in/out
- **Click + Drag:** Pan around
- **Press 'R':** Reset to UK view

**Styling:**
- Background: Dark Mapbox theme
- Labels: Removed (minimal aesthetic)
- Transmission Lines: #d4af37 (muted gold), 4px wide, 90% opacity
- Initial View: Full UK (center: -2.5, 54.5, zoom: 5.8)

---

## 🔧 Scripts

### Generate Transmission Network
```bash
python scripts/create_real_transmission_network.py
# Creates frontend/public/data/transmission_lines.geojson
```

### Download NESO Data
```bash
python scripts/download_neso_data.py
# Downloads: GSP boundaries, TEC Register, Historic demand
```

### Download Buildings (29.5M buildings, ~10 minutes)
```bash
source venv/bin/activate
pip install overturemaps
python scripts/download_overture_buildings.py
# Creates 18 GB GeoJSON file
```

### Simplify GeoJSON
```bash
python scripts/simplify_geojson.py
# Reduces coordinate precision
# 6.4 MB → 1.6 MB (GSP boundaries)
```

---

## 🚧 Known Issues & Limitations

### Current Limitations
- ⚠️ **Distribution coverage: 25% UK** (UKPN only - SE England)
  - NGED, NPG, SSEN, SPEN, ENWL data available but not yet integrated
  - Scripts ready for expansion to 100% UK coverage
- ❌ Buildings not deployed (too large for Vercel - 18 GB)
- ❌ No real-time data integration (BMRS API not connected)
- ⚠️ Transmission lines approximate (based on topology, not exact GPS routes)

### Deployment Constraints
- Vercel free tier: 100 MB per file limit
- Buildings dataset: 18 GB (needs external hosting: S3/R2 or vector tiles)
- Combined DNO data: ~25 MB raw (acceptable with gzip)

### Active Development
1. ✅ ~~Connection queue visualization~~ - COMPLETE
2. ✅ ~~GSP boundary overlays~~ - COMPLETE
3. ✅ ~~Distribution network (UKPN)~~ - COMPLETE (25% UK)
4. 🚧 **Complete UK distribution coverage** - IN PROGRESS
   - Scripts ready, manual DNO downloads required
   - See `scripts/README_DNO_DATA.md`

### Future Enhancements
1. **Complete UK distribution network** (Priority 1)
   - Add NGED (Midlands, SW, Wales - 7.9M customers)
   - Add NPG, SSEN, SPEN, ENWL (remaining 50% UK)
2. Real-time generation/demand data from BMRS
3. Network capacity heatmaps
4. Building footprints (via vector tiles)
5. Analytics dashboard with charts
6. Demand forecasting tools
7. Future energy scenarios (NESO FES)

---

## 🐛 Troubleshooting

**Map shows pure black:**
- This is CORRECT at low zoom (country-wide view)
- Transmission lines should be visible as yellow lines
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+F5` (Windows)

**Map not loading:**
- Check browser console for errors (F12)
- Try test pages to isolate issue
- Verify Mapbox token is valid

**Transmission lines not visible:**
- Ensure latest deployment (check vercel ls)
- Lines are muted yellow (#d4af37), should be visible at all zooms
- Try test-transmission.html page

---

## 📈 Performance

- **Initial Load:** ~2 seconds
- **Data Transfer:** ~10 KB (transmission lines only)
- **Map Tiles:** Loaded on-demand from Mapbox
- **Browser:** Modern browsers with WebGL support

---

## 🎯 Original Vision vs. Current State

### Original Goals
1. ✅ **Visualize UK energy grid** - DONE
2. ⏳ **Run infrastructure simulations** - NOT STARTED
3. ⏳ **Forecast demand** - NOT STARTED
4. ⏳ **Analyze connection queue** - DATA READY, NOT DISPLAYED

### What We Built
- Clean, minimal web visualization of transmission grid
- Real data foundation (54 MB datasets downloaded)
- Deployable, shareable product (live on Vercel)
- Extensible platform for future features

---

## 📝 Git Workflow

```bash
# Check status
git status

# Commit (NO Claude credit in messages)
git add <files>
git commit -m "Description of changes"

# Deploy
git push  # Auto-deploys to Vercel

# Monitor deployments
vercel ls
```

---

## 📚 Documentation

- **README.md** (this file) - Project overview
- **CONTEXT.md** - Context restoration guide for Claude
- **LAUNCH.md** - Original launch summary (outdated)
- **DATA_INVENTORY.md** - Detailed data documentation

---

## 🏆 Achievement Summary

**What We Accomplished:**
- ✅ Researched UK vs US energy data landscape
- ✅ Downloaded 54 MB of UK energy data (33 files)
- ✅ Built interactive web map visualization
- ✅ Deployed to production (Vercel)
- ✅ Created transmission network from grid topology
- ✅ **Integrated UK Power Networks distribution (8.4M customers)**
  - 132kV, 66kV, 33kV overhead lines (6,770 features)
  - 1,504 substations with rich metadata
  - Zoom-based progressive disclosure
  - Monochrome gold color palette
- ✅ Added GSP boundaries (329 regions)
- ✅ Added connection queue visualization (2,219 projects)
- ✅ **Created complete DNO integration toolkit**
  - 5 Python scripts for data processing
  - Automated download, conversion, standardization
  - Ready for 100% UK coverage expansion
- ✅ Downloaded 29.5M UK building footprints
- ✅ Established comprehensive data pipeline

**Time:** Multiple extended sessions
**Cost:** $0
**Status:** Live and accessible
**Coverage:** 25% distribution, 100% transmission

---

## 🔄 Next Session Priorities

### Immediate (High Impact)

1. **Complete UK Distribution Coverage** - Add remaining 5 DNOs
   - ✅ UKPN integrated (8.4M customers, 25% UK)
   - 🎯 **NGED next** (7.9M customers, Midlands/SW/Wales) - Highest priority
   - NPG, SSEN, SPEN, ENWL (remaining 50% UK)
   - Scripts ready: `scripts/README_DNO_DATA.md`
   - Manual download required from DNO portals
   - Expected: ~40,000 features, 100% GB coverage

### Medium Priority

2. **Add Real-Time Data Integration**
   - Integrate BMRS API for live generation/demand
   - Show current grid status by region
   - Carbon intensity overlay

3. **Network Capacity Visualization**
   - Download headroom datasets from DNOs
   - Visualize available capacity by region
   - Color-code by constraint level

4. **Enhanced Interactivity**
   - Filter by DNO, voltage, region
   - Layer toggles in sidebar
   - Search for substations by name

### Lower Priority

5. **Deploy Building Footprints**
   - 29.5M buildings downloaded (18 GB)
   - Options: Vector tiles, external hosting (S3/R2), or simplify

6. **Future Energy Scenarios**
   - Use NESO FES data
   - Show planned infrastructure upgrades
   - 2030/2040/2050 scenario comparison

---

## 📧 Links

- **Live Site:** https://uk-energy-digital-twin.vercel.app
- **GitHub:** https://github.com/NikhilSDesai/energy_digital_twin
- **Vercel:** Auto-deployed from main branch

---

## 📄 License

MIT - Open source

**Data Attribution:**
- National Energy System Operator (NESO) - Open Data License
- UK Power Networks (UKPN) - CC BY 4.0 / OGL UK 3.0
- National Grid Electricity Distribution (NGED) - Shared Data License
- Northern Powergrid, SSEN, SPEN, ENWL - Open Data Licenses
- Elexon BMRS - BSC Open Data License
- Overture Maps - Community Data License

---

*Last Updated: November 4, 2026*
*Version: 2.0 - Distribution Network Integration*
*Coverage: 25% Distribution (UKPN), 100% Transmission, Ready for 100% UK expansion*
